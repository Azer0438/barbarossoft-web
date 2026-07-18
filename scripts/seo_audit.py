from __future__ import annotations

import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import app as barbaros

SEO_DIR = ROOT / "seo"
DOMAIN = barbaros.SITE["domain"]
TODAY = barbaros.TODAY


@dataclass
class PageAudit:
    path: str
    route_name: str
    status_code: int
    index_policy: str
    title: str = ""
    description: str = ""
    canonical: str = ""
    robots: str = ""
    h1: list[str] = field(default_factory=list)
    links: set[str] = field(default_factory=set)
    image_alts_missing: list[str] = field(default_factory=list)
    schema_types: list[str] = field(default_factory=list)
    jsonld_errors: list[str] = field(default_factory=list)
    word_count: int = 0
    in_sitemap: bool = False
    internal_links_in: int = 0
    internal_links_out: int = 0
    issues: list[str] = field(default_factory=list)


class SEOHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.links: set[str] = set()
        self.image_alts_missing: list[str] = []
        self.schema_blocks: list[str] = []
        self.text_parts: list[str] = []
        self.h1: list[str] = []
        self._in_title = False
        self._heading_level: int | None = None
        self._heading_parts: list[str] = []
        self._in_script_ld = False
        self._script_parts: list[str] = []
        self._skip_text_tag: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            if name == "description":
                self.description = attrs_dict.get("content", "").strip()
            elif name == "robots":
                self.robots = attrs_dict.get("content", "").strip()
        elif tag == "link":
            rel = attrs_dict.get("rel", "").lower().split()
            if "canonical" in rel:
                self.canonical = attrs_dict.get("href", "").strip()
        elif tag == "a":
            href = attrs_dict.get("href", "").strip()
            if href:
                normalized = normalize_internal_url(href)
                if normalized:
                    self.links.add(normalized)
        elif tag == "img":
            src = attrs_dict.get("src", "").strip()
            alt = attrs_dict.get("alt", "")
            if src and not alt.strip():
                self.image_alts_missing.append(src)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_level = int(tag[1])
            self._heading_parts = []
        elif tag == "script":
            if "application/ld+json" in attrs_dict.get("type", "").lower():
                self._in_script_ld = True
                self._script_parts = []
            else:
                self._skip_text_tag = "script"
        elif tag in {"style", "noscript"}:
            self._skip_text_tag = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif self._heading_level and tag == f"h{self._heading_level}":
            text = clean_text(" ".join(self._heading_parts))
            if self._heading_level == 1 and text:
                self.h1.append(text)
            self._heading_level = None
            self._heading_parts = []
        elif tag == "script" and self._in_script_ld:
            block = "".join(self._script_parts).strip()
            if block:
                self.schema_blocks.append(block)
            self._in_script_ld = False
            self._script_parts = []
        elif self._skip_text_tag == tag:
            self._skip_text_tag = None

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._heading_level:
            self._heading_parts.append(data)
        if self._in_script_ld:
            self._script_parts.append(data)
            return
        if not self._skip_text_tag:
            text = clean_text(data)
            if text:
                self.text_parts.append(text)

    @property
    def title(self) -> str:
        return clean_text(" ".join(self.title_parts))

    @property
    def text(self) -> str:
        return clean_text(" ".join(self.text_parts))


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_internal_url(href: str) -> str | None:
    if href.startswith(("#", "tel:", "mailto:", "javascript:")):
        return None
    parsed = urlparse(urljoin(DOMAIN, href))
    if parsed.netloc and parsed.netloc != urlparse(DOMAIN).netloc:
        return None
    path = parsed.path or "/"
    if path.startswith("/static/"):
        return None
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path or "/"


def collect_schema_types(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        schema_type = value.get("@type")
        if isinstance(schema_type, str):
            found.append(schema_type)
        elif isinstance(schema_type, list):
            found.extend(str(item) for item in schema_type)
        for nested in value.values():
            found.extend(collect_schema_types(nested))
    elif isinstance(value, list):
        for item in value:
            found.extend(collect_schema_types(item))
    return found


def sitemap_urls() -> set[str]:
    sitemap_path = ROOT / "static" / "sitemap.xml"
    root = ET.parse(sitemap_path).getroot()
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return {loc.text.strip() for loc in root.findall(".//sm:loc", namespace) if loc.text}


def route_names() -> dict[str, str]:
    names: dict[str, str] = {}
    for rule in barbaros.app.url_map.iter_rules():
        if "GET" not in rule.methods or rule.endpoint == "static":
            continue
        if "<" not in rule.rule:
            names[rule.rule] = rule.endpoint
    for item in barbaros.PROJECTS:
        names[item["path"]] = "project_detail"
    for item in barbaros.BLOG_POSTS:
        names[item["path"]] = "blog_detail"
    return names


def canonical_paths() -> list[str]:
    paths = [
        "/",
        "/hizmetler",
        *[item["path"] for item in barbaros.SERVICES],
        "/projeler",
        *[item["path"] for item in barbaros.PROJECTS],
        *[item["path"] for item in barbaros.INDUSTRY_PAGES],
        "/hakkimizda",
        "/iletisim",
        "/blog",
        *[item["path"] for item in barbaros.BLOG_POSTS],
        *[item["path"] for item in barbaros.LEGAL_PAGES],
    ]
    return unique(paths)


def redirect_targets() -> list[tuple[str, str, str]]:
    return [
        ("/services", "/hizmetler", "Eski İngilizce hizmetler URL'si"),
        ("/projects", "/projeler", "Eski İngilizce projeler URL'si"),
        ("/about", "/hakkimizda", "Eski İngilizce hakkımızda URL'si"),
        ("/contact", "/iletisim", "Eski İngilizce iletişim URL'si"),
        ("/kurumsal-web-sitesi", "/kurumsal-web-tasarim", "Kurumsal web tasarım için tercih edilen yeni URL"),
        ("/seo-hizmeti", "/kayseri-seo", "Kayseri SEO ticari niyeti için tercih edilen URL"),
        ("/kayseri-seo-danismanligi", "/kayseri-seo", "Kayseri SEO danışmanlığı varyantı için tercih edilen URL"),
    ]


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def audit_pages() -> tuple[list[PageAudit], dict[str, PageAudit]]:
    SEO_DIR.mkdir(exist_ok=True)
    names = route_names()
    sitemap = sitemap_urls()
    index_paths = canonical_paths()
    noindex_paths = ["/fastlisting-privacy"]
    redirect_paths = [old for old, _, _ in redirect_targets()]
    all_paths = unique(index_paths + noindex_paths + redirect_paths)

    page_by_path: dict[str, PageAudit] = {}
    with barbaros.app.test_client() as client:
        for path in all_paths:
            response = client.get(path, follow_redirects=False)
            status_code = response.status_code
            policy = "redirect" if 300 <= status_code < 400 else "index, follow"
            if path in noindex_paths:
                policy = "noindex, follow"
            page = PageAudit(
                path=path,
                route_name=names.get(path, "redirect" if policy == "redirect" else "unknown"),
                status_code=status_code,
                index_policy=policy,
                in_sitemap=site_url(path) in sitemap,
            )
            if status_code == 200 and response.content_type.startswith("text/html"):
                parser = SEOHTMLParser()
                parser.feed(response.get_data(as_text=True))
                page.title = parser.title
                page.description = parser.description
                page.canonical = parser.canonical
                page.robots = parser.robots
                page.h1 = parser.h1
                page.links = parser.links
                page.image_alts_missing = parser.image_alts_missing
                page.word_count = len(re.findall(r"\w+", parser.text, flags=re.UNICODE))
                for block in parser.schema_blocks:
                    try:
                        page.schema_types.extend(collect_schema_types(json.loads(block)))
                    except json.JSONDecodeError as exc:
                        page.jsonld_errors.append(str(exc))
                page.schema_types = sorted(set(page.schema_types))
            page_by_path[path] = page

    inbound: Counter[str] = Counter()
    for page in page_by_path.values():
        page.internal_links_out = len(page.links)
        for target in page.links:
            inbound[target] += 1
    for page in page_by_path.values():
        page.internal_links_in = inbound.get(page.path, 0)

    title_counts = Counter(page.title for page in page_by_path.values() if page.title and page.status_code == 200)
    desc_counts = Counter(page.description for page in page_by_path.values() if page.description and page.status_code == 200)
    valid_200_paths = {page.path for page in page_by_path.values() if page.status_code == 200}
    valid_redirect_paths = {old for old, _, _ in redirect_targets()}

    for page in page_by_path.values():
        if page.index_policy == "redirect":
            if not 300 <= page.status_code < 400:
                page.issues.append("redirect_expected_but_not_redirecting")
            continue
        if page.status_code != 200:
            page.issues.append(f"unexpected_status_{page.status_code}")
            continue
        if page.index_policy.startswith("index"):
            expected_canonical = site_url(page.path)
            if not page.title:
                page.issues.append("missing_title")
            if not page.description:
                page.issues.append("missing_meta_description")
            if not page.canonical:
                page.issues.append("missing_canonical")
            elif page.canonical != expected_canonical:
                page.issues.append("canonical_mismatch")
            if len(page.h1) != 1:
                page.issues.append("missing_or_multiple_h1")
            if page.robots.lower().startswith("noindex"):
                page.issues.append("indexable_page_has_noindex")
            if not page.in_sitemap:
                page.issues.append("indexable_page_missing_from_sitemap")
        else:
            if page.in_sitemap:
                page.issues.append("noindex_page_in_sitemap")
            if "noindex" not in page.robots.lower():
                page.issues.append("noindex_page_missing_robots_meta")
        if page.title and title_counts[page.title] > 1:
            page.issues.append("duplicate_title")
        if page.description and desc_counts[page.description] > 1:
            page.issues.append("duplicate_meta_description")
        if page.jsonld_errors:
            page.issues.append("jsonld_parse_error")
        broken = sorted(
            link
            for link in page.links
            if link not in valid_200_paths and link not in valid_redirect_paths
        )
        if broken:
            page.issues.append("broken_internal_link:" + "|".join(broken[:5]))

    return list(page_by_path.values()), page_by_path


def site_url(path: str) -> str:
    return barbaros.site_url(path)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_url_inventory(pages: list[PageAudit]) -> None:
    rows = []
    for page in pages:
        issue = "; ".join(page.issues)
        if page.index_policy == "redirect":
            action = "301 hedefini koru ve dahili linkleri yeni URL'ye ver."
        elif not issue:
            action = "Mevcut haliyle korunabilir; Search Console'da izlenmeli."
        elif "noindex_page_in_sitemap" in page.issues:
            action = "Noindex URL'yi sitemap dışı bırak."
        elif "indexable_page_missing_from_sitemap" in page.issues:
            action = "Indexlenebilir canonical URL'yi sitemap'e ekle."
        else:
            action = "SEO validation raporundaki teknik uyarıları sırayla düzelt."
        rows.append(
            {
                "url": site_url(page.path),
                "route_name": page.route_name,
                "status_code": page.status_code,
                "indexable": "true" if page.index_policy.startswith("index") and page.status_code == 200 else "false",
                "canonical": page.canonical,
                "title": page.title,
                "meta_description": page.description,
                "h1": " | ".join(page.h1),
                "word_count_estimate": page.word_count,
                "schema_types": "|".join(page.schema_types),
                "in_sitemap": "true" if page.in_sitemap else "false",
                "internal_links_in": page.internal_links_in,
                "internal_links_out": page.internal_links_out,
                "issue": issue,
                "recommended_action": action,
            }
        )
    write_csv(
        SEO_DIR / "url-inventory.csv",
        [
            "url",
            "route_name",
            "status_code",
            "indexable",
            "canonical",
            "title",
            "meta_description",
            "h1",
            "word_count_estimate",
            "schema_types",
            "in_sitemap",
            "internal_links_in",
            "internal_links_out",
            "issue",
            "recommended_action",
        ],
        rows,
    )


def write_keyword_map() -> None:
    rows: list[dict[str, str]] = [
        keyword_row("/", "Ana sayfa", "Barbarossoft", "Kayseri dijital ajans|Kayseri web tasarım ve SEO ajansı|butik dijital ajans", "Marka ve ajans araştırması", "Kayseri / Türkiye", "Değerlendirme", "Uygulandı", "Düşük", "Barbarossoft | Kayseri Web Tasarım, SEO ve Google Ads", "İşletmeler İçin Web Tasarım, SEO ve Google Ads Çözümleri", "Ana sayfa marka ve genel ajans niyetine ayrıldı."),
        keyword_row("/kayseri-web-tasarim", "Hizmet", "kayseri web tasarım", "kayseri web tasarım firması|kayseri web sitesi|kayseri web sitesi yaptırma|kayseri web tasarım ajansı", "Ticari hizmet satın alma", "Kayseri", "Karar", "Uygulandı", "Orta", "Kayseri Web Tasarım ve Kurumsal Web Sitesi | Barbarossoft", "Kayseri Web Tasarım Hizmeti", "Ticari web tasarım niyeti bu sayfada tutuldu."),
        keyword_row("/kurumsal-web-tasarim", "Hizmet", "kurumsal web tasarım", "kurumsal web sitesi|şirket web sitesi|firma web sitesi|kurumsal site yenileme", "Ticari", "Türkiye / Kayseri", "Karar", "Yeni sayfa eklendi", "Düşük", "Kurumsal Web Tasarım ve Şirket Web Sitesi | Barbarossoft", "Kurumsal Web Tasarım Hizmeti", "Kurumsal web sitesi niyeti ayrı URL'ye alındı."),
        keyword_row("/kayseri-seo", "Hizmet", "kayseri seo", "kayseri seo danışmanlığı|kayseri seo firması|seo hizmeti kayseri|teknik seo kayseri|seo danışmanı kayseri", "Ticari yerel", "Kayseri", "Karar", "Yeni sayfa eklendi", "Orta", "Kayseri SEO Hizmeti ve SEO Danışmanlığı | Barbarossoft", "Kayseri SEO Hizmeti", "/yerel-seo ile kanibalizasyonu azaltmak için ticari danışmanlık odağı verildi."),
        keyword_row("/yerel-seo", "Hizmet", "yerel seo", "local seo hizmeti|yerel arama optimizasyonu|google yerel görünürlük|hizmet alanı seo", "Ticari ve bilgilendirici", "Türkiye / hizmet alanı işletmeleri", "Değerlendirme", "Ayrıştırıldı", "Orta", "Yerel SEO Hizmeti | Bölgesel Google Görünürlüğü", "Yerel SEO Hizmeti", "Yerel sinyaller, alaka/mesafe/bilinirlik ve GBP uyumu odağı verildi."),
        keyword_row("/google-haritalar-optimizasyonu", "Hizmet", "google haritalar optimizasyonu", "google haritalar seo|google işletme profili optimizasyonu|google maps sıralama|işletme profili yönetimi", "Ticari", "Kayseri / Türkiye", "Karar", "Ayrıştırıldı", "Düşük", "Google Haritalar Optimizasyonu ve İşletme Profili Yönetimi", "Google Haritalar Optimizasyonu", "Harita/GBP niyeti yerel SEO'dan ayrıldı."),
        keyword_row("/google-ads-yonetimi", "Hizmet", "google ads yönetimi", "kayseri google ads|google reklam yönetimi|google ads danışmanlığı|arama reklamı yönetimi", "Ticari", "Kayseri / Türkiye", "Karar", "Uygulandı", "Düşük", "Google Ads Yönetimi | Reklam Optimizasyonu - Barbarossoft", "Google Ads Yönetimi", "SEO ve Ads tamamlayıcı anlatıldı; bütçe ayrı tutuluyor."),
        keyword_row("/e-ticaret-sitesi", "Hizmet", "e-ticaret sitesi", "kayseri e-ticaret sitesi|e-ticaret web tasarım|online satış sitesi", "Ticari", "Türkiye / Kayseri", "Karar", "Uygulandı", "Düşük", "E-Ticaret Sitesi | Satış Odaklı Web Çözümleri - Barbarossoft", "E-Ticaret Sitesi", "Ürün schema kullanılmadı; hizmet mantığında kaldı."),
        keyword_row("/web-sitesi-bakim-hizmeti", "Hizmet", "web sitesi bakım hizmeti", "web sitesi güncelleme|site bakım paketi|web sitesi destek", "Ticari", "Türkiye / Kayseri", "Karar", "Uygulandı", "Düşük", "Web Sitesi Bakım Hizmeti | Güncelleme ve Destek - Barbarossoft", "Web Sitesi Bakım Hizmeti", "Bakım ile aylık SEO çalışması ayrıştırıldı."),
        keyword_row("/projeler", "Portfolyo", "Barbarossoft projeler", "web tasarım projeleri|referans web sitesi|kayseri web tasarım projeleri", "Marka güveni", "Türkiye / Kayseri", "Değerlendirme", "Uygulandı", "Düşük", "Projeler | Barbarossoft", "Gerçek işletmeler için hazırlanan dijital altyapı çalışmaları.", "Vaka kanıtı ve iç linkleme merkezi."),
        keyword_row("/hakkimizda", "Kurumsal", "Barbarossoft hakkında", "Barbarossoft kimdir|Kayseri dijital ajans hakkında", "Marka güveni", "Kayseri", "Değerlendirme", "Uygulandı", "Düşük", "Hakkımızda | Barbarossoft", "Hakkımızda", "Resmi unvan ve kuruluş tarihi manuel doğrulama bekliyor."),
        keyword_row("/iletisim", "İletişim", "Barbarossoft iletişim", "Barbarossoft telefon|Barbarossoft WhatsApp|Barbarossoft e-posta", "Dönüşüm", "Kayseri", "Dönüşüm", "Uygulandı", "Düşük", "İletişim | Barbarossoft", "İletişim", "Açık ofis adresi yayınlanmıyor."),
        keyword_row("/blog", "İçerik merkezi", "Barbarossoft blog", "web tasarım blog|seo rehberleri|google ads rehberi", "Bilgilendirici", "Türkiye", "Farkındalık", "Uygulandı", "Düşük", "Blog | Barbarossoft", "Blog", "Cluster içerik merkezi."),
    ]
    for project in barbaros.PROJECTS:
        rows.append(
            keyword_row(
                project["path"],
                "Vaka çalışması",
                f"{project['name']} projesi",
                f"{project['sector']} web tasarım|{project['sector']} dijital altyapı|Barbarossoft referans",
                "Marka ve vaka kanıtı",
                project["location"],
                "Değerlendirme",
                "Uygulandı",
                "Düşük",
                f"{project['name']} Projesi | Barbarossoft",
                f"{project['name']} Projesi",
                "Performans metriği uydurulmadı; doğrulanabilir proje kapsamı anlatıldı.",
            )
        )
    for page in barbaros.INDUSTRY_PAGES:
        rows.append(
            keyword_row(
                page["path"],
                "Sektör rehberi",
                page["title"].lower(),
                f"{page['sector']} web sitesi|{page['sector']} dijital pazarlama|sektörel web tasarım",
                "Ticari araştırma",
                "Türkiye / Kayseri",
                "Değerlendirme",
                "Uygulandı",
                "Düşük",
                f"{page['title']} | Barbarossoft",
                page["title"],
                "Sektör niyeti proje örnekleriyle destekleniyor.",
            )
        )
    for post in barbaros.BLOG_POSTS:
        rows.append(
            keyword_row(
                post["path"],
                "Blog",
                post["title"].rstrip("?").lower(),
                f"{post['category'].lower()} rehberi|{post['category'].lower()} kontrol listesi|yerel işletme dijital pazarlama",
                "Bilgilendirici",
                "Türkiye / Kayseri",
                "Farkındalık",
                "Yayında",
                "Düşük",
                f"{post['title']} | Barbarossoft",
                post["title"],
                "Blog ticari hizmet sayfasını destekleyen açıyla konumlandı.",
            )
        )
    for legal in barbaros.LEGAL_PAGES:
        rows.append(
            keyword_row(
                legal["path"],
                "Yasal",
                f"Barbarossoft {legal['title'].lower()}",
                "gizlilik|kvkk|çerez politikası|kullanım koşulları",
                "Güven ve yasal bilgilendirme",
                "Türkiye",
                "Güven",
                "Uygulandı",
                "Düşük",
                f"{legal['title']} | Barbarossoft",
                legal["title"],
                "Yasal sayfalar arama hacmi hedefiyle değil güven ve uyum amacıyla tutuldu.",
            )
        )
    write_csv(
        SEO_DIR / "keyword-url-map.csv",
        [
            "target_url",
            "page_type",
            "primary_query",
            "secondary_queries",
            "search_intent",
            "target_location",
            "funnel_stage",
            "current_status",
            "cannibalization_risk",
            "recommended_title",
            "recommended_h1",
            "notes",
        ],
        rows,
    )


def keyword_row(
    path: str,
    page_type: str,
    primary_query: str,
    secondary_queries: str,
    search_intent: str,
    target_location: str,
    funnel_stage: str,
    current_status: str,
    cannibalization_risk: str,
    recommended_title: str,
    recommended_h1: str,
    notes: str,
) -> dict[str, str]:
    return {
        "target_url": site_url(path),
        "page_type": page_type,
        "primary_query": primary_query,
        "secondary_queries": secondary_queries,
        "search_intent": search_intent,
        "target_location": target_location,
        "funnel_stage": funnel_stage,
        "current_status": current_status,
        "cannibalization_risk": cannibalization_risk,
        "recommended_title": recommended_title,
        "recommended_h1": recommended_h1,
        "notes": notes,
    }


def write_redirect_map(page_by_path: dict[str, PageAudit]) -> None:
    rows = []
    with barbaros.app.test_client() as client:
        for old, new, reason in redirect_targets():
            response = client.get(old, follow_redirects=False)
            location = response.headers.get("Location", "")
            tested = response.status_code == 301 and location.endswith(new)
            rows.append(
                {
                    "old_url": site_url(old),
                    "new_url": site_url(new),
                    "redirect_type": "301",
                    "reason": reason,
                    "implemented": "true" if page_by_path.get(old, PageAudit(old, "", 0, "")).status_code == 301 else "false",
                    "tested": "true" if tested else "false",
                }
            )
    write_csv(
        SEO_DIR / "redirect-map.csv",
        ["old_url", "new_url", "redirect_type", "reason", "implemented", "tested"],
        rows,
    )


def write_internal_link_map(page_by_path: dict[str, PageAudit]) -> None:
    recommendations = [
        ("/", "/kayseri-web-tasarim", "Kayseri web tasarım", "Ana sayfa ana hizmet kartı"),
        ("/", "/kurumsal-web-tasarim", "Kurumsal web tasarım", "Ana sayfa ana hizmet kartı"),
        ("/", "/kayseri-seo", "Kayseri SEO", "Ana sayfa ana hizmet kartı"),
        ("/", "/yerel-seo", "Yerel SEO", "Ana sayfa ana hizmet kartı"),
        ("/", "/google-haritalar-optimizasyonu", "Google Haritalar optimizasyonu", "Ana sayfa ana hizmet kartı"),
        ("/", "/google-ads-yonetimi", "Google Ads yönetimi", "Ana sayfa ana hizmet kartı"),
        ("/kayseri-seo", "/yerel-seo", "yerel SEO", "SEO hizmet sayfası kavramsal local SEO'ya bağlanır"),
        ("/kayseri-seo", "/google-haritalar-optimizasyonu", "Google İşletme Profili uyumu", "SEO hizmet sayfasında harita odağı"),
        ("/yerel-seo", "/google-haritalar-optimizasyonu", "Google Haritalar optimizasyonu", "Yerel sinyallerden GBP sayfasına geçiş"),
        ("/kurumsal-web-tasarim", "/kayseri-web-tasarim", "Kayseri web tasarım hizmeti", "Kurumsal web sayfasından yerel ticari sayfaya geçiş"),
        ("/kayseri-web-tasarim", "/blog/kayseride-web-sitesi-yaptirirken-nelere-dikkat-edilmeli", "web sitesi yaptırırken dikkat edilecekler", "İlgili rehber"),
        ("/kurumsal-web-tasarim", "/blog/kurumsal-web-sitesinde-mutlaka-bulunmasi-gereken-bolumler", "kurumsal web sitesi bölümleri", "İlgili rehber"),
        ("/google-ads-yonetimi", "/blog/google-ads-reklamlari-neden-gorunmeyebilir", "Google Ads reklamları neden görünmez", "İlgili rehber"),
        ("/google-haritalar-optimizasyonu", "/blog/google-haritalarda-isletme-siralamasi-nasil-guclendirilir", "Haritalar sıralaması", "İlgili rehber"),
        ("/projeler", "/kurumsal-web-tasarim", "kurumsal web tasarım", "Portfolyodan hizmete geçiş"),
        ("/projeler", "/kayseri-seo", "Kayseri SEO", "Portfolyodan SEO hizmetine geçiş"),
    ]
    rows = []
    for source, target, anchor, context in recommendations:
        implemented = target in page_by_path.get(source, PageAudit(source, "", 0, "")).links
        rows.append(
            {
                "source_url": site_url(source),
                "target_url": site_url(target),
                "recommended_anchor": anchor,
                "context": context,
                "implemented": "true" if implemented else "false",
            }
        )
    write_csv(
        SEO_DIR / "internal-link-map.csv",
        ["source_url", "target_url", "recommended_anchor", "context", "implemented"],
        rows,
    )


def write_schema_map(page_by_path: dict[str, PageAudit]) -> None:
    schema_rows = [
        ("/", "Ana sayfa", "ProfessionalService|WebSite|FAQPage", "name|url|image|telephone|email|areaServed", "sameAs|faq", "SITE ve HOME_FAQ", True),
        ("/hizmetler", "Hizmet listesi", "WebPage", "title|description|canonical", "BreadcrumbList", "Template metadata", False),
        ("/kayseri-web-tasarim", "Hizmet", "Service|FAQPage|BreadcrumbList", "name|description|provider|areaServed|url", "faq", "SERVICES", True),
        ("/kurumsal-web-tasarim", "Hizmet", "Service|FAQPage|BreadcrumbList", "name|description|provider|areaServed|url", "faq", "SERVICES", True),
        ("/kayseri-seo", "Hizmet", "Service|FAQPage|BreadcrumbList", "name|description|provider|areaServed|url", "faq", "SERVICES", True),
        ("/yerel-seo", "Hizmet", "Service|FAQPage|BreadcrumbList", "name|description|provider|areaServed|url", "faq", "SERVICES", True),
        ("/google-haritalar-optimizasyonu", "Hizmet", "Service|FAQPage|BreadcrumbList", "name|description|provider|areaServed|url", "faq", "SERVICES", True),
        ("/google-ads-yonetimi", "Hizmet", "Service|FAQPage|BreadcrumbList", "name|description|provider|areaServed|url", "faq", "SERVICES", True),
        ("/projeler", "Portfolyo", "CollectionPage|BreadcrumbList", "name|url|description", "hasPart", "PROJECTS", True),
        ("/projeler/{slug}", "Vaka çalışması", "CreativeWork|BreadcrumbList", "name|description|about|image|url", "publisher", "PROJECTS", True),
        ("/blog/{slug}", "Blog", "BlogPosting|BreadcrumbList", "headline|description|datePublished|dateModified|author|publisher", "image", "BLOG_POSTS", True),
        ("/iletisim", "İletişim", "WebPage", "title|description|canonical", "ContactPage", "Template metadata", False),
        ("/fastlisting-privacy", "Uygulama gizlilik", "Yok", "noindex robots meta", "", "Standalone template", True),
    ]
    rows = []
    for pattern, page_type, schema_type, required, optional, source, planned in schema_rows:
        sample_path = pattern.replace("{slug}", barbaros.PROJECTS[0]["slug"]) if "projeler/{slug}" in pattern else pattern
        sample_path = sample_path.replace("blog/{slug}", f"blog/{barbaros.BLOG_POSTS[0]['slug']}")
        page = page_by_path.get(sample_path)
        implemented = planned and page is not None and (schema_type == "Yok" or bool(page.schema_types) or "noindex" in page.robots.lower())
        validation = "valid_json_ld" if implemented and schema_type != "Yok" else "manual_review_needed"
        if page and page.jsonld_errors:
            validation = "jsonld_error"
        rows.append(
            {
                "url_pattern": site_url(pattern.replace("{slug}", "*")),
                "page_type": page_type,
                "schema_type": schema_type,
                "required_properties": required,
                "optional_properties": optional,
                "source_of_truth": source,
                "implemented": "true" if implemented else "false",
                "validation_status": validation,
            }
        )
    write_csv(
        SEO_DIR / "schema-map.csv",
        [
            "url_pattern",
            "page_type",
            "schema_type",
            "required_properties",
            "optional_properties",
            "source_of_truth",
            "implemented",
            "validation_status",
        ],
        rows,
    )


def write_content_plan() -> None:
    start = date(2026, 7, 20)
    topics = [
        ("Blog", "Kayseri'de Web Sitesi Yaptırırken Nelere Dikkat Edilmeli?", "kayseri web sitesi yaptırma", "/kayseri-web-tasarim", "Yerel web tasarım araştırması", "/kayseri-web-tasarim|/kurumsal-web-tasarim|/iletisim", "Yerel proje örnekleri ve kullanıcı soruları"),
        ("Blog", "Kurumsal Web Sitesinde Mutlaka Bulunması Gereken Bölümler", "kurumsal web sitesi bölümleri", "/kurumsal-web-tasarim", "Ticari araştırma", "/kurumsal-web-tasarim|/projeler", "Gerçek kurumsal site ekranları"),
        ("Blog", "Web Sitesi Google'da Neden Görünmez? Teknik Kontrol Listesi", "web sitesi google'da neden görünmez", "/kayseri-seo", "Problem çözme", "/kayseri-seo|/yerel-seo", "Search Console ekran görüntüsü izni"),
        ("Blog", "Yerel SEO Nedir? Kayseri'deki İşletmeler İçin Uygulama Rehberi", "yerel seo nedir", "/yerel-seo", "Bilgilendirici", "/yerel-seo|/kayseri-seo|/google-haritalar-optimizasyonu", "Gerçek hizmet alanı örnekleri"),
        ("Blog", "Google Haritalar'da İşletmeler Neden Farklı Sıralarda Görünür?", "google haritalar sıralama", "/google-haritalar-optimizasyonu", "Bilgilendirici", "/google-haritalar-optimizasyonu|/yerel-seo", "GBP ekran görüntüsü izni"),
        ("Blog", "Google İşletme Profili İçin Doğru Kategori Nasıl Seçilir?", "google işletme profili kategori seçimi", "/google-haritalar-optimizasyonu", "Uygulama rehberi", "/google-haritalar-optimizasyonu|/yerel-seo", "Doğrulanmış kategori örnekleri"),
        ("Blog", "Google Ads Reklamı Neden Görünmez?", "google ads reklamları neden görünmez", "/google-ads-yonetimi", "Problem çözme", "/google-ads-yonetimi|/iletisim", "Reklam hesabı ekran izni"),
        ("Blog", "Negatif Anahtar Kelime Nedir ve Bütçeyi Nasıl Korur?", "negatif anahtar kelime nedir", "/google-ads-yonetimi", "Uygulama rehberi", "/google-ads-yonetimi|/blog/google-ads-reklamlari-neden-gorunmeyebilir", "Gerçek arama terimi örnekleri"),
        ("Blog", "Web Sitesinden Gelen WhatsApp Tıklamaları Nasıl Ölçülür?", "whatsapp tıklama ölçümü", "/kayseri-web-tasarim", "Uygulama rehberi", "/kayseri-web-tasarim|/google-ads-yonetimi|/iletisim", "GA4 event ekran görüntüsü"),
        ("Blog", "SEO ve Google Ads Arasındaki Fark Nedir?", "seo ve google ads farkı", "/kayseri-seo", "Karşılaştırma", "/kayseri-seo|/google-ads-yonetimi", "Gerçek kampanya/organik veri izni"),
        ("Vaka çalışması", "Gerçek Bir Müşteri Vaka Çalışması", "web tasarım vaka çalışması", "/projeler", "Güven ve değerlendirme", "/projeler|/kurumsal-web-tasarim|/kayseri-seo", "Müşteri izinleri ve gerçek sonuç verileri"),
        ("Blog", "Web Sitesi Yenileme Zamanının Geldiğini Gösteren İşaretler", "web sitesi yenileme", "/kayseri-web-tasarim", "Ticari araştırma", "/kayseri-web-tasarim|/web-sitesi-bakim-hizmeti", "Mevcut site audit örnekleri"),
    ]
    rows = []
    for index, (content_type, title, query, target, intent, links, evidence) in enumerate(topics, start=1):
        rows.append(
            {
                "week": index,
                "publish_date": (start + timedelta(days=(index - 1) * 7)).isoformat(),
                "content_type": content_type,
                "working_title": title,
                "primary_query": query,
                "target_url": site_url(target),
                "search_intent": intent,
                "supporting_pillar": site_url(target),
                "internal_links_to_add": links,
                "original_evidence_needed": evidence,
                "status": "brief_hazir_yayinlanmadi",
                "owner": "Barbarossoft",
            }
        )
    write_csv(
        SEO_DIR / "90-day-content-plan.csv",
        [
            "week",
            "publish_date",
            "content_type",
            "working_title",
            "primary_query",
            "target_url",
            "search_intent",
            "supporting_pillar",
            "internal_links_to_add",
            "original_evidence_needed",
            "status",
            "owner",
        ],
        rows,
    )


def write_content_briefs() -> None:
    briefs = [
        ("Kayseri'de Web Sitesi Yaptırırken Nelere Dikkat Edilmeli?", "/kayseri-web-tasarim", "Yerel işletme sahibinin teklif almadan önce kontrol etmesi gereken alanlar."),
        ("Kurumsal Web Sitesinde Mutlaka Bulunması Gereken Bölümler", "/kurumsal-web-tasarim", "Şirket web sitesinde güven, hizmet, proje ve iletişim bölümlerinin rolü."),
        ("Web Sitesi Google'da Neden Görünmez? Teknik Kontrol Listesi", "/kayseri-seo", "Index, canonical, sitemap, noindex, hız ve içerik sorunlarını sade anlatan kontrol listesi."),
        ("Yerel SEO Nedir? Kayseri'deki İşletmeler İçin Uygulama Rehberi", "/yerel-seo", "Yerel SEO'nun alaka, mesafe ve bilinirlik mantığını dürüstçe açıklayan rehber."),
        ("Google Haritalar'da İşletmeler Neden Farklı Sıralarda Görünür?", "/google-haritalar-optimizasyonu", "Kategori, hizmet, yorum, fotoğraf, mesafe ve web sitesi uyumunu anlatan rehber."),
        ("Google İşletme Profili İçin Doğru Kategori Nasıl Seçilir?", "/google-haritalar-optimizasyonu", "Ana ve ek kategorilerin hizmet modeliyle nasıl eşleştirileceği."),
        ("Google Ads Reklamı Neden Görünmez?", "/google-ads-yonetimi", "Bütçe, onay, kalite, teklif ve lokasyon nedenlerini açıklayan yazı."),
        ("Negatif Anahtar Kelime Nedir ve Bütçeyi Nasıl Korur?", "/google-ads-yonetimi", "Arama terimi analizinden negatif kelime listesine pratik süreç."),
        ("Web Sitesinden Gelen WhatsApp Tıklamaları Nasıl Ölçülür?", "/kayseri-web-tasarim", "GA4 event, consent ve dönüşüm akışını PII göndermeden anlatan rehber."),
        ("SEO ve Google Ads Arasındaki Fark Nedir?", "/kayseri-seo", "Organik büyüme ve ücretli reklamı karar kriterleriyle karşılaştıran içerik."),
        ("Gerçek Bir Müşteri Vaka Çalışması", "/projeler", "Müşteri izni ve gerçek veriyle hazırlanacak vaka formatı."),
        ("Web Sitesi Yenileme Zamanının Geldiğini Gösteren İşaretler", "/kayseri-web-tasarim", "Hız, mobil, güven, içerik ve dönüşüm sorunları üzerinden yenileme ihtiyacı."),
    ]
    lines = [
        "# İçerik Briefleri",
        "",
        f"Üretim tarihi: {TODAY}",
        "",
        "Bu briefler otomatik yayınlanacak yazılar değildir. Gerçek proje, ekran görüntüsü, müşteri izni veya performans verisi gerektiren alanlar doğrulanmadan indexlenebilir içerik olarak yayınlanmamalıdır.",
        "",
    ]
    for title, pillar, angle in briefs:
        lines.extend(
            [
                f"## {title}",
                f"- Arama niyeti: {angle}",
                "- Hedef okuyucu: Web sitesi, SEO veya reklam yatırımı planlayan yerel işletme sahibi.",
                f"- Birincil sorgu: {title.rstrip('?').lower()}",
                "- İkincil sorgular: needs_external_validation; hacim veya zorluk verisi uydurulmadı.",
                "- Rakip içerik boşluğu: Yerel işletmeye uygulanabilir, abartısız ve örnekli anlatım.",
                "- Özgün açı: Barbarossoft süreçleri, teknik kontrol listeleri ve gerçek proje deneyimiyle açıklama.",
                "- Gerekli gerçek deneyim: [GERÇEK PROJE VERİSİ EKLENECEK]",
                f"- Önerilen H1: {title}",
                "- H2/H3 taslağı: Problem, neden olur, nasıl kontrol edilir, uygulanabilir adımlar, sık hatalar, sonraki adım.",
                f"- Dahili linkler: {site_url(pillar)}, {site_url('/iletisim')}",
                "- Harici kaynak ihtiyacı: Google Search Central, Google Business Profile veya Google Ads resmi dokümanları gerektiğinde doğrulanmalı.",
                "- Görsel ihtiyacı: Gerçek ekran görüntüsü veya izinli proje görseli; stok görsel öncelikli değil.",
                "- CTA: Ücretsiz ön görüşme / mevcut site kontrolü.",
                "- Schema: BlogPosting; gerçek yayın ve güncelleme tarihleriyle.",
                "- Editoryal kontrol: Sıralama garantisi, sahte metrik, uydurma müşteri yorumu ve keyword stuffing yok.",
                "- Yayına hazır olma kriteri: Placeholder kalmamalı, gerçek kanıt veya net kaynak eklenmeli, iç linkler kontrol edilmeli.",
                "",
            ]
        )
    (SEO_DIR / "content-briefs.md").write_text("\n".join(lines), encoding="utf-8")


def write_checklists() -> None:
    (SEO_DIR / "local-seo-checklist.md").write_text(
        "\n".join(
            [
                "# Local SEO ve Google İşletme Profili Checklist",
                "",
                "## NAP ve Site",
                "- [x] Marka adı site genelinde Barbarossoft olarak tekleştirildi.",
                "- [x] Telefon ve e-posta site genelinde tek kaynak olan SITE verisinden kullanılıyor.",
                "- [x] Açık ofis adresi yayınlanmadı; genel konum Kayseri, Türkiye olarak tutuldu.",
                "- [ ] Hizmet alanı ve çalışma modeli Google İşletme Profili politikalarına göre kullanıcı tarafından doğrulanacak.",
                "",
                "## Google İşletme Profili",
                "- [ ] İşletme adı politika uyumu kontrolü.",
                "- [ ] Ana kategori seçimi.",
                "- [ ] Ek kategoriler.",
                "- [ ] Hizmetler.",
                "- [ ] Açıklama.",
                "- [ ] Hizmet alanları.",
                "- [ ] Telefon.",
                "- [ ] Web sitesi URL'si.",
                "- [ ] Randevu/teklif URL'si.",
                "- [ ] Çalışma saatleri.",
                "- [ ] Özel saatler.",
                "- [ ] Logo.",
                "- [ ] Kapak görseli.",
                "- [ ] Gerçek iş fotoğrafları.",
                "- [ ] Düzenli güncellemeler.",
                "- [ ] Yorum isteme süreci.",
                "- [ ] Yorum yanıtlama.",
                "- [ ] Soru-cevap takibi.",
                "- [ ] Duplicate profil kontrolü.",
                "- [ ] UTM standardı: site içi linklerde UTM kullanılmaz; GBP website alanında gerekirse `utm_source=google&utm_medium=organic&utm_campaign=gbp` standardı değerlendirilebilir.",
                "- [ ] GBP landing page eşleşmesi.",
                "- [ ] Askıya alma riski kontrolü.",
                "",
                "## Yerel Sıralama Notu",
                "Yerel görünürlükte alaka düzeyi, mesafe ve bilinirlik birlikte etki eder. Mesafe doğrudan kontrol edilemez; Haritalar'da kesin ilk 3 garanti edilmez.",
            ]
        ),
        encoding="utf-8",
    )
    (SEO_DIR / "search-console-launch-checklist.md").write_text(
        "\n".join(
            [
                "# Search Console Yayına Alma Checklist",
                "",
                "## Mülk",
                "- [ ] Domain property doğrulaması.",
                "- [ ] DNS doğrulaması.",
                "- [ ] Doğru kullanıcı yetkileri.",
                "- [ ] HTTPS ve tüm subdomain kapsamı.",
                "",
                "## Yayın Öncesi",
                "- [x] Production robots dosyası kontrol edildi.",
                "- [x] Sitemap 200 ve XML content-type için route ayarlandı.",
                "- [x] Canonical kontrolü otomasyon scriptine eklendi.",
                "- [x] Noindex kontrolü otomasyon scriptine eklendi.",
                "- [x] 301 redirect kontrolü otomasyon scriptine eklendi.",
                "- [ ] Mobile render canlı ortamda URL Inspection ile kontrol edilecek.",
                "- [ ] Structured data Rich Results Test ile canlıda kontrol edilecek.",
                "- [ ] HTTPS güvenlik kontrolü canlıda yapılacak.",
                "- [x] 404 sayfası gerçek HTTP 404 döndürüyor.",
                "",
                "## Yayın Sonrası",
                "- [ ] Sitemap gönderimi.",
                "- [ ] Ana sayfa URL Inspection.",
                "- [ ] Ana hizmet sayfaları URL Inspection.",
                "- [ ] Live Test.",
                "- [ ] Rendered HTML kontrolü.",
                "- [ ] Index request yalnızca önemli sayfalarda.",
                "- [ ] Page indexing raporu.",
                "- [ ] Core Web Vitals raporu.",
                "- [ ] Enhancements/structured data raporları.",
                "- [ ] Manual actions.",
                "- [ ] Security issues.",
                "- [ ] Links raporu.",
                "- [ ] Performance baseline.",
                "",
                "## 30 Günlük Takip",
                "- [ ] Indexlenen URL sayısı.",
                "- [ ] Excluded nedenleri.",
                "- [ ] Sorgu bazlı impressions.",
                "- [ ] Marka / marka dışı ayrımı.",
                "- [ ] CTR.",
                "- [ ] Ortalama pozisyon.",
                "- [ ] Landing page performansı.",
                "- [ ] Mobil/masaüstü.",
                "- [ ] Şehir/ülke.",
                "- [ ] Organik dönüşümler.",
                "",
                "## 60-90 Gün",
                "- [ ] Kazanan/kaybeden sorgular.",
                "- [ ] Sayfa bazlı kanibalizasyon.",
                "- [ ] Düşük CTR yüksek gösterim fırsatları.",
                "- [ ] 8-20 pozisyon arasındaki sorgular.",
                "- [ ] İç link geliştirme fırsatları.",
                "- [ ] İçerik güncelleme ihtiyacı.",
                "- [ ] Yeni vaka ve özgün veri ekleme.",
            ]
        ),
        encoding="utf-8",
    )


def write_manual_todos() -> None:
    (SEO_DIR / "manual-todos.md").write_text(
        "\n".join(
            [
                "# Manuel Yapılacaklar",
                "",
                "## Doğrulanması Gereken İşletme Bilgileri",
                "- [ ] Resmi marka yazımı.",
                "- [ ] Güncel telefon ve WhatsApp.",
                "- [ ] Aktif kurumsal e-posta.",
                "- [ ] Açık adresin yayınlanıp yayınlanmayacağı.",
                "- [ ] Google İşletme Profili URL'si.",
                "- [ ] Çalışma saatleri.",
                "- [ ] Hizmet verilen şehirler.",
                "- [ ] Gerçek müşteri listesi ve yayın izinleri.",
                "- [ ] Search Console property erişimi.",
                "- [ ] GA4 property ID ve yönetici erişimi.",
                "- [ ] GTM container ID varsa doğrulama.",
                "- [ ] Gerçek organik performans verileri.",
                "- [ ] Gerçek Ads sonuçları.",
                "- [ ] Gerçek müşteri yorumları.",
                "- [ ] Kuruluş tarihi ve yasal şirket unvanı.",
                "- [ ] Sosyal medya profilleri.",
                "- [ ] İçerik yazarının gerçek adı ve biyografisi.",
                "- [ ] GSC/GA4 ekran görüntülerinin yayın izni.",
                "",
                "## Etik Backlink ve Marka Otoritesi Planı",
                "- [ ] Gerçek müşteri sitelerinden uygun referans linkleri.",
                "- [ ] Kayseri ticaret/sanayi ve mesleki dizinleri.",
                "- [ ] Yerel iş ortaklıkları.",
                "- [ ] Gerçek proje duyuruları.",
                "- [ ] Sektörel konuk içerikler.",
                "- [ ] Yerel basın ve etkinlikler.",
                "- [ ] Faydalı araç/checklist içerikleri.",
                "- [ ] Orijinal vaka çalışmaları.",
                "- [ ] Marka sosyal profilleri.",
                "- [ ] Tutarlı firma bilgileri.",
                "- [ ] Kırık link fırsatları.",
                "- [ ] Rakip backlink araştırması için harici araç ihtiyacı.",
                "",
                "Not: Link satın alma, forum spam'i, toplu profil linki, PBN veya exact-match anchor kampanyası önerilmez.",
            ]
        ),
        encoding="utf-8",
    )


def write_audit_reports(pages: list[PageAudit], page_by_path: dict[str, PageAudit]) -> None:
    indexable_count = sum(1 for page in pages if page.index_policy.startswith("index") and page.status_code == 200)
    redirect_count = sum(1 for page in pages if page.index_policy == "redirect")
    issue_pages = [page for page in pages if page.issues]
    noindex_pages = [page for page in pages if page.index_policy.startswith("noindex")]
    sitemap_count = len(sitemap_urls())
    missing_alt_count = sum(len(page.image_alts_missing) for page in pages)
    jsonld_error_count = sum(len(page.jsonld_errors) for page in pages)
    broken_links = [
        issue
        for page in pages
        for issue in page.issues
        if issue.startswith("broken_internal_link")
    ]

    audit_lines = [
        "# SEO Audit",
        "",
        f"Tarih: {TODAY}",
        f"Branch: seo/professional-audit-and-implementation",
        f"Domain: {DOMAIN}",
        "",
        "## Başlangıç Durumu",
        "- Stack: Flask, Jinja template, statik CSS/JS ve statik sitemap/robots dosyaları.",
        f"- Taranan URL sayısı: {len(pages)}.",
        f"- Indexlenebilir 200 URL sayısı: {indexable_count}.",
        f"- Redirect olarak izlenen URL sayısı: {redirect_count}.",
        f"- Sitemap URL sayısı: {sitemap_count}.",
        f"- Noindex izlenen URL sayısı: {len(noindex_pages)}.",
        "- GA4 ID bulundu: G-N0C5JP85VR. Analytics scripti çerez onayı olmadan yüklenmeyecek şekilde korunuyor.",
        "- Search Console erişimi lokal kod ortamında yok; manuel checklist oluşturuldu.",
        "- Lighthouse/PageSpeed laboratuvar testi bu scriptte çalıştırılmadı; canlı/staging ortamda manuel çalıştırılmalı.",
        "",
        "## Kritik Bulgular",
        "- `/kayseri-seo` ve `/kurumsal-web-tasarim` çekirdek SEO mimarisinde eksikti; yeni sayfalar eklendi.",
        "- Ana sayfa, ticari web tasarım niyetini hizmet sayfasıyla karıştırıyordu; marka ve genel ajans niyetine çekildi.",
        "- `/kayseri-seo` ile `/yerel-seo` arasında olası kanibalizasyon vardı; ticari SEO danışmanlığı ve kavramsal/local SEO ayrıştırıldı.",
        "- `fastlisting-privacy` Barbarossoft SEO mimarisiyle ilişkili olmadığı için noindex yapıldı ve sitemap dışına alındı.",
        "- OG locale, robots meta ve sayfa tipine göre OG type merkezi template'e eklendi.",
        "",
        "## Teknik Durum",
        f"- JSON-LD parse hatası: {jsonld_error_count}.",
        f"- Kırık dahili link uyarısı: {len(broken_links)}.",
        f"- Eksik alt metin uyarısı: {missing_alt_count}. Logo gibi dekoratif görsellerde boş alt kabul edilebilir; gerçek içerik görselleri kontrol edilmelidir.",
        f"- Uyarılı sayfa sayısı: {len(issue_pages)}. Ayrıntı `url-inventory.csv` ve `seo-validation-report.md` içinde.",
        "",
        "## Uygulanan Düzeltmeler",
        "- Yeni URL'ler: `/kurumsal-web-tasarim`, `/kayseri-seo`.",
        "- Yeni 301'ler: `/kurumsal-web-sitesi`, `/seo-hizmeti`, `/kayseri-seo-danismanligi`.",
        "- Sitemap güncellendi; noindex sayfa çıkarıldı.",
        "- Hizmet sayfalarına ölçüm/kalite kontrolleri ve ilgili rehber iç linkleri eklendi.",
        "- Proje dış linklerine `outbound_project_click`, blog detaylarına `blog_view` event'i eklendi.",
        "- Service, CreativeWork, BlogPosting, CollectionPage ve Breadcrumb JSON-LD kapsamı genişletildi.",
        "",
        "## Veri Uydurmama Notları",
        "- Anahtar kelime hacmi, KD, trafik, organik sonuç, reklam sonucu veya sıralama iddiası yazılmadı.",
        "- Açık adres yayınlanmadı.",
        "- Müşteri yorumu/rating schema eklenmedi.",
        "- Harici SERP, GBP, GSC, GA4 ve backlink işleri manuel TODO olarak belgelendi.",
    ]
    (SEO_DIR / "seo-audit.md").write_text("\n".join(audit_lines), encoding="utf-8")

    validation_lines = [
        "# SEO Validation Report",
        "",
        f"Tarih: {TODAY}",
        "",
        "## Otomatik Kontrol Özeti",
        f"- Taranan route: {len(pages)}",
        f"- Indexlenebilir 200 URL: {indexable_count}",
        f"- Redirect URL: {redirect_count}",
        f"- Sitemap URL: {sitemap_count}",
        f"- JSON-LD parse hatası: {jsonld_error_count}",
        f"- Kırık dahili link uyarısı: {len(broken_links)}",
        "",
        "## Kabul Kriterleri",
    ]
    checks = [
        ("Tüm önemli route'lar 200", all(page.status_code == 200 for page in pages if page.index_policy.startswith(("index", "noindex")))),
        ("Silinen/değişen route'lar 301", all(page_by_path[old].status_code == 301 for old, _, _ in redirect_targets())),
        ("Indexlenebilir sayfalarda self canonical", all(not any(issue == "canonical_mismatch" or issue == "missing_canonical" for issue in page.issues) for page in pages if page.index_policy.startswith("index"))),
        ("Sitemap yalnızca indexlenebilir 200 URL içeriyor", all(not any(issue == "noindex_page_in_sitemap" for issue in page.issues) for page in pages)),
        ("Noindex URL sitemap'te yok", all(not page.in_sitemap for page in noindex_pages)),
        ("Her önemli sayfada tek H1", all(not any(issue == "missing_or_multiple_h1" for issue in page.issues) for page in pages if page.index_policy.startswith("index"))),
        ("Duplicate title yok", all(not any(issue == "duplicate_title" for issue in page.issues) for page in pages)),
        ("Duplicate description yok", all(not any(issue == "duplicate_meta_description" for issue in page.issues) for page in pages)),
        ("JSON-LD parse hatası yok", jsonld_error_count == 0),
        ("Kırık dahili link yok", len(broken_links) == 0),
    ]
    for label, passed in checks:
        validation_lines.append(f"- [{'x' if passed else ' '}] {label}")
    validation_lines.extend(
        [
            "",
            "## Uyarı Detayları",
        ]
    )
    for page in pages:
        if page.issues:
            validation_lines.append(f"- {site_url(page.path)}: {'; '.join(page.issues)}")
    if not issue_pages:
        validation_lines.append("- Kritik otomatik SEO uyarısı bulunmadı.")
    validation_lines.extend(
        [
            "",
            "## Manuel Test Gerektirenler",
            "- Lighthouse/PageSpeed lab testi ve canlı Core Web Vitals izleme.",
            "- Google Rich Results Test ile schema doğrulaması.",
            "- Search Console URL Inspection ve rendered HTML kontrolü.",
            "- Canlı ortamda HTTPS, www/non-www ve HTTP yönlendirme varyantları.",
            "- Google İşletme Profili kategori, hizmet alanı, fotoğraf ve yorum süreci.",
        ]
    )
    (SEO_DIR / "seo-validation-report.md").write_text("\n".join(validation_lines), encoding="utf-8")


def main() -> None:
    pages, page_by_path = audit_pages()
    write_url_inventory(pages)
    write_keyword_map()
    write_redirect_map(page_by_path)
    write_internal_link_map(page_by_path)
    write_schema_map(page_by_path)
    write_content_plan()
    write_content_briefs()
    write_checklists()
    write_manual_todos()
    write_audit_reports(pages, page_by_path)
    print(f"SEO audit tamamlandı. {len(pages)} URL tarandı, {len([page for page in pages if page.issues])} sayfada uyarı var.")


if __name__ == "__main__":
    main()
