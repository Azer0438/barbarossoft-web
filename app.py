from flask import Flask, render_template, send_from_directory, request
import os

app = Flask(__name__, static_folder='static')

@app.route('/sitemap.xml')
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# --- ANA SAYFA ROTASI ---
@app.route("/", methods=["GET"])
def ana_sayfa():
    
    # 1. PROJELER VERİSİ
    projeler = [
        {
            "isim": "AZR Evden Eve Nakliyat",
            "kategori": "Nakliyat & Yerel SEO",
            "aciklama": "Kayseri evden eve nakliyat firması için hızlı, mobil uyumlu, yerel SEO odaklı ve teklif dönüşümü güçlü kurumsal web sitesi.",
            "link": "https://www.azrevdenevenakliyat.com.tr/",
            "resim": "/static/azr-logo.webp"
        },
        {
            "isim": "Seferoğlu Nakliyat",
            "kategori": "Kurumsal Web Sitesi",
            "aciklama": "Kayseri evden eve nakliyat firması için mobil uyumlu, hızlı ve SEO altyapılı kurumsal tanıtım sitesi.",
            "link": "https://kayseriseferoğluevdenevenakliyat.com.tr",
            "resim": "/static/seferoglu.png"
        },
        {
            "isim": "Doğtek Doğalgaz ve Mühendislik",
            "kategori": "Kurumsal Web Sitesi",
            "aciklama": "Doğalgaz ve mühendislik hizmetleri için hazırlanan mobil uyumlu kurumsal web sitesi.",
            "link": "/projeler/dogtek-dogalgaz-kurumsal-web-sitesi",
            "resim": "/static/dogutek.png",
            "internal": True
        },
        {
            "isim": "BarbarosSoft",
            "kategori": "Yazılım Ajansı",
            "aciklama": "Tamamen Python ve Flask kullanılarak geliştirilmiş, modern yazılım ajansı projesi.",
            "link": "#",
            "resim": "https://images.unsplash.com/photo-1555099962-4199c345e5dd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
        }
    ]

    # 2. YORUMLAR VERİSİ
    yorumlar = [
        {
            "isim": "Emrah Taşdemir",
            "firma": "Seferoğlu Nakliyat",
            "yorum": "BarbarosSoft sayesinde Google'da ilk sayfaya çıktık. İşlerimizde %40 artış oldu, kesinlikle tavsiye ederim.",
            "puan": 5
        },
        {
            "isim": "Vefacan Önal",
            "firma": "Doğtek Doğalgaz Mühendislik",
            "yorum": "Kurumsal kimliğimizi çok iyi yansıtan, hızlı ve şık bir site oldu. Eline sağlık.",
            "puan": 5
        },
        {
            "isim": "Zeynep Yalın",
            "firma": "Kayseri Butik",
            "yorum": "E-ticaret sitemiz sorunsuz çalışıyor. Teknik destek konusunda her zaman ulaşılabilirler.",
            "puan": 5
        },
        {
            "isim": "Hüseyin Yılmaz",
            "firma": "Yılmaz Yapı",
            "yorum": "Kısa sürede profesyonel bir iş çıkardılar. Fiyat/Performans olarak Kayseri'nin en iyisi.",
            "puan": 5
        }
    ]

    return render_template("index.html", projeler=projeler, yorumlar=yorumlar)

@app.route('/projeler/dogtek-dogalgaz-kurumsal-web-sitesi', methods=["GET"])
def dogtek_proje_detay():
    return render_template("project-dogtek.html")

# --- PINTEREST GİZLİLİK POLİTİKASI ROTASI ---
@app.route('/fastlisting-privacy', methods=["GET"])
def fastlisting_privacy():
    return render_template("fastlisting-privacy.html")

# Vercel uyumluluğu için
app = app

if __name__ == "__main__":
    app.run(debug=True)
