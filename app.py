from flask import Flask, render_template

app = Flask(__name__)

# --- ANA SAYFA ROTASI ---
@app.route("/", methods=["GET"])
def ana_sayfa():
    
    # 1. PROJELER VERİSİ (HTML'e gönderilecek)
    projeler = [
        {
            "isim": "Seferoğlu Nakliyat",
            "kategori": "Kurumsal Web Sitesi",
            "aciklama": "Kayseri evden eve nakliyat firması için mobil uyumlu, hızlı ve SEO altyapılı kurumsal tanıtım sitesi.",
            "link": "https://kayseriseferoğluevdenevenakliyat.com.tr",
            "resim": "/static/seferoglu.png"
        },
        {
            "isim": "Doğtek Mühendislik",
            "kategori": "Mühendislik & Proje",
            "aciklama": "Mühendislik firması için kurumsal kimlik çalışması ve hizmet tanıtım web sitesi.",
            "link": "https://dogtekdogalgazmuhendislik.com/", 
            "resim": "/static/dogutek.png"
        },
        {
            "isim": "BarbarosSoft",
            "kategori": "Yazılım Ajansı",
            "aciklama": "Tamamen Python ve Flask kullanılarak geliştirilmiş, modern yazılım ajansı projesi.",
            "link": "#",
            "resim": "https://images.unsplash.com/photo-1555099962-4199c345e5dd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
        }
    ]

    # 2. YORUMLAR VERİSİ (HTML'e gönderilecek)
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
    
    # HTML dosyasını bu verilerle birlikte aç
    return render_template("index.html", projeler=projeler, yorumlar=yorumlar)

# Vercel'in uygulamayı tanıması için gerekli satır
app = app

if __name__ == "__main__":
    app.run(debug=True)