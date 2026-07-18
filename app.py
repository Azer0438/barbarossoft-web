from datetime import date
from urllib.parse import quote

from flask import Flask, abort, redirect, render_template, request, send_from_directory


app = Flask(__name__, static_folder="static")

TODAY = date(2026, 7, 18).isoformat()

SITE = {
    "name": "BarbarosSoft",
    "domain": "https://barbarossoft.com.tr",
    "tagline": "Kayseri merkezli butik dijital büyüme ajansı",
    "location": "Kayseri merkezli, açık ofis adresi yayınlanmıyor",
    "phone_display": "+90 505 081 02 38",
    "phone_raw": "+905050810238",
    "whatsapp_raw": "905050810238",
    "email": "azerbarbaros7@gmail.com",
    "instagram": "https://www.instagram.com/barbarossoft/",
    "business_profile": "https://share.google/OMNqU5gPIR5fwU4Re",
    "image": "/static/social-share.png",
    "whatsapp_message": "Merhaba Barbarossoft, web sitesi ve dijital pazarlama hizmetleri hakkında bilgi almak istiyorum.",
    "hours": "Pazartesi - Cumartesi, 09:00 - 19:00",
}


def site_url(path="/"):
    if path == "/":
        return SITE["domain"] + "/"
    return SITE["domain"] + path


def whatsapp_url(message=None):
    text = quote(message or SITE["whatsapp_message"])
    return f"https://wa.me/{SITE['whatsapp_raw']}?text={text}"


SERVICES = [
    {
        "slug": "kayseri-web-tasarim",
        "path": "/kayseri-web-tasarim",
        "title": "Kayseri Web Tasarım Hizmeti",
        "menu_title": "Web Tasarım",
        "category": "Ana hizmet",
        "icon": "fa-code",
        "seo_title": "Kayseri Web Tasarım | Kurumsal Web Sitesi - Barbarossoft",
        "description": "Kayseri'de mobil uyumlu, hızlı ve müşteri odaklı kurumsal web sitesi çözümleri. Web tasarım, teknik SEO ve dönüşüm altyapısı için Barbarossoft.",
        "summary": "Mobil uyumlu, hızlı, güven veren ve ziyaretçiyi telefon, WhatsApp veya teklif formuna yönlendiren kurumsal web siteleri.",
        "lead": "Yerel işletmeler için web sitesi yalnızca tanıtım alanı değil, müşteri talebi üreten bir merkez olmalı. Barbarossoft, Kayseri ve çevresindeki firmalar için güven veren, hızlı açılan ve dönüşüm noktaları net olan kurumsal web siteleri hazırlar.",
        "benefits": [
            "Mobil uyumlu ve hızlı sayfa yapısı",
            "Telefon, WhatsApp ve teklif formu odaklı akış",
            "Temel teknik SEO ve ölçüm altyapısı",
        ],
        "who": [
            "Kayseri'de hizmet veren yerel işletmeler",
            "Kurumsal görünümünü yenilemek isteyen firmalar",
            "Telefon ve WhatsApp üzerinden talep alan işletmeler",
        ],
        "problems": [
            "Eski sitenin mobilde zor kullanılması",
            "Hizmetlerin ve bölge bilgisinin net anlatılamaması",
            "Ziyaretçinin iletişim aksiyonlarına kolay ulaşamaması",
        ],
        "approach": [
            "Önce hizmetlerinizi, müşteri kazanma modelinizi ve hedef bölgelerinizi çıkarırız.",
            "Sayfa akışını güven, hizmet anlatımı ve iletişim aksiyonları üzerine kurarız.",
            "Yayına alırken temel hız, SEO, Analytics ve Search Console kontrollerini tamamlarız.",
        ],
        "scope": [
            "Kurumsal sayfa tasarımı",
            "Mobil uyumlu arayüz",
            "Hizmet sayfaları ve CTA kurgusu",
            "Temel teknik SEO kurulumu",
            "Analytics ve Search Console hazırlığı",
        ],
        "process": ["Analiz", "İçerik ve sayfa planı", "Tasarım ve geliştirme", "Yayın ve ölçüm kurulumu"],
        "faq": [
            {
                "question": "Web tasarım hizmetine SEO dahil mi?",
                "answer": "Kurumsal web sitesi projelerinde temel teknik SEO altyapısı kurulur. Düzenli içerik, sıralama takibi ve yerel SEO çalışmaları ayrı bir hizmet olarak planlanır.",
            },
            {
                "question": "Mevcut web sitem yenilenebilir mi?",
                "answer": "Evet. Mevcut sitenin teknik durumu, içerikleri ve dönüşüm noktaları incelenir; gerekiyorsa aynı alan adı korunarak yenileme yapılır.",
            },
        ],
    },
    {
        "slug": "yerel-seo",
        "path": "/yerel-seo",
        "title": "Yerel SEO Hizmeti",
        "menu_title": "Yerel SEO",
        "category": "Ana hizmet",
        "icon": "fa-magnifying-glass-chart",
        "seo_title": "Yerel SEO Hizmeti | Google'da Bölgesel Görünürlük",
        "description": "İşletmenizin hizmet verdiği şehir ve ilçelerde Google'da daha görünür olması için yerel SEO, içerik ve teknik optimizasyon hizmeti.",
        "summary": "İşletmenizin hizmet verdiği bölgelerde Google aramalarında daha görünür olması için teknik ve içerik odaklı çalışmalar.",
        "lead": "Yerel SEO, işletmenizin bulunduğu veya hizmet verdiği bölgelerde doğru aramalarda görünür olmasını hedefler. Sayfa yapısı, içerik planı, teknik kontroller ve Google İşletme Profili uyumu birlikte ele alınır.",
        "benefits": [
            "Hizmet ve bölge sayfalarının doğru kurgulanması",
            "Search Console ve teknik SEO kontrolleri",
            "Google İşletme Profili ile uyumlu içerik yapısı",
        ],
        "who": [
            "Belirli şehir veya ilçelerde hizmet veren firmalar",
            "Google aramalarından düzenli talep almak isteyen işletmeler",
            "Web sitesi ile Haritalar görünürlüğünü birlikte güçlendirmek isteyenler",
        ],
        "problems": [
            "Hizmet sayfalarının arama niyetini karşılamaması",
            "Bölge odaklı içeriklerin eksik veya zayıf olması",
            "Teknik sorunlar nedeniyle sayfaların yeterince anlaşılmaması",
        ],
        "approach": [
            "Önce mevcut görünürlük, sayfa yapısı ve hedef kelimeler incelenir.",
            "Hizmet ve bölge odaklı içerik planı hazırlanır.",
            "Teknik iyileştirmeler, iç linkleme ve ölçüm takibi düzenli şekilde ele alınır.",
        ],
        "scope": [
            "Anahtar kelime ve arama niyeti analizi",
            "Hizmet ve bölge sayfası planı",
            "Teknik SEO kontrol listesi",
            "İç linkleme ve meta düzenlemeleri",
            "Performans takip raporu",
        ],
        "process": ["Analiz", "Strateji", "İçerik ve teknik düzenleme", "Takip ve optimizasyon"],
        "faq": [
            {
                "question": "Yerel SEO ne kadar sürede etki gösterir?",
                "answer": "SEO çalışmaları rekabet, mevcut site kalitesi ve içerik durumuna göre zaman içinde olgunlaşır. Kesin süre yerine düzenli takip ve iyileştirme planı üzerinden ilerlenir.",
            },
            {
                "question": "Google Haritalar çalışması da dahil mi?",
                "answer": "Yerel SEO planında web sitesi ve Google İşletme Profili uyumu birlikte değerlendirilir. Profil optimizasyonu kapsamı teklif aşamasında netleştirilir.",
            },
        ],
    },
    {
        "slug": "google-ads-yonetimi",
        "path": "/google-ads-yonetimi",
        "title": "Google Ads Yönetimi",
        "menu_title": "Google Ads Yönetimi",
        "category": "Ana hizmet",
        "icon": "fa-bullhorn",
        "seo_title": "Google Ads Yönetimi | Reklam Optimizasyonu - Barbarossoft",
        "description": "Google Ads arama kampanyaları, dönüşüm takibi, negatif kelime yönetimi ve bütçe optimizasyonu ile daha nitelikli müşteri talepleri.",
        "summary": "Doğru anahtar kelimeler, negatif kelime yönetimi ve dönüşüm takibiyle reklam bütçesini gerçek müşteri taleplerine yönlendiren kampanyalar.",
        "lead": "Google Ads yönetiminde amaç yalnızca tıklama almak değil, işletmeye ulaşan telefon, WhatsApp ve form taleplerini ölçülebilir hale getirmektir. Kampanyalar lokasyon, hizmet ve arama niyeti odağında kurulur.",
        "benefits": [
            "Arama kampanyaları için net anahtar kelime yapısı",
            "Telefon, form ve WhatsApp dönüşüm takibi",
            "Negatif kelime ve arama terimi kontrolleri",
        ],
        "who": [
            "Kısa vadede nitelikli talep almak isteyen işletmeler",
            "Reklam bütçesinin hangi aramalara gittiğini görmek isteyenler",
            "Web sitesi veya landing page üzerinden teklif toplayan firmalar",
        ],
        "problems": [
            "Alakasız aramalardan gelen bütçe kaybı",
            "Dönüşüm ölçümü olmadığı için verimsiz kararlar",
            "Lokasyon ve reklam saatlerinin iş modeline uymaması",
        ],
        "approach": [
            "Hizmetlerinizi ve hedef bölgenizi netleştirerek kampanya yapısını planlarız.",
            "Dönüşüm takibi, negatif kelimeler ve reklam metinlerini kurarız.",
            "Arama terimlerini izleyerek kampanyayı düzenli şekilde iyileştiririz.",
        ],
        "scope": [
            "Arama kampanyası kurulumu",
            "Anahtar kelime ve negatif kelime listesi",
            "Lokasyon ve zaman planı",
            "Dönüşüm ölçüm altyapısı",
            "Düzenli optimizasyon ve raporlama",
        ],
        "process": ["Hesap kontrolü", "Kampanya kurulumu", "Dönüşüm ölçümü", "Aylık optimizasyon"],
        "faq": [
            {
                "question": "Reklam bütçesi hizmet ücretine dahil mi?",
                "answer": "Hayır. Google'a ödenecek reklam bütçesi, yönetim hizmet ücretinden ayrıdır. Bütçe işletmenin hedefi ve rekabet durumuna göre birlikte planlanır.",
            },
            {
                "question": "Mevcut reklam hesabım incelenebilir mi?",
                "answer": "Evet. Mevcut kampanya yapısı, arama terimleri, dönüşüm ayarları ve bütçe dağılımı kontrol edilerek iyileştirme planı hazırlanabilir.",
            },
        ],
    },
    {
        "slug": "google-haritalar-optimizasyonu",
        "path": "/google-haritalar-optimizasyonu",
        "title": "Google Haritalar Optimizasyonu",
        "menu_title": "Google Haritalar Optimizasyonu",
        "category": "İkincil hizmet",
        "icon": "fa-map-location-dot",
        "seo_title": "Google Haritalar Optimizasyonu | Barbarossoft",
        "description": "Google İşletme Profilinizi doğru kategori, hizmet, içerik ve web sitesi uyumuyla güçlendirin. Kayseri yerel görünürlük danışmanlığı.",
        "summary": "Google İşletme Profilinizi kategori, hizmet, fotoğraf, web sitesi uyumu ve doğru bilgi düzeniyle güçlendiren çalışma.",
        "lead": "Google Haritalar görünürlüğü, özellikle yerel hizmet işletmeleri için telefon ve yol tarifi taleplerinin önemli kaynaklarından biridir. Profil bilgileri, hizmet alanları ve web sitesi uyumu doğru kurulduğunda kullanıcıların sizi anlaması kolaylaşır.",
        "benefits": [
            "Kategori, hizmet alanı ve profil bilgisi düzeni",
            "Fotoğraf, hizmet ve açıklama içeriklerinin planlanması",
            "Web sitesiyle tutarlı yerel sinyaller",
        ],
        "who": [
            "Google İşletme Profili olan yerel işletmeler",
            "Haritalar'dan daha nitelikli talep almak isteyen firmalar",
            "Profil bilgileri dağınık veya eksik olan işletmeler",
        ],
        "problems": [
            "Yanlış kategori veya eksik hizmet bilgileri",
            "Web sitesi ile profil bilgilerinin tutarsız olması",
            "Yorum ve fotoğraf sürecinin plansız ilerlemesi",
        ],
        "approach": [
            "Profil bilgileri ve web sitesi uyumu kontrol edilir.",
            "Kategori, hizmet, açıklama ve görsel düzeni oluşturulur.",
            "Spam veya yanıltıcı bilgi kullanmadan sürdürülebilir bir profil akışı planlanır.",
        ],
        "scope": [
            "Profil kategori ve hizmet kontrolü",
            "Hizmet alanı ve iletişim bilgisi düzeni",
            "Fotoğraf ve paylaşım önerileri",
            "Web sitesi bağlantı uyumu",
            "Yorum süreci için etik yönlendirme",
        ],
        "process": ["Profil inceleme", "Bilgi düzenleme", "Web sitesi uyumu", "Takip önerileri"],
        "faq": [
            {
                "question": "Google Haritalar'da konum değişikliği yapılır mı?",
                "answer": "İşletmenin gerçek bilgilerinde değişiklik varsa profil üzerinden düzenleme yapılabilir. Yanıltıcı adres veya hizmet alanı kullanılmaz.",
            },
            {
                "question": "Yorum çalışması yapıyor musunuz?",
                "answer": "Gerçek müşterilerden etik şekilde yorum isteme süreci planlanabilir. Sahte yorum veya yanıltıcı uygulama önerilmez.",
            },
        ],
    },
    {
        "slug": "e-ticaret-sitesi",
        "path": "/e-ticaret-sitesi",
        "title": "E-Ticaret Sitesi",
        "menu_title": "E-Ticaret Sitesi",
        "category": "İkincil hizmet",
        "icon": "fa-cart-shopping",
        "seo_title": "E-Ticaret Sitesi | Satış Odaklı Web Çözümleri - Barbarossoft",
        "description": "Ürünlerinizi düzenli, güven veren ve ölçülebilir bir e-ticaret altyapısıyla sunmanız için e-ticaret sitesi kurulumu ve optimizasyonu.",
        "summary": "Ürün, kategori, ödeme, kargo ve güven unsurlarını sade bir satın alma akışıyla birleştiren e-ticaret çözümleri.",
        "lead": "E-ticaret sitesinde tasarım, ürün bulma kolaylığı ve güven unsurları birlikte çalışmalıdır. Barbarossoft, ürün yapınıza uygun kategori düzeni, ödeme akışı ve ölçüm altyapısı kurar.",
        "benefits": [
            "Mobil uyumlu ürün ve kategori sayfaları",
            "Ödeme, kargo ve güven bilgileri için net akış",
            "Satış ve reklam ölçümü için temel altyapı",
        ],
        "who": [
            "Yerel mağazasını internete taşımak isteyen işletmeler",
            "Ürünlerini düzenli bir katalogla sunmak isteyen markalar",
            "Reklam ve kampanya ile satış toplamak isteyen firmalar",
        ],
        "problems": [
            "Ürünlerin düzensiz sunulması",
            "Mobil satın alma sürecinin zor olması",
            "Kargo, iade ve iletişim bilgilerinin güven vermemesi",
        ],
        "approach": [
            "Ürün grupları, ödeme ihtiyacı ve operasyon süreci değerlendirilir.",
            "Kategori, ürün, sepet ve iletişim akışı sade şekilde tasarlanır.",
            "Yayından sonra reklam ve ölçüm ihtiyaçlarına göre yapı güçlendirilir.",
        ],
        "scope": [
            "E-ticaret arayüzü",
            "Ürün ve kategori yapısı",
            "Ödeme ve kargo sayfaları için yönlendirme",
            "Temel SEO ve ölçüm kurulumu",
            "Bakım ve geliştirme planı",
        ],
        "process": ["İhtiyaç analizi", "Ürün yapısı", "Kurulum", "Test ve yayın"],
        "faq": [
            {
                "question": "Ödeme altyapısı seçimine yardımcı oluyor musunuz?",
                "answer": "Evet. İşletmenin ihtiyacına göre uygun ödeme altyapıları değerlendirilir ve teknik entegrasyon kapsamı teklif aşamasında netleştirilir.",
            },
            {
                "question": "E-ticaret sitesi için bakım gerekiyor mu?",
                "answer": "Ürün, stok, güvenlik ve kampanya süreçleri nedeniyle düzenli bakım önerilir. Bakım kapsamı aylık destek hizmeti olarak planlanabilir.",
            },
        ],
    },
    {
        "slug": "web-sitesi-bakim-hizmeti",
        "path": "/web-sitesi-bakim-hizmeti",
        "title": "Web Sitesi Bakım Hizmeti",
        "menu_title": "Bakım ve Destek",
        "category": "İkincil hizmet",
        "icon": "fa-screwdriver-wrench",
        "seo_title": "Web Sitesi Bakım Hizmeti | Güncelleme ve Destek - Barbarossoft",
        "description": "Web sitenizin güncel, güvenli ve sorunsuz kalması için yedekleme, güncelleme, küçük içerik değişiklikleri ve performans kontrolleri.",
        "summary": "Yedekleme, güvenlik kontrolü, içerik güncellemeleri ve performans takibiyle web sitenizi düzenli tutan destek hizmeti.",
        "lead": "Web sitesi yayına alındıktan sonra içerikler, güvenlik kontrolleri ve teknik ihtiyaçlar devam eder. Bakım hizmeti, sitenin çalışır ve güncel kalmasını amaçlar.",
        "benefits": [
            "Düzenli yedekleme ve güvenlik kontrolleri",
            "Küçük içerik değişiklikleri için hızlı destek",
            "Performans ve teknik hata kontrolleri",
        ],
        "who": [
            "Sitesi yayında olan yerel işletmeler",
            "İçerik değişikliği için teknik destek isteyenler",
            "Site hızını ve güvenliğini düzenli takip etmek isteyen firmalar",
        ],
        "problems": [
            "Güncellenmeyen içerikler ve bozuk linkler",
            "Yedekleme ve güvenlik kontrollerinin ihmal edilmesi",
            "Küçük değişiklikler için sürekli vakit kaybı",
        ],
        "approach": [
            "Mevcut sitenin teknik durumu ve ihtiyaçları incelenir.",
            "Aylık bakım kapsamı ve müdahale sınırları netleştirilir.",
            "Düzenli kontroller ve küçük güncellemeler planlı şekilde yapılır.",
        ],
        "scope": [
            "Yedekleme kontrolleri",
            "Güvenlik ve hata kontrolleri",
            "Küçük içerik düzenlemeleri",
            "Performans kontrolleri",
            "Geliştirme önerileri",
        ],
        "process": ["Site kontrolü", "Bakım planı", "Aylık uygulama", "Kısa rapor"],
        "faq": [
            {
                "question": "Teslim sonrası destek politikanız nedir?",
                "answer": "Teslim sonrası hata düzeltme desteği proje kapsamına dahildir. İçerik güncelleme, bakım ve yeni geliştirmeler için aylık destek hizmeti sunulur.",
            },
            {
                "question": "Başka biri tarafından yapılan siteye bakım verebilir misiniz?",
                "answer": "Teknik yapı incelendikten sonra mümkün olan işler kapsamlandırılır. Riskli veya eksik erişimli sistemlerde önce kontrol yapılır.",
            },
        ],
    },
]

MAIN_SERVICE_SLUGS = {"kayseri-web-tasarim", "yerel-seo", "google-ads-yonetimi"}
MAIN_SERVICES = [service for service in SERVICES if service["slug"] in MAIN_SERVICE_SLUGS]
SECONDARY_SERVICES = [
    next(service for service in SERVICES if service["slug"] == "e-ticaret-sitesi"),
    next(service for service in SERVICES if service["slug"] == "web-sitesi-bakim-hizmeti"),
    {
        "slug": "ozel-yazilim-otomasyon",
        "path": "/iletisim",
        "title": "Özel Yazılım / Otomasyon",
        "menu_title": "Özel Yazılım",
        "icon": "fa-gears",
        "summary": "Tekrarlanan iş adımlarını azaltan, işletmenin sürecine göre planlanan küçük ölçekli yazılım ve otomasyon çözümleri.",
        "benefits": ["İhtiyaca özel kapsam", "Mevcut iş akışına uyum", "Bakım ve geliştirme planı"],
    },
]

PROCESS_STEPS = [
    {
        "title": "İhtiyaç Analizi",
        "text": "İşletmenizi, hedef bölgenizi, hizmetlerinizi ve müşteri kazanma sürecinizi inceliyoruz.",
    },
    {
        "title": "Planlama ve Tasarım",
        "text": "Sayfa yapısını, içerik akışını ve dönüşüm noktalarını planlayarak tasarımı hazırlıyoruz.",
    },
    {
        "title": "Kurulum ve Ölçüm",
        "text": "Siteyi yayına alıyor; Analytics, Search Console ve dönüşüm ölçüm altyapısını kuruyoruz.",
    },
    {
        "title": "Büyüme ve Optimizasyon",
        "text": "İhtiyaca göre SEO, Google Haritalar, reklam ve bakım çalışmalarıyla sistemi geliştiriyoruz.",
    },
]

WHY_ITEMS = [
    "Projeyi satış temsilcisi değil, işi yapan uzmanla görüşürsünüz.",
    "Tasarım kadar telefon ve WhatsApp dönüşümlerine odaklanılır.",
    "Süreç, kapsam ve teslimatlar açık şekilde paylaşılır.",
    "Gereksiz özellikler yerine işletmenin gerçekten ihtiyaç duyduğu sistem kurulur.",
    "Teslim sonrasında bakım, SEO ve reklam desteği devam edebilir.",
]

PACKAGES = [
    {
        "title": "Dijital Başlangıç",
        "note": "Kurumsal görünüm ve temel ölçüm altyapısı",
        "items": [
            "Kurumsal web sitesi",
            "Mobil uyumluluk",
            "Temel teknik SEO",
            "WhatsApp ve telefon butonları",
            "Analytics ve Search Console kurulumu",
            "SSL ve temel güvenlik kontrolleri",
        ],
    },
    {
        "title": "Yerel Büyüme",
        "note": "Bölgesel görünürlük ve düzenli takip",
        "items": [
            "Web sitesi veya mevcut site optimizasyonu",
            "Hizmet ve bölge sayfaları",
            "Google İşletme Profili optimizasyonu",
            "Yerel anahtar kelime çalışması",
            "Düzenli performans takibi",
        ],
    },
    {
        "title": "Müşteri Kazanım",
        "note": "Reklam, landing page ve dönüşüm takibi",
        "items": [
            "Landing page veya web sitesi",
            "Google Ads kurulumu",
            "Dönüşüm takibi",
            "Negatif anahtar kelime yönetimi",
            "Arama terimi analizi",
            "Düzenli kampanya optimizasyonu",
        ],
    },
    {
        "title": "Bakım ve Destek",
        "note": "Yayın sonrası teknik düzen ve küçük güncellemeler",
        "items": [
            "Yedekleme",
            "Güvenlik kontrolleri",
            "Yazılım güncellemeleri",
            "Küçük içerik değişiklikleri",
            "Performans kontrolleri",
        ],
    },
]

PROJECTS = [
    {
        "slug": "azr-evden-eve-nakliyat",
        "path": "/projeler/azr-evden-eve-nakliyat",
        "name": "AZR Evden Eve Nakliyat",
        "sector": "Nakliyat",
        "location": "Kayseri",
        "image": "/static/azr-logo.webp",
        "external_url": "https://www.azrevdenevenakliyat.com.tr/",
        "summary": "Kayseri'de nakliyat hizmetleri için mobil uyumlu, hızlı ve iletişim aksiyonları görünür bir kurumsal web sitesi hazırlandı.",
        "problem": "Hizmet türleri, bölge bilgileri ve hızlı iletişim aksiyonları daha düzenli sunulmalıydı.",
        "solution": "Hizmet sayfaları, telefon ve WhatsApp yönlendirmeleri, temel teknik SEO ve sade bir teklif akışı oluşturuldu.",
        "result": "Mobil uyumlu yeni site yayına alındı; hizmet sayfaları ve iletişim aksiyonları görünür hale getirildi.",
        "services": ["Kurumsal web tasarım", "Yerel SEO", "İçerik yapısı", "Dönüşüm takibi"],
        "features": ["Mobil uyumlu sayfa yapısı", "Hizmet odaklı içerik", "Telefon ve WhatsApp CTA", "Temel teknik SEO"],
    },
    {
        "slug": "dogtek-dogalgaz-kurumsal-web-sitesi",
        "path": "/projeler/dogtek-dogalgaz-kurumsal-web-sitesi",
        "name": "Doğtek Doğalgaz ve Mühendislik",
        "sector": "Doğalgaz ve mühendislik",
        "location": "Kayseri",
        "image": "/static/dogutek.png",
        "external_url": "https://www.dogtekdogalgazmuhendislik.com/",
        "summary": "Doğalgaz ve mühendislik hizmetleri için kurumsal kimliği yansıtan, mobil uyumlu ve hizmet odaklı web sitesi hazırlandı.",
        "problem": "Teknik hizmetlerin güven veren, düzenli ve kolay anlaşılır bir web yapısında sunulması gerekiyordu.",
        "solution": "Hizmet anlatımı, kurumsal görünüm, iletişim yönlendirmeleri ve temel teknik SEO yapısı birlikte kurgulandı.",
        "result": "Kurumsal web sitesi yayına hazırlandı; hizmet bilgileri ve iletişim seçenekleri daha net hale getirildi.",
        "services": ["Kurumsal web tasarım", "İçerik yapısı", "Dönüşüm takibi"],
        "features": ["Kurumsal hero alanı", "Hizmet sayfa kurgusu", "Mobil iletişim aksiyonları", "SEO meta düzeni"],
    },
    {
        "slug": "omerogullari-nakliyat",
        "path": "/projeler/omerogullari-nakliyat",
        "name": "Ömeroğulları Nakliyat",
        "sector": "Nakliyat",
        "location": "Kayseri",
        "image": "/static/omerogullari-nakliyat.png",
        "external_url": "https://omerogullarinakliyat.com.tr/",
        "summary": "Kayseri merkezli nakliyat hizmetleri için hızlı teklif formu, hizmet bölgesi anlatımı ve mobil iletişim aksiyonları öne çıkarılan web sitesi hazırlandı.",
        "problem": "Taşınma hizmetlerinde kullanıcıların hızlı teklif alabilmesi ve hizmet sürecini güvenle anlayabilmesi gerekiyordu.",
        "solution": "Hizmetler, süreç, SSS, hizmet bölgeleri, teklif formu ve WhatsApp aksiyonları tek bir akışta düzenlendi.",
        "result": "Mobil uyumlu proje yayına alındı; teklif formu, telefon ve WhatsApp yönlendirmeleri görünür hale getirildi.",
        "services": ["Kurumsal web tasarım", "Yerel SEO", "İçerik yapısı", "Dönüşüm takibi"],
        "features": ["Hızlı teklif formu", "Hizmet bölgesi sayfaları", "SSS yapısı", "Mobil WhatsApp CTA"],
    },
    {
        "slug": "kayseri-hanedan-nakliyat",
        "path": "/projeler/kayseri-hanedan-nakliyat",
        "name": "Kayseri Hanedan Nakliyat",
        "sector": "Nakliyat",
        "location": "Kayseri",
        "image": "/static/kayseri-hanedan-nakliyat.png",
        "external_url": "https://www.kayserihanedannakliyat.com.tr/",
        "summary": "Ev ve ofis taşımacılığı hizmetleri için kurumsal görünüm, hizmet anlatımı, rota/bölge yapısı ve teklif aksiyonları güçlendirildi.",
        "problem": "Nakliyat hizmetleri, rotalar, bölgeler ve hızlı iletişim kanallarının yoğun içerik içinde düzenli sunulması gerekiyordu.",
        "solution": "Kurumsal menü yapısı, hizmet/bölge kurgusu, teklif butonları ve mobil iletişim alanları düzenli bir yapıda toplandı.",
        "result": "Hizmet ve bölge odaklı kurumsal site yayına alındı; teklif, telefon ve WhatsApp aksiyonları görünür hale getirildi.",
        "services": ["Kurumsal web tasarım", "Yerel SEO", "İçerik yapısı", "Dönüşüm takibi"],
        "features": ["Rota ve bölge menüsü", "Teklif CTA", "Mobil iletişim aksiyonları", "Kurumsal görsel yapı"],
    },
    {
        "slug": "kayseri-florya-palet",
        "path": "/projeler/kayseri-florya-palet",
        "name": "Kayseri Florya Palet",
        "sector": "Palet alım satımı",
        "location": "Kayseri",
        "image": "/static/kayseri-florya-palet.png",
        "external_url": "https://www.kayserifloryapalet.com.tr/",
        "summary": "Palet alım satımı yapan işletme için ürün/hizmet anlatımı, hızlı fiyat talebi ve WhatsApp odaklı web sitesi kurgulandı.",
        "problem": "Kullanılmış ahşap palet alım satımı gibi niş bir hizmette kullanıcıların stok, sevkiyat ve teklif sürecini hızlı anlaması gerekiyordu.",
        "solution": "Hizmet anlatımı, güven veren görsel yapı, telefon ve WhatsApp teklif aksiyonları sade bir açılış akışına yerleştirildi.",
        "result": "Mobil uyumlu site yayına alındı; fiyat/teklif talebi için telefon ve WhatsApp butonları öne çıkarıldı.",
        "services": ["Kurumsal web tasarım", "Yerel SEO", "İçerik yapısı", "Dönüşüm takibi"],
        "features": ["Sektörel açılış sayfası", "Teklif CTA", "Telefon/WhatsApp yönlendirmesi", "Hızlı hizmet anlatımı"],
    },
    {
        "slug": "izodev-izolasyon",
        "path": "/projeler/izodev-izolasyon",
        "name": "İzoDev İzolasyon",
        "sector": "İzolasyon",
        "location": "Kayseri ve çevresi",
        "image": "/static/izodev-izolasyon.png",
        "external_url": "https://www.izodev.tr/",
        "summary": "Sprey poliüretan köpük yalıtım ve polyurea kaplama hizmetleri için hizmet odaklı, hızlı iletişim aksiyonları net bir web sitesi hazırlandı.",
        "problem": "Teknik izolasyon hizmetlerinin kullanıcıya açık anlatılması ve keşif/teklif taleplerinin kolay başlatılması gerekiyordu.",
        "solution": "Hizmet başlıkları, keşif talebi, telefon ve WhatsApp aksiyonları sade bir kullanıcı akışında toplandı.",
        "result": "Hizmet odaklı site yayına alındı; hızlı arama ve WhatsApp'tan teklif alma aksiyonları görünür hale getirildi.",
        "services": ["Kurumsal web tasarım", "Yerel SEO", "İçerik yapısı", "Dönüşüm takibi"],
        "features": ["Teknik hizmet anlatımı", "Keşif/teklif CTA", "Mobil iletişim butonları", "SEO meta altyapısı"],
    },
]

HOME_FAQ = [
    {
        "question": "Web sitesi ne kadar sürede hazırlanır?",
        "answer": "Hazır içerikli standart kurumsal sitelerde ilk taslak kısa sürede hazırlanabilir. Kesin teslim süresi sayfa sayısı, içerik ve özel ihtiyaçlara göre teklif aşamasında netleştirilir.",
    },
    {
        "question": "Web sitesi fiyatı nasıl belirlenir?",
        "answer": "Fiyat; sayfa sayısı, içerik ihtiyacı, özel geliştirme, SEO kapsamı ve bakım desteğine göre belirlenir. Bu yüzden net kapsam çıkarıldıktan sonra teklif paylaşılır.",
    },
    {
        "question": "Web sitesine SEO dahil mi?",
        "answer": "Kurumsal web sitesi projelerinde temel teknik SEO altyapısı kurulur. Düzenli içerik, sıralama takibi, yerel SEO ve backlink çalışmaları aylık SEO hizmeti kapsamında sunulur.",
    },
    {
        "question": "Google Ads bütçesi hizmet ücretine dahil mi?",
        "answer": "Hayır. Google'a ödenecek reklam bütçesi hizmet ücretinden ayrıdır ve doğrudan reklam hesabı üzerinden yönetilir.",
    },
    {
        "question": "Teslim sonrasında destek veriyor musunuz?",
        "answer": "Teslim sonrası hata düzeltme desteği proje kapsamına dahildir. İçerik güncelleme, bakım ve yeni geliştirmeler için aylık destek hizmeti sunulur.",
    },
    {
        "question": "İçerikleri ve görselleri kim hazırlıyor?",
        "answer": "Mevcut içerik ve görseller birlikte değerlendirilir. Eksik alanlar için sayfa metni, hizmet akışı ve görsel ihtiyaçları proje kapsamında planlanır.",
    },
    {
        "question": "Kayseri dışındaki firmalarla çalışıyor musunuz?",
        "answer": "Evet. Öncelik Kayseri ve çevresindeki yerel işletmeler olmakla birlikte uzaktan yürütülebilecek projeler için farklı şehirlerle de çalışılabilir.",
    },
    {
        "question": "Mevcut web sitemi yenileyebilir misiniz?",
        "answer": "Evet. Mevcut sitenin teknik durumu, içerikleri ve dönüşüm noktaları incelenir; alan adı ve mevcut veriler korunarak yenileme planı çıkarılır.",
    },
]

BLOG_POSTS = [
    {
        "slug": "kayseride-web-sitesi-yaptirirken-nelere-dikkat-edilmeli",
        "path": "/blog/kayseride-web-sitesi-yaptirirken-nelere-dikkat-edilmeli",
        "title": "Kayseri'de Web Sitesi Yaptırırken Nelere Dikkat Edilmeli?",
        "category": "Web Tasarım",
        "date": TODAY,
        "updated": TODAY,
        "reading_time": "5 dk",
        "description": "Kayseri'de kurumsal web sitesi yaptırmadan önce hız, mobil uyum, içerik, SEO ve dönüşüm noktalarında nelere bakmanız gerektiğini öğrenin.",
        "sections": [
            ("Mobil kullanım ilk kontrol olmalı", "Yerel işletmelerde kullanıcıların önemli bir kısmı telefon üzerinden arama yapar. Menü, hizmet sayfaları, telefon butonu ve WhatsApp bağlantısı mobil ekranda kolay ulaşılır olmalıdır."),
            ("Hizmet sayfaları net hazırlanmalı", "Ana sayfada her şeyi anlatmaya çalışmak yerine her ana hizmet için ayrı ve anlaşılır sayfalar oluşturmak kullanıcı deneyimini ve SEO altyapısını güçlendirir."),
            ("Ölçüm kurulmadan karar verilmemeli", "Analytics, Search Console ve dönüşüm takibi olmadan sitenin hangi sayfadan talep getirdiğini anlamak zorlaşır. Yayın öncesi ölçüm planı hazırlanmalıdır."),
        ],
    },
    {
        "slug": "yerel-seo-nedir-ve-hangi-isletmeler-icin-gereklidir",
        "path": "/blog/yerel-seo-nedir-ve-hangi-isletmeler-icin-gereklidir",
        "title": "Yerel SEO Nedir ve Hangi İşletmeler İçin Gereklidir?",
        "category": "SEO",
        "date": TODAY,
        "updated": TODAY,
        "reading_time": "4 dk",
        "description": "Yerel SEO'nun hizmet bölgesi olan işletmeler için neden önemli olduğunu ve web sitesiyle Google Haritalar'ın nasıl birlikte çalıştığını öğrenin.",
        "sections": [
            ("Yerel SEO arama niyetini yakalar", "Kullanıcı bir hizmeti şehir veya ilçe adıyla aradığında karşısına net, hızlı ve güven veren sayfalar çıkmalıdır. Yerel SEO bu sayfa düzenini planlar."),
            ("Google İşletme Profili tek başına yetmez", "Profil bilgileri değerli olsa da web sitesindeki hizmet ve bölge sayfalarıyla desteklenmediğinde görünürlük sınırlı kalabilir."),
            ("Düzenli takip gerekir", "Yerel SEO tek seferlik bir ayar değildir. İçerik, teknik sağlık ve arama performansı düzenli kontrol edilmelidir."),
        ],
    },
    {
        "slug": "google-haritalarda-isletme-siralamasi-nasil-guclendirilir",
        "path": "/blog/google-haritalarda-isletme-siralamasi-nasil-guclendirilir",
        "title": "Google Haritalar'da İşletme Sıralaması Nasıl Güçlendirilir?",
        "category": "Google Haritalar",
        "date": TODAY,
        "updated": TODAY,
        "reading_time": "4 dk",
        "description": "Google Haritalar görünürlüğünü güçlendirmek için kategori, hizmet, fotoğraf, yorum süreci ve web sitesi uyumunda dikkat edilmesi gerekenler.",
        "sections": [
            ("Profil bilgileri tutarlı olmalı", "Telefon, site, hizmet alanı ve kategori bilgileri gerçek işletme bilgileriyle uyumlu olmalıdır."),
            ("Hizmetler açık yazılmalı", "Kullanıcı hangi hizmeti aldığını hızlıca anlamalıdır. Profil hizmetleri ve web sitesi sayfaları aynı dili konuşmalıdır."),
            ("Sahte uygulamalardan uzak durulmalı", "Yanıltıcı adres, sahte yorum veya alakasız kategori kısa vadede cazip görünse de işletmeye kalıcı risk doğurur."),
        ],
    },
    {
        "slug": "google-ads-reklamlari-neden-gorunmeyebilir",
        "path": "/blog/google-ads-reklamlari-neden-gorunmeyebilir",
        "title": "Google Ads Reklamları Neden Görünmeyebilir?",
        "category": "Google Ads",
        "date": TODAY,
        "updated": TODAY,
        "reading_time": "4 dk",
        "description": "Google Ads reklamlarınız görünmüyorsa bütçe, kalite, lokasyon, anahtar kelime ve onay süreçlerinde kontrol edilmesi gereken alanlar.",
        "sections": [
            ("Bütçe ve teklif sınırları", "Günlük bütçe erken tükeniyorsa veya teklif stratejisi rekabet için yetersiz kalıyorsa reklam her aramada görünmeyebilir."),
            ("Lokasyon ve zaman ayarları", "Kampanya yalnızca belirli bölgelerde veya saatlerde çalışacak şekilde ayarlanmış olabilir."),
            ("Anahtar kelime ve kalite", "Anahtar kelime, reklam metni ve açılış sayfası uyumu zayıfsa kampanya performansı düşebilir."),
        ],
    },
    {
        "slug": "web-sitesinden-gelen-whatsapp-talepleri-nasil-olculur",
        "path": "/blog/web-sitesinden-gelen-whatsapp-talepleri-nasil-olculur",
        "title": "Web Sitesinden Gelen WhatsApp Talepleri Nasıl Ölçülür?",
        "category": "Dijital Pazarlama",
        "date": TODAY,
        "updated": TODAY,
        "reading_time": "4 dk",
        "description": "WhatsApp butonlarının tıklanma, form başlangıcı ve teklif talebi gibi dönüşüm olaylarıyla nasıl ölçülebileceğini öğrenin.",
        "sections": [
            ("Butonlara event eklenmeli", "WhatsApp, telefon ve e-posta linkleri ayrı event isimleriyle takip edilirse hangi kanalın daha çok talep başlattığı görülebilir."),
            ("Form başlangıcı ayrı izlenmeli", "Kullanıcı formu doldurmaya başlayıp göndermiyorsa form uzunluğu veya alan isimleri tekrar gözden geçirilebilir."),
            ("Reklam kampanyalarıyla ilişkilendirilmeli", "Google Ads dönüşüm takibiyle tıklama sonrası gelen talepler daha net değerlendirilebilir."),
        ],
    },
    {
        "slug": "kurumsal-web-sitesinde-mutlaka-bulunmasi-gereken-bolumler",
        "path": "/blog/kurumsal-web-sitesinde-mutlaka-bulunmasi-gereken-bolumler",
        "title": "Kurumsal Web Sitesinde Mutlaka Bulunması Gereken Bölümler",
        "category": "Web Tasarım",
        "date": TODAY,
        "updated": TODAY,
        "reading_time": "5 dk",
        "description": "Kurumsal web sitesinde hizmetler, projeler, hakkımızda, iletişim, SSS ve güven unsurlarının nasıl konumlanması gerektiğini keşfedin.",
        "sections": [
            ("Hizmetler sade ayrılmalı", "Ziyaretçi hangi hizmeti aldığını ve o hizmetin kendisine nasıl fayda sağladığını hızlı anlamalıdır."),
            ("Projeler kanıt sunmalı", "Proje kartlarında yalnızca görsel değil; ihtiyaç, çözüm ve yapılan iş bilgisi de yer almalıdır."),
            ("İletişim görünür olmalı", "Telefon, WhatsApp ve teklif formu özellikle mobilde kolay erişilebilir olmalıdır."),
        ],
    },
]

INDUSTRY_PAGES = [
    {
        "slug": "nakliyat-firmalari-icin-web-tasarim",
        "path": "/nakliyat-firmalari-icin-web-tasarim",
        "title": "Nakliyat Firmaları İçin Web Tasarım",
        "description": "Nakliyat firmaları için telefon, WhatsApp, hizmet bölgesi ve yerel SEO odaklı kurumsal web sitesi yaklaşımı.",
        "sector": "Nakliyat",
        "intro": "Nakliyat müşterisi çoğu zaman hızlı teklif almak, güven görmek ve hizmet bölgesini net anlamak ister. Bu yüzden nakliyat web sitesinde telefon ve WhatsApp aksiyonları, hizmet sayfaları ve bölge anlatımı kritik rol oynar.",
        "needs": ["Evden eve nakliyat, asansörlü taşıma ve şehirler arası hizmet sayfaları", "Fotoğraf, araç ve süreç bilgisiyle güven veren içerik", "Google Ads ve yerel SEO için bölge odaklı açılış sayfaları"],
        "project_slug": "azr-evden-eve-nakliyat",
    },
    {
        "slug": "dogalgaz-firmalari-icin-web-tasarim",
        "path": "/dogalgaz-firmalari-icin-web-tasarim",
        "title": "Doğalgaz Firmaları İçin Web Tasarım",
        "description": "Doğalgaz ve mühendislik firmaları için güven, hizmet anlatımı, yetki bilgileri ve iletişim odaklı web sitesi kurgusu.",
        "sector": "Doğalgaz ve mühendislik",
        "intro": "Doğalgaz firmalarında kullanıcı güven, teknik yeterlilik ve hızlı iletişim arar. Site yapısı hizmetleri anlaşılır anlatmalı, kurumsal kimliği güçlendirmeli ve teklif alma sürecini kolaylaştırmalıdır.",
        "needs": ["Kombi, tesisat, proje ve mühendislik hizmetlerinin net ayrılması", "Kurumsal güven unsurları ve belge alanları", "Telefon ve WhatsApp üzerinden hızlı keşif talebi"],
        "project_slug": "dogtek-dogalgaz-kurumsal-web-sitesi",
    },
    {
        "slug": "izolasyon-firmalari-icin-dijital-pazarlama",
        "path": "/izolasyon-firmalari-icin-dijital-pazarlama",
        "title": "İzolasyon Firmaları İçin Dijital Pazarlama",
        "description": "İzolasyon firmaları için hizmet sayfaları, yerel SEO, Google Ads ve teklif formu odaklı dijital pazarlama planı.",
        "sector": "İzolasyon",
        "intro": "İzolasyon hizmetlerinde müşteri genellikle problem odaklı arama yapar. Çatı, dış cephe, su yalıtımı veya ısı yalıtımı gibi hizmetler ayrı sayfalarda açık anlatılmalıdır.",
        "needs": ["Hizmet türlerine göre ayrı sayfa planı", "Öncesi sonrası görselleri ve uygulama süreci anlatımı", "Google Ads için teklif odaklı landing page"],
        "project_slug": "izodev-izolasyon",
    },
    {
        "slug": "sanayi-firmalari-icin-kurumsal-web-sitesi",
        "path": "/sanayi-firmalari-icin-kurumsal-web-sitesi",
        "title": "Sanayi Firmaları İçin Kurumsal Web Sitesi",
        "description": "Sanayi ve üretim firmaları için ürün, kapasite, referans ve teklif talebi odaklı kurumsal web sitesi yaklaşımı.",
        "sector": "Sanayi ve üretim",
        "intro": "Sanayi firmalarında web sitesi yalnızca tanıtım değil, güven veren bir katalog ve teklif toplama kanalıdır. Ürün grupları, üretim kapasitesi ve iletişim akışı düzenli sunulmalıdır.",
        "needs": ["Ürün ve hizmet katalog yapısı", "Kurumsal sayfalar ve sertifika alanları", "B2B teklif formu ve hızlı iletişim seçenekleri"],
        "project_slug": "kayseri-florya-palet",
    },
]

LEGAL_PAGES = [
    {
        "slug": "gizlilik-politikasi",
        "path": "/gizlilik-politikasi",
        "title": "Gizlilik Politikası",
        "description": "Barbarossoft web sitesi üzerinden işlenen kişisel veriler, iletişim kanalları, analitik çerezler ve kullanıcı hakları hakkında gizlilik bilgilendirmesi.",
        "updated": TODAY,
        "sections": [
            {
                "heading": "1. Veri sorumlusu ve kapsam",
                "paragraphs": [
                    "Bu Gizlilik Politikası; barbarossoft.com.tr adresini ziyaret eden, iletişim formunu kullanan, telefon, e-posta veya WhatsApp üzerinden Barbarossoft ile iletişime geçen kişiler için hazırlanmıştır.",
                    "Veri sorumlusu Barbarossoft'tur. Barbarossoft, Kayseri merkezli home-office/butik çalışma modeliyle hizmet verir; açık ofis adresi web sitesinde yayınlanmamaktadır. İletişim için azerbarbaros7@gmail.com ve +90 505 081 02 38 kullanılabilir.",
                ],
            },
            {
                "heading": "2. İşlenen veri kategorileri",
                "paragraphs": ["Web sitesi ve iletişim süreçlerinde yalnızca amaçla bağlantılı ve sınırlı veriler işlenir."],
                "items": [
                    "Kimlik ve iletişim bilgileri: ad soyad, firma adı, telefon, e-posta.",
                    "Talep bilgileri: ihtiyaç duyulan hizmet, mevcut web sitesi, bütçe aralığı tercihi, proje açıklaması.",
                    "İşlem güvenliği ve teknik veriler: IP adresi, tarayıcı bilgisi, cihaz türü, sayfa görüntüleme ve tıklama kayıtları.",
                    "İletişim kayıtları: WhatsApp, e-posta veya telefon üzerinden paylaşılan talep içerikleri.",
                ],
            },
            {
                "heading": "3. İşleme amaçları",
                "items": [
                    "Teklif talebini almak, değerlendirmek ve talebe dönüş yapmak.",
                    "Web tasarım, yerel SEO, Google Haritalar, Google Ads ve bakım hizmetleri için kapsam analizi yapmak.",
                    "İletişim kayıtlarını takip etmek ve müşteri ilişkilerini yürütmek.",
                    "Site güvenliğini, performansını ve kullanıcı deneyimini iyileştirmek.",
                    "Yasal yükümlülüklerin yerine getirilmesi ve olası uyuşmazlıklarda hakların korunması.",
                ],
            },
            {
                "heading": "4. Veri aktarımı",
                "paragraphs": [
                    "Kişisel veriler kural olarak üçüncü kişilere satılmaz. Hizmetin gerektirdiği ölçüde barındırma altyapısı, analitik hizmet sağlayıcıları, iletişim uygulamaları, muhasebe/hukuk danışmanları ve yetkili kamu kurumlarıyla paylaşım yapılabilir.",
                    "WhatsApp, Google Analytics ve benzeri üçüncü taraf araçlar kullanıldığında veriler ilgili hizmet sağlayıcıların teknik altyapılarında işlenebilir. Yurt dışına aktarım gerektiren hallerde KVKK'nın ilgili hükümlerine uygun hareket edilmesi hedeflenir.",
                ],
            },
            {
                "heading": "5. Saklama ve güvenlik",
                "paragraphs": [
                    "Veriler, işleme amacı için gerekli süre boyunca ve yasal saklama süreleri dikkate alınarak tutulur. Amaç ortadan kalktığında veya saklama süresi dolduğunda veriler silinir, yok edilir veya anonim hale getirilir.",
                    "Yetkisiz erişimi azaltmak için erişim kontrolü, güçlü parola kullanımı, güncel yazılım, SSL ve temel güvenlik önlemleri uygulanır.",
                ],
            },
            {
                "heading": "6. Haklarınız",
                "paragraphs": [
                    "KVKK'nın 11. maddesi kapsamındaki haklarınızı kullanmak için Barbarossoft ile e-posta veya telefon üzerinden iletişime geçebilirsiniz. Başvurular, talebin niteliğine göre kanuni süreler içinde değerlendirilir.",
                ],
            },
        ],
    },
    {
        "slug": "kvkk-aydinlatma-metni",
        "path": "/kvkk-aydinlatma-metni",
        "title": "KVKK Aydınlatma Metni",
        "description": "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında Barbarossoft iletişim ve teklif süreçleri için aydınlatma metni.",
        "updated": TODAY,
        "sections": [
            {
                "heading": "1. Veri sorumlusu",
                "paragraphs": [
                    "6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında veri sorumlusu Barbarossoft'tur. Barbarossoft'a azerbarbaros7@gmail.com e-posta adresi ve +90 505 081 02 38 telefon numarası üzerinden ulaşılabilir.",
                    "Barbarossoft home-office çalışma modeline sahiptir; bu nedenle web sitesinde açık ofis adresi yayınlanmamaktadır.",
                ],
            },
            {
                "heading": "2. Kişisel verilerin toplanma yöntemi",
                "items": [
                    "Web sitesi iletişim/teklif formu.",
                    "WhatsApp, telefon ve e-posta görüşmeleri.",
                    "Google Analytics ve benzeri analitik araçlardan gelen sınırlı teknik veriler.",
                    "Sözleşme, teklif, fatura veya destek süreçlerinde tarafınızca paylaşılan bilgiler.",
                ],
            },
            {
                "heading": "3. İşlenen kişisel veriler",
                "items": [
                    "Ad soyad, firma adı, telefon numarası ve e-posta adresi.",
                    "Talep edilen hizmet, mevcut web sitesi, bütçe aralığı tercihi ve proje açıklaması.",
                    "IP adresi, cihaz/tarayıcı bilgisi, çerez tercihleri, sayfa görüntüleme ve tıklama olayları.",
                    "Hizmet ilişkisi kurulursa teklif, sözleşme, fatura ve destek kayıtları.",
                ],
            },
            {
                "heading": "4. İşleme amaçları",
                "items": [
                    "Teklif talebinin alınması, değerlendirilmesi ve cevaplanması.",
                    "Hizmet kapsamının belirlenmesi, proje planlama ve müşteri iletişiminin yürütülmesi.",
                    "Sözleşme kurulması veya ifası, ödeme/fatura süreçlerinin yürütülmesi.",
                    "Site performansının ölçülmesi, dönüşüm takibi ve kullanıcı deneyiminin iyileştirilmesi.",
                    "Bilgi güvenliği süreçlerinin yürütülmesi ve yasal yükümlülüklerin yerine getirilmesi.",
                    "Uyuşmazlık halinde hakların tesisi, kullanılması veya korunması.",
                ],
            },
            {
                "heading": "5. Hukuki sebepler",
                "paragraphs": [
                    "Kişisel veriler; KVKK madde 5/2 kapsamında bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması, veri sorumlusunun hukuki yükümlülüğünü yerine getirmesi, bir hakkın tesisi/kullanılması/korunması ve ilgili kişinin temel hak ve özgürlüklerine zarar vermemek kaydıyla meşru menfaat hukuki sebeplerine dayanılarak işlenebilir.",
                    "Zorunlu olmayan analitik çerezler ve pazarlama niteliğindeki işlemler için gerekli hallerde açık rıza alınır.",
                ],
            },
            {
                "heading": "6. Aktarım yapılabilecek taraflar",
                "items": [
                    "Barındırma, alan adı, e-posta, analitik ve iletişim altyapısı hizmet sağlayıcıları.",
                    "WhatsApp/Meta, Google Analytics ve benzeri üçüncü taraf teknoloji sağlayıcıları.",
                    "Muhasebe, hukuk ve teknik destek danışmanları.",
                    "Yetkili kamu kurumları ve yargı mercileri.",
                ],
            },
            {
                "heading": "7. Saklama süresi",
                "paragraphs": [
                    "Teklif ve iletişim verileri, talebin sonuçlandırılması ve makul müşteri ilişkisi süreci boyunca saklanır. Hizmet ilişkisi kurulması halinde sözleşme, fatura ve destek kayıtları ilgili mevzuattaki saklama süreleri dikkate alınarak korunur.",
                    "Saklama amacı sona erdiğinde veriler silinir, yok edilir veya anonim hale getirilir.",
                ],
            },
            {
                "heading": "8. İlgili kişinin hakları",
                "items": [
                    "Kişisel verilerinizin işlenip işlenmediğini öğrenme.",
                    "İşlenmişse buna ilişkin bilgi talep etme.",
                    "İşleme amacını ve verilerin amacına uygun kullanılıp kullanılmadığını öğrenme.",
                    "Yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme.",
                    "Eksik veya yanlış işlenmiş verilerin düzeltilmesini isteme.",
                    "KVKK şartları çerçevesinde silme veya yok etme talep etme.",
                    "Düzeltme, silme veya yok etme işlemlerinin aktarılan üçüncü kişilere bildirilmesini isteme.",
                    "Otomatik sistemler sonucunda aleyhe bir sonuç çıkmasına itiraz etme.",
                    "Kanuna aykırı işleme nedeniyle zarara uğranması halinde zararın giderilmesini talep etme.",
                ],
            },
            {
                "heading": "9. Başvuru yöntemi",
                "paragraphs": [
                    "KVKK kapsamındaki taleplerinizi kimliğinizi doğrulamaya elverişli bilgilerle birlikte azerbarbaros7@gmail.com adresine iletebilirsiniz. Talebiniz, niteliğine göre en kısa sürede ve en geç kanuni süre içinde sonuçlandırılır.",
                ],
            },
        ],
    },
    {
        "slug": "cerez-politikasi",
        "path": "/cerez-politikasi",
        "title": "Çerez Politikası",
        "description": "Barbarossoft web sitesinde kullanılan zorunlu ve analitik çerezler, amaçları, saklama süreleri ve tercih yönetimi.",
        "updated": TODAY,
        "sections": [
            {
                "heading": "1. Çerez nedir?",
                "paragraphs": [
                    "Çerezler, ziyaret ettiğiniz web sitesi tarafından tarayıcınıza veya cihazınıza kaydedilebilen küçük metin dosyalarıdır. Çerezler siteyi çalıştırmak, tercihleri hatırlamak, performansı ölçmek ve kullanıcı deneyimini iyileştirmek için kullanılabilir.",
                ],
            },
            {
                "heading": "2. Bu sitede kullanılan çerez türleri",
                "items": [
                    "Zorunlu çerezler: Sitenin güvenli ve düzgün çalışması, çerez tercihinizin hatırlanması ve form güvenliği için kullanılır.",
                    "Analitik çerezler: Google Analytics aracılığıyla sayfa görüntüleme, tıklama ve dönüşüm olaylarını ölçmek için kullanılır. Bu çerezler açık rızanız olmadan etkinleştirilmez.",
                    "Üçüncü taraf bağlantıları: WhatsApp, Google ve sosyal medya bağlantılarına tıkladığınızda ilgili platformların kendi çerez ve gizlilik kuralları geçerli olabilir.",
                ],
            },
            {
                "heading": "3. Kullanılabilecek çerezler",
                "items": [
                    "barbarossoft_cookie_consent: Çerez tercihinizi hatırlar. Saklama süresi tarayıcı ayarlarınıza bağlıdır.",
                    "_ga ve _ga_*: Google Analytics tarafından ziyaretçi ve oturum ölçümü için kullanılabilir. Yalnızca analitik çerezlere onay verdiğinizde çalışır.",
                ],
            },
            {
                "heading": "4. Çerezlerin amaçları",
                "items": [
                    "Siteyi güvenli ve kararlı şekilde çalıştırmak.",
                    "Ziyaret edilen sayfaları ve tıklanan iletişim aksiyonlarını ölçmek.",
                    "Web sitesi performansını ve dönüşüm akışını iyileştirmek.",
                    "Kullanıcının çerez tercihlerini hatırlamak.",
                ],
            },
            {
                "heading": "5. Çerez tercihini yönetme",
                "paragraphs": [
                    "Siteye ilk girişte analitik çerezleri kabul edebilir veya reddedebilirsiniz. Tercihinizi tarayıcı ayarlarınızdan site verilerini temizleyerek sıfırlayabilirsiniz.",
                    "Tarayıcınız üzerinden çerezleri engelleyebilir veya silebilirsiniz; ancak bu durumda bazı tercihlerin hatırlanması mümkün olmayabilir.",
                ],
            },
        ],
    },
    {
        "slug": "kullanim-kosullari",
        "path": "/kullanim-kosullari",
        "title": "Kullanım Koşulları",
        "description": "Barbarossoft web sitesinin kullanımına, hizmet bilgilerinin kapsamına ve teklif süreçlerine ilişkin koşullar.",
        "updated": TODAY,
        "sections": [
            {
                "heading": "1. Genel kullanım",
                "paragraphs": [
                    "barbarossoft.com.tr, Barbarossoft tarafından sunulan web tasarım, yerel SEO, Google Haritalar, Google Ads, e-ticaret ve bakım hizmetleri hakkında bilgilendirme amacıyla yayınlanır.",
                    "Siteyi kullanan ziyaretçi bu kullanım koşullarını ve ilgili gizlilik/KVKK metinlerini kabul etmiş sayılır.",
                ],
            },
            {
                "heading": "2. Hizmet açıklamaları ve teklif",
                "paragraphs": [
                    "Sitedeki hizmet açıklamaları genel bilgilendirme niteliğindedir; nihai teklif, sözleşme veya garanti anlamına gelmez. Proje kapsamı, teslimatlar, süre, bakım ve ücretler görüşme sonrasında yazılı olarak netleştirilir.",
                    "Barbarossoft doğrulanmamış müşteri sayısı, sıralama garantisi, kesin reklam sonucu veya sabit performans artışı taahhüdünde bulunmaz.",
                ],
            },
            {
                "heading": "3. Fikri mülkiyet",
                "paragraphs": [
                    "Sitedeki metinler, tasarımlar, görseller, kod parçaları ve marka unsurları Barbarossoft'a veya ilgili hak sahiplerine aittir. Yazılı izin olmadan ticari amaçla kopyalanamaz, çoğaltılamaz veya yeniden yayınlanamaz.",
                ],
            },
            {
                "heading": "4. Üçüncü taraf bağlantıları",
                "paragraphs": [
                    "Sitede proje örnekleri, WhatsApp, Google, Instagram veya müşteri web sitelerine yönlendiren bağlantılar bulunabilir. Üçüncü taraf sitelerin içerik, güvenlik ve veri işleme uygulamalarından Barbarossoft sorumlu değildir.",
                ],
            },
            {
                "heading": "5. Sorumluluk sınırı",
                "paragraphs": [
                    "Barbarossoft, sitedeki bilgileri güncel ve doğru tutmaya özen gösterir; ancak teknik hata, bağlantı kesintisi, üçüncü taraf servislerdeki değişiklikler veya kullanıcı kaynaklı sorunlardan doğabilecek dolaylı zararlardan sorumlu tutulamaz.",
                ],
            },
            {
                "heading": "6. Değişiklikler",
                "paragraphs": [
                    "Barbarossoft, kullanım koşullarını, gizlilik politikasını ve hizmet açıklamalarını gerektiğinde güncelleyebilir. Güncel metinler web sitesinde yayınlandığı tarihten itibaren geçerli olur.",
                ],
            },
        ],
    },
]


def get_by_slug(collection, slug):
    return next((item for item in collection if item["slug"] == slug), None)


def get_by_path(collection, path):
    return next((item for item in collection if item["path"] == path), None)


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index + 1,
                "name": item["name"],
                "item": site_url(item["path"]),
            }
            for index, item in enumerate(items)
        ],
    }


def faq_schema(faq_items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
            }
            for item in faq_items
        ],
    }


@app.context_processor
def inject_globals():
    return {
        "site": SITE,
        "services": SERVICES,
        "legal_pages": LEGAL_PAGES,
        "current_year": date.today().year,
        "whatsapp_url": whatsapp_url,
    }


@app.route("/sitemap.xml")
@app.route("/robots.txt")
def static_from_root():
    return send_from_directory(app.static_folder, request.path.lstrip("/"))


@app.route("/")
def index():
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": SITE["name"],
            "url": SITE["domain"],
            "image": site_url(SITE["image"]),
            "telephone": SITE["phone_display"],
            "email": SITE["email"],
            "areaServed": ["Kayseri", "Türkiye"],
            "description": "Kayseri ve çevresindeki işletmeler için web tasarım, yerel SEO, Google Haritalar ve Google Ads çözümleri sunan butik dijital ajans.",
            "sameAs": [SITE["instagram"]],
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE["name"],
            "url": SITE["domain"],
        },
        faq_schema(HOME_FAQ),
    ]
    return render_template(
        "index.html",
        title="Barbarossoft | Kayseri Web Tasarım, Yerel SEO ve Google Ads",
        description="Kayseri ve çevresindeki işletmeler için dönüşüm odaklı web tasarım, yerel SEO, Google Haritalar ve Google Ads çözümleri.",
        canonical=site_url("/"),
        main_services=MAIN_SERVICES,
        secondary_services=SECONDARY_SERVICES,
        process_steps=PROCESS_STEPS,
        why_items=WHY_ITEMS,
        packages=PACKAGES,
        projects=PROJECTS,
        faq_items=HOME_FAQ,
        schema=schema,
    )


@app.route("/hizmetler")
def services_index():
    return render_template(
        "services.html",
        title="Hizmetler | Barbarossoft",
        description="Web tasarım, yerel SEO, Google Haritalar, Google Ads, e-ticaret ve web sitesi bakım hizmetlerini inceleyin.",
        canonical=site_url("/hizmetler"),
    )


def render_service_page(service):
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": service["title"],
            "description": service["description"],
            "provider": {"@type": "Organization", "name": SITE["name"], "url": SITE["domain"]},
            "areaServed": ["Kayseri", "Türkiye"],
            "url": site_url(service["path"]),
        },
        faq_schema(service["faq"]),
        breadcrumb_schema(
            [
                {"name": "Ana Sayfa", "path": "/"},
                {"name": "Hizmetler", "path": "/hizmetler"},
                {"name": service["title"], "path": service["path"]},
            ]
        ),
    ]
    return render_template(
        "service-detail.html",
        title=service["seo_title"],
        description=service["description"],
        canonical=site_url(service["path"]),
        service=service,
        projects=PROJECTS,
        schema=schema,
    )


for item in SERVICES:
    app.add_url_rule(
        item["path"],
        endpoint=f"service_{item['slug']}",
        view_func=lambda service=item: render_service_page(service),
    )


@app.route("/projeler")
def projects_index():
    schema = [
        breadcrumb_schema(
            [
                {"name": "Ana Sayfa", "path": "/"},
                {"name": "Projeler", "path": "/projeler"},
            ]
        )
    ]
    return render_template(
        "projects.html",
        title="Projeler | Barbarossoft",
        description="Barbarossoft tarafından hazırlanan gerçek web tasarım ve dijital altyapı projelerini inceleyin.",
        canonical=site_url("/projeler"),
        projects=PROJECTS,
        schema=schema,
    )


@app.route("/projeler/<slug>")
def project_detail(slug):
    project = get_by_slug(PROJECTS, slug)
    if not project:
        abort(404)
    schema = [
        breadcrumb_schema(
            [
                {"name": "Ana Sayfa", "path": "/"},
                {"name": "Projeler", "path": "/projeler"},
                {"name": project["name"], "path": project["path"]},
            ]
        )
    ]
    return render_template(
        "project-detail.html",
        title=f"{project['name']} Projesi | Barbarossoft",
        description=project["summary"],
        canonical=site_url(project["path"]),
        project=project,
        schema=schema,
    )


@app.route("/hakkimizda")
def about():
    return render_template(
        "about.html",
        title="Hakkımızda | Barbarossoft",
        description="Barbarossoft, Kayseri merkezli butik bir dijital ajans olarak yerel işletmelere web tasarım, yerel SEO, Google Haritalar ve Google Ads çözümleri geliştirir.",
        canonical=site_url("/hakkimizda"),
        why_items=WHY_ITEMS,
    )


@app.route("/iletisim")
def contact():
    return render_template(
        "contact.html",
        title="İletişim | Barbarossoft",
        description="Barbarossoft ile telefon, WhatsApp, e-posta veya teklif formu üzerinden iletişime geçin.",
        canonical=site_url("/iletisim"),
        form={},
        errors={},
    )


@app.route("/teklif", methods=["POST"])
def quote_request():
    form = {key: request.form.get(key, "").strip() for key in request.form}
    required_fields = {
        "name": "Ad soyad",
        "company": "Firma adı",
        "phone": "Telefon",
        "email": "E-posta",
        "service": "İhtiyaç duyulan hizmet",
        "description": "Kısa proje açıklaması",
    }
    errors = {
        field: f"{label} alanı zorunludur."
        for field, label in required_fields.items()
        if not form.get(field)
    }
    if form.get("email") and "@" not in form["email"]:
        errors["email"] = "Geçerli bir e-posta adresi yazın."
    if form.get("website_url"):
        return render_template(
            "contact.html",
            title="İletişim | Barbarossoft",
            description="Barbarossoft teklif formu.",
            canonical=site_url("/iletisim"),
            form={},
            errors={},
            success="Talebiniz alındı. En kısa sürede dönüş yapılacaktır.",
        )
    if form.get("consent") != "on":
        errors["consent"] = "İletişim için verilerin işlenmesine onay vermeniz gerekir."
    if errors:
        return (
            render_template(
                "contact.html",
                title="İletişim | Barbarossoft",
                description="Barbarossoft teklif formu.",
                canonical=site_url("/iletisim"),
                form=form,
                errors=errors,
            ),
            400,
        )

    message = "\n".join(
        [
            "Merhaba Barbarossoft, teklif talebi göndermek istiyorum.",
            f"Ad Soyad: {form.get('name', '')}",
            f"Firma: {form.get('company', '')}",
            f"Telefon: {form.get('phone', '')}",
            f"E-posta: {form.get('email', '')}",
            f"Hizmet: {form.get('service', '')}",
            f"Web sitesi: {form.get('website', '')}",
            f"Bütçe: {form.get('budget', '')}",
            f"Açıklama: {form.get('description', '')}",
        ]
    )
    return redirect(whatsapp_url(message), code=302)


@app.route("/blog")
def blog_index():
    return render_template(
        "blog.html",
        title="Blog | Barbarossoft",
        description="Web tasarım, yerel SEO, Google Haritalar ve Google Ads hakkında yerel işletmeler için pratik yazılar.",
        canonical=site_url("/blog"),
        posts=BLOG_POSTS,
    )


@app.route("/blog/<slug>")
def blog_detail(slug):
    post = get_by_slug(BLOG_POSTS, slug)
    if not post:
        abort(404)
    related = [item for item in BLOG_POSTS if item["slug"] != slug][:3]
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": post["title"],
            "description": post["description"],
            "datePublished": post["date"],
            "dateModified": post["updated"],
            "author": {"@type": "Organization", "name": SITE["name"]},
            "publisher": {"@type": "Organization", "name": SITE["name"]},
            "mainEntityOfPage": site_url(post["path"]),
        },
        breadcrumb_schema(
            [
                {"name": "Ana Sayfa", "path": "/"},
                {"name": "Blog", "path": "/blog"},
                {"name": post["title"], "path": post["path"]},
            ]
        ),
    ]
    return render_template(
        "blog-detail.html",
        title=f"{post['title']} | Barbarossoft",
        description=post["description"],
        canonical=site_url(post["path"]),
        post=post,
        related_posts=related,
        schema=schema,
    )


def render_industry_page(page):
    project = get_by_slug(PROJECTS, page["project_slug"]) if page.get("project_slug") else None
    schema = [
        breadcrumb_schema(
            [
                {"name": "Ana Sayfa", "path": "/"},
                {"name": page["title"], "path": page["path"]},
            ]
        )
    ]
    return render_template(
        "industry-detail.html",
        title=f"{page['title']} | Barbarossoft",
        description=page["description"],
        canonical=site_url(page["path"]),
        page=page,
        project=project,
        schema=schema,
    )


for item in INDUSTRY_PAGES:
    app.add_url_rule(
        item["path"],
        endpoint=f"industry_{item['slug']}",
        view_func=lambda page=item: render_industry_page(page),
    )


def render_legal_page(page):
    return render_template(
        "legal-page.html",
        title=f"{page['title']} | Barbarossoft",
        description=page["description"],
        canonical=site_url(page["path"]),
        page=page,
    )


for item in LEGAL_PAGES:
    app.add_url_rule(
        item["path"],
        endpoint=f"legal_{item['slug']}",
        view_func=lambda page=item: render_legal_page(page),
    )


@app.route("/fastlisting-privacy")
def fastlisting_privacy():
    return render_template("fastlisting-privacy.html")


@app.route("/services")
def legacy_services():
    return redirect("/hizmetler", code=301)


@app.route("/projects")
def legacy_projects():
    return redirect("/projeler", code=301)


@app.route("/about")
def legacy_about():
    return redirect("/hakkimizda", code=301)


@app.route("/contact")
def legacy_contact():
    return redirect("/iletisim", code=301)


@app.errorhandler(404)
def not_found(error):
    return (
        render_template(
            "404.html",
            title="Sayfa Bulunamadı | Barbarossoft",
            description="Aradığınız sayfa bulunamadı. Barbarossoft hizmetlerini ve projelerini inceleyebilirsiniz.",
            canonical=site_url(request.path),
        ),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
