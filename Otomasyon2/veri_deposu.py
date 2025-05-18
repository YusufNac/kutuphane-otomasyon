import sqlite3
from datetime import datetime

def baglanti_olustur():
    try:
        return sqlite3.connect("kutuphane_verileri.db")
    except sqlite3.Error as hata:
        print("Veritabanı bağlantı hatası:", hata)
        return None

def tablolari_hazirla():
    conn = baglanti_olustur()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS kitaplar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL,
            yazar TEXT NOT NULL,
            barkod TEXT UNIQUE,
            raf TEXT,
            durum TEXT DEFAULT 'rafta',
            eklenme_zamani TEXT
        )
        """)
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS uyeler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            soyisim TEXT NOT NULL,
            telefon TEXT,
            eposta TEXT UNIQUE,
            kayit_tarihi TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS odunc_kayitlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kitap_id INTEGER,
            uye_id INTEGER,
            alinma_tarihi TEXT,
            son_teslim_tarihi TEXT,
            iade_edildi_mi INTEGER DEFAULT 0,
            FOREIGN KEY (kitap_id) REFERENCES kitaplar (id),
            FOREIGN KEY (uye_id) REFERENCES uyeler (id)
        )
        """)

        conn.commit()
        return True
    except sqlite3.Error as hata:
        print("Tablo oluşturma hatası:", hata)
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if tablolari_hazirla():
        print("Tablolar başarıyla oluşturuldu.")
    else:
        print("Tablolar oluşturulamadı.")
