import sqlite3
from datetime import datetime
from veri_deposu import baglanti_olustur

def kitap_ekle(ad, yazar, barkod=None, raf=None):
    conn = baglanti_olustur()
    if not conn:
        print("Veritabanı bağlantı hatası!")
        return False

    try:
        imlec = conn.cursor()
        tarih = datetime.now().strftime("%d.%m.%Y %H:%M")

        imlec.execute("""
        INSERT INTO kitaplar (ad, yazar, barkod, raf, eklenme_zamani)
        VALUES (?, ?, ?, ?, ?)
        """, (ad, yazar, barkod, raf, tarih))

        conn.commit()
        print(f"'{ad}' kitabı başarıyla eklendi.")
        return True

    except sqlite3.IntegrityError:
        print("Hata: Bu barkod zaten kayıtlı!")
        return False
    except Exception as hata:
        print(f"Beklenmeyen hata: {hata}")
        return False
    finally:
        conn.close()

def kitap_sil(kitap_id):
    conn = baglanti_olustur()
    if not conn:
        return False

    try:
        imlec = conn.cursor()

        imlec.execute("SELECT ad, durum FROM kitaplar WHERE id = ?", (kitap_id,))
        kitap = imlec.fetchone()

        if not kitap:
            print("Hata: Kitap bulunamadı!")
            return False

        if kitap[1] == "odunc":
            print(f"Hata: '{kitap[0]}' kitabı ödünçte, silinemez!")
            return False

        imlec.execute("DELETE FROM kitaplar WHERE id = ?", (kitap_id,))
        conn.commit()
        print(f"'{kitap[0]}' kitabı silindi.")
        return True

    except Exception as hata:
        print(f"Silme hatası: {hata}")
        return False
    finally:
        conn.close()

def kitaplari_listele(filtre=None):
    conn = baglanti_olustur()
    if not conn:
        return []

    try:
        imlec = conn.cursor()

        if filtre:
            imlec.execute("""
            SELECT id, ad, yazar, barkod, raf, durum 
            FROM kitaplar 
            WHERE ad LIKE ? OR yazar LIKE ? OR barkod LIKE ?
            """, (f"%{filtre}%", f"%{filtre}%", f"%{filtre}%"))
        else:
            imlec.execute("SELECT id, ad, yazar, barkod, raf, durum FROM kitaplar")

        return imlec.fetchall()

    except Exception as hata:
        print(f"Listeleme hatası: {hata}")
        return []
    finally:
        conn.close()

def kitap_durum_guncelle(kitap_id, yeni_durum):
    conn = baglanti_olustur()
    if not conn:
        return False

    try:
        imlec = conn.cursor()
        imlec.execute("""
        UPDATE kitaplar 
        SET durum = ? 
        WHERE id = ?
        """, (yeni_durum, kitap_id))

        conn.commit()
        return True

    except Exception as hata:
        print(f"Güncelleme hatası: {hata}")
        return False
    finally:
        conn.close()

def kitap_bilgisi_getir(kitap_id):
    conn = baglanti_olustur()
    if not conn:
        return None

    try:
        imlec = conn.cursor()
        imlec.execute("""
        SELECT id, ad, yazar, barkod, raf, durum, eklenme_zamani 
        FROM kitaplar 
        WHERE id = ?
        """, (kitap_id,))

        return imlec.fetchone()

    except Exception as hata:
        print(f"Bilgi getirme hatası: {hata}")
        return None
    finally:
        conn.close()
