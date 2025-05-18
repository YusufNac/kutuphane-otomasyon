from veri_deposu import baglanti_olustur
from datetime import datetime

def uye_ekle(isim, soyisim, telefon="", eposta=""):
    baglanti = baglanti_olustur()
    if not baglanti:
        print("Veritabanı bağlantı hatası!")
        return False

    try:
        imlec = baglanti.cursor()
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

        imlec.execute("""
        INSERT INTO uyeler (isim, soyisim, telefon, eposta, kayit_tarihi)
        VALUES (?, ?, ?, ?, ?)
        """, (isim, soyisim, telefon, eposta, tarih))

        baglanti.commit()
        print(f"'{isim} {soyisim}' üyesi başarıyla eklendi.")
        return True

    except Exception as hata:
        print(f"Üye ekleme hatası: {hata}")
        return False
    finally:
        baglanti.close()

def uyeleri_listele():
    baglanti = baglanti_olustur()
    if not baglanti:
        print("Veritabanı bağlantı hatası!")
        return []

    try:
        imlec = baglanti.cursor()
        imlec.execute("SELECT id, isim, soyisim, telefon, eposta FROM uyeler")
        return imlec.fetchall()
    except Exception as hata:
        print(f"Üye listeleme hatası: {hata}")
        return []
    finally:
        baglanti.close()
