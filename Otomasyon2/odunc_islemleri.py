from veri_deposu import baglanti_olustur
from datetime import datetime, timedelta
import sqlite3

def odunc_ver(kitap_id, uye_id, kac_gun=14):
    conn = baglanti_olustur()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT ad, durum FROM kitaplar WHERE id = ?", (kitap_id,))
        kitap = cursor.fetchone()
        
        if not kitap:
            print("Hata: Kitap bulunamadı!")
            return False
            
        if kitap[1] != "rafta":
            print(f"Hata: '{kitap[0]}' kitabı zaten ödünçte!")
            return False
     
        alis_tarihi = datetime.now().strftime("%d.%m.%Y %H:%M")
        iade_tarihi = (datetime.now() + timedelta(days=kac_gun)).strftime("%d.%m.%Y")
        
        cursor.execute("""
        INSERT INTO odunc_kayitlari (kitap_id, uye_id, alinma_tarihi, son_teslim_tarihi)
        VALUES (?, ?, ?, ?)
        """, (kitap_id, uye_id, alis_tarihi, iade_tarihi))
      
        cursor.execute("UPDATE kitaplar SET durum = 'odunc' WHERE id = ?", (kitap_id,))
        
        conn.commit()
        return True
        
    except sqlite3.Error as hata:
        print(f"Ödünç verme hatası: {hata}")
        return False
    finally:
        conn.close()

def iade_et(odunc_id): 
    conn = baglanti_olustur()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
  
        cursor.execute("SELECT kitap_id FROM odunc_kayitlari WHERE id = ?", (odunc_id,))
        sonuc = cursor.fetchone()
        
        if not sonuc:
            print("Hata: Ödünç kaydı bulunamadı!")
            return False
            
        kitap_id = sonuc[0]
        cursor.execute("UPDATE kitaplar SET durum = 'rafta' WHERE id = ?", (kitap_id,))

        cursor.execute("UPDATE odunc_kayitlari SET iade_edildi_mi = 1 WHERE id = ?", (odunc_id,))
        
        conn.commit()
        return True
        
    except sqlite3.Error as hata:
        print(f"İade hatası: {hata}")
        return False
    finally:
        conn.close()

def aktif_odunc_kayitlari():
    conn = baglanti_olustur()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT o.id, k.ad, u.isim || ' ' || u.soyisim, o.alinma_tarihi, o.son_teslim_tarihi
        FROM odunc_kayitlari o
        JOIN kitaplar k ON o.kitap_id = k.id
        JOIN uyeler u ON o.uye_id = u.id
        WHERE o.iade_edildi_mi = 0
        """)
        return cursor.fetchall()
    except sqlite3.Error as hata:
        print(f"Aktif ödünç listeleme hatası: {hata}")
        return []
    finally:
        conn.close()