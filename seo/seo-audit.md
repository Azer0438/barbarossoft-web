# SEO Audit

Tarih: 2026-07-18
Branch: seo/professional-audit-and-implementation
Domain: https://barbarossoft.com.tr

## Başlangıç Durumu
- Stack: Flask, Jinja template, statik CSS/JS ve statik sitemap/robots dosyaları.
- Taranan URL sayısı: 42.
- Indexlenebilir 200 URL sayısı: 34.
- Redirect olarak izlenen URL sayısı: 7.
- Sitemap URL sayısı: 34.
- Noindex izlenen URL sayısı: 1.
- GA4 ID bulundu: G-N0C5JP85VR. Analytics scripti çerez onayı olmadan yüklenmeyecek şekilde korunuyor.
- Search Console erişimi lokal kod ortamında yok; manuel checklist oluşturuldu.
- Lighthouse/PageSpeed laboratuvar testi bu scriptte çalıştırılmadı; canlı/staging ortamda manuel çalıştırılmalı.

## Kritik Bulgular
- `/kayseri-seo` ve `/kurumsal-web-tasarim` çekirdek SEO mimarisinde eksikti; yeni sayfalar eklendi.
- Ana sayfa, ticari web tasarım niyetini hizmet sayfasıyla karıştırıyordu; marka ve genel ajans niyetine çekildi.
- `/kayseri-seo` ile `/yerel-seo` arasında olası kanibalizasyon vardı; ticari SEO danışmanlığı ve kavramsal/local SEO ayrıştırıldı.
- `fastlisting-privacy` Barbarossoft SEO mimarisiyle ilişkili olmadığı için noindex yapıldı ve sitemap dışına alındı.
- OG locale, robots meta ve sayfa tipine göre OG type merkezi template'e eklendi.

## Teknik Durum
- JSON-LD parse hatası: 0.
- Kırık dahili link uyarısı: 0.
- Eksik alt metin uyarısı: 68. Logo gibi dekoratif görsellerde boş alt kabul edilebilir; gerçek içerik görselleri kontrol edilmelidir.
- Uyarılı sayfa sayısı: 0. Ayrıntı `url-inventory.csv` ve `seo-validation-report.md` içinde.

## Uygulanan Düzeltmeler
- Yeni URL'ler: `/kurumsal-web-tasarim`, `/kayseri-seo`.
- Yeni 301'ler: `/kurumsal-web-sitesi`, `/seo-hizmeti`, `/kayseri-seo-danismanligi`.
- Sitemap güncellendi; noindex sayfa çıkarıldı.
- Hizmet sayfalarına ölçüm/kalite kontrolleri ve ilgili rehber iç linkleri eklendi.
- Proje dış linklerine `outbound_project_click`, blog detaylarına `blog_view` event'i eklendi.
- Service, CreativeWork, BlogPosting, CollectionPage ve Breadcrumb JSON-LD kapsamı genişletildi.

## Veri Uydurmama Notları
- Anahtar kelime hacmi, KD, trafik, organik sonuç, reklam sonucu veya sıralama iddiası yazılmadı.
- Açık adres yayınlanmadı.
- Müşteri yorumu/rating schema eklenmedi.
- Harici SERP, GBP, GSC, GA4 ve backlink işleri manuel TODO olarak belgelendi.