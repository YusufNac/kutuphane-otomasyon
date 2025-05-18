import tkinter as tk
from tkinter import ttk, messagebox
from kitap_islemleri import *
from uye_islemleri import *
from odunc_islemleri import *
from PIL import Image, ImageTk  

def set_window_icon(window):
    """Tüm pencerelere logo ikonunu uygular"""
    try:
        img = Image.open('logo.png').resize((32,32), Image.LANCZOS)
        icon = ImageTk.PhotoImage(img)
        window.tk.call('wm', 'iconphoto', window._w, icon)
        window._iconref = icon  
    except Exception as e:
        print("Icon yüklenemedi:", e)

pencere = tk.Tk()
pencere.title("Kütüphanem")
pencere.geometry("800x600")

notebook = ttk.Notebook(pencere)
notebook.pack(fill="both", expand=True)

kitap_sekmesi = ttk.Frame(notebook)
notebook.add(kitap_sekmesi, text="Kitaplar")

def kitap_ekle_penceresi():
    def kaydet():
        if kitap_ekle(ent_kitap_adi.get(), ent_yazar.get(), ent_barkod.get(), ent_raf.get()):
            messagebox.showinfo("Başarılı", "Kitap eklendi!")
            pencere_kapat.destroy()
        else:
            messagebox.showerror("Hata", "Kitap eklenemedi!")
    
    pencere_kapat = tk.Toplevel(pencere)
    set_window_icon(pencere_kapat) 
    pencere_kapat.title("Yeni Kitap Ekle")
    
    tk.Label(pencere_kapat, text="Kitap Adı:").grid(row=0, column=0, padx=5, pady=5)
    ent_kitap_adi = tk.Entry(pencere_kapat, width=30)
    ent_kitap_adi.grid(row=0, column=1)
    
    tk.Label(pencere_kapat, text="Yazar:").grid(row=1, column=0)
    ent_yazar = tk.Entry(pencere_kapat, width=30)
    ent_yazar.grid(row=1, column=1)
    
    tk.Label(pencere_kapat, text="Barkod:").grid(row=2, column=0)
    ent_barkod = tk.Entry(pencere_kapat, width=30)
    ent_barkod.grid(row=2, column=1)
    
    tk.Label(pencere_kapat, text="Raf No:").grid(row=3, column=0)
    ent_raf = tk.Entry(pencere_kapat, width=30)
    ent_raf.grid(row=3, column=1)
    
    tk.Button(pencere_kapat, text="Kaydet", command=kaydet).grid(row=4, columnspan=2, pady=10)

def kitap_listele():
    liste_penceresi = tk.Toplevel(pencere)
    set_window_icon(liste_penceresi)
    liste_penceresi.title("Kitap Listesi")
    
    tablo = ttk.Treeview(liste_penceresi, 
                        columns=("ID", "Kitap Adı", "Yazar", "Barkod", "Raf No", "Durum"), 
                        show="headings")
    
    tablo.heading("ID", text="ID")
    tablo.heading("Kitap Adı", text="Kitap Adı")
    tablo.heading("Yazar", text="Yazar")
    tablo.heading("Barkod", text="Barkod")
    tablo.heading("Raf No", text="Raf No")
    tablo.heading("Durum", text="Durum")
    
    tablo.column("ID", width=50)
    tablo.column("Kitap Adı", width=200)
    tablo.column("Yazar", width=150)
    tablo.column("Barkod", width=120)
    tablo.column("Raf No", width=80)
    tablo.column("Durum", width=80)

    for kitap in kitaplari_listele():
        tablo.insert("", tk.END, values=(
            kitap[0],  # ID
            kitap[1],  # Kitap Adı
            kitap[2],  # Yazar
            kitap[3],  # Barkod
            kitap[4],  # Raf No
            kitap[5]   # Durum
        ))
    
    tablo.pack(fill="both", expand=True)

def kitap_ara_penceresi():
    def ara():
        sonuclar = kitaplari_listele(ent_arama.get())
        liste.delete(0, tk.END)
        
        if not sonuclar:
            liste.insert(tk.END, "Sonuç bulunamadı!")
        else:
            for kitap in sonuclar:
                liste.insert(tk.END, f"{kitap[1]} - {kitap[2]} ({kitap[5]})")
    
    pencere_ara = tk.Toplevel(pencere)
    set_window_icon(pencere_ara) 
    pencere_ara.title("Kitap Ara")
    
    tk.Label(pencere_ara, text="Aranacak Kelime:").pack(pady=5)
    ent_arama = tk.Entry(pencere_ara, width=40)
    ent_arama.pack()
    
    tk.Button(pencere_ara, text="Ara", command=ara).pack(pady=5)
    
    liste = tk.Listbox(pencere_ara, width=60, height=15)
    liste.pack(pady=10)

tk.Button(kitap_sekmesi, text="Yeni Kitap Ekle", command=kitap_ekle_penceresi).pack(pady=10)
tk.Button(kitap_sekmesi, text="Tüm Kitapları Listele", command=kitap_listele).pack(pady=10)
tk.Button(kitap_sekmesi, text="Kitap Ara", command=kitap_ara_penceresi).pack(pady=10)

uye_sekmesi = ttk.Frame(notebook)
notebook.add(uye_sekmesi, text="Üyeler")

def uye_ekle_penceresi():
    def kaydet():
        if uye_ekle(ent_isim.get(), ent_soyisim.get(), ent_telefon.get(), ent_eposta.get()):
            messagebox.showinfo("Başarılı", "Üye eklendi!")
            pencere_kapat.destroy()
        else:
            messagebox.showerror("Hata", "Üye eklenemedi! E-posta zaten kayıtlı olabilir.")
    
    pencere_kapat = tk.Toplevel(pencere)
    set_window_icon(pencere_kapat) 
    pencere_kapat.title("Yeni Üye Ekle")
    
    tk.Label(pencere_kapat, text="İsim:").grid(row=0, column=0, padx=5, pady=5)
    ent_isim = tk.Entry(pencere_kapat, width=30)
    ent_isim.grid(row=0, column=1)
    
    tk.Label(pencere_kapat, text="Soyisim:").grid(row=1, column=0)
    ent_soyisim = tk.Entry(pencere_kapat, width=30)
    ent_soyisim.grid(row=1, column=1)
    
    tk.Label(pencere_kapat, text="Telefon:").grid(row=2, column=0)
    ent_telefon = tk.Entry(pencere_kapat, width=30)
    ent_telefon.grid(row=2, column=1)
    
    tk.Label(pencere_kapat, text="E-posta:").grid(row=3, column=0)
    ent_eposta = tk.Entry(pencere_kapat, width=30)
    ent_eposta.grid(row=3, column=1)
    
    tk.Button(pencere_kapat, text="Kaydet", command=kaydet).grid(row=4, columnspan=2, pady=10)

def uye_listele():
    liste_penceresi = tk.Toplevel(pencere)
    set_window_icon(liste_penceresi) 
    liste_penceresi.title("Üye Listesi")
    
    tablo = ttk.Treeview(liste_penceresi, 
                        columns=("ID", "İsim", "Soyisim", "Telefon", "E-posta"), 
                        show="headings")
    
    tablo.heading("ID", text="ID")
    tablo.heading("İsim", text="İsim")
    tablo.heading("Soyisim", text="Soyisim")
    tablo.heading("Telefon", text="Telefon")
    tablo.heading("E-posta", text="E-posta") 
    
    tablo.column("ID", width=50)
    tablo.column("İsim", width=120)
    tablo.column("Soyisim", width=120)
    tablo.column("Telefon", width=100)
    tablo.column("E-posta", width=180)  

    for uye in uyeleri_listele():
        tablo.insert("", tk.END, values=uye)

    scrollbar = ttk.Scrollbar(liste_penceresi, orient="vertical", command=tablo.yview)
    tablo.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tablo.pack(fill="both", expand=True)

tk.Button(uye_sekmesi, text="Yeni Üye Ekle", command=uye_ekle_penceresi).pack(pady=10)
tk.Button(uye_sekmesi, text="Tüm Üyeleri Listele", command=uye_listele).pack(pady=10)

odunc_sekmesi = ttk.Frame(notebook)
notebook.add(odunc_sekmesi, text="Ödünç İşlemleri")

def odunc_ver_penceresi():
    def odunc_kaydet():
        if odunc_ver(int(ent_kitap_id.get()), int(ent_uye_id.get())):
            messagebox.showinfo("Başarılı", "Kitap ödünç verildi!")
            pencere_kapat.destroy()
        else:
            messagebox.showerror("Hata", "Kitap ödünç verilemedi! Kitap zaten ödünçte olabilir.")
    
    pencere_kapat = tk.Toplevel(pencere)
    set_window_icon(pencere_kapat)
    pencere_kapat.title("Kitap Ödünç Ver")
    
    tk.Label(pencere_kapat, text="Kitap ID:").grid(row=0, column=0, padx=5, pady=5)
    ent_kitap_id = tk.Entry(pencere_kapat, width=30)
    ent_kitap_id.grid(row=0, column=1)
    
    tk.Label(pencere_kapat, text="Üye ID:").grid(row=1, column=0)
    ent_uye_id = tk.Entry(pencere_kapat, width=30)
    ent_uye_id.grid(row=1, column=1)
    
    tk.Button(pencere_kapat, text="Ödünç Ver", command=odunc_kaydet).grid(row=2, columnspan=2, pady=10)

def iade_al_penceresi():
    def iade_kaydet():
        try:
            if iade_et(int(ent_odunc_id.get())):  
                messagebox.showinfo("Başarılı", "Kitap iade edildi!")
                pencere_kapat.destroy()
            else:
                messagebox.showerror("Hata", "İade işlemi başarısız! Geçersiz ID olabilir.")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")
    
    pencere_kapat = tk.Toplevel(pencere)
    set_window_icon(pencere_kapat)
    pencere_kapat.title("Kitap İade Al")
    
    tk.Label(pencere_kapat, text="Ödünç Kayıt ID:").grid(row=0, column=0, padx=5, pady=5)
    ent_odunc_id = tk.Entry(pencere_kapat, width=30)
    ent_odunc_id.grid(row=0, column=1)
    
    tk.Button(pencere_kapat, text="İade Al", command=iade_kaydet).grid(row=1, columnspan=2, pady=10)

def odunc_listele():
    try:
        kayitlar = aktif_odunc_kayitlari()
        if not kayitlar:
            messagebox.showinfo("Bilgi", "Aktif ödünç kaydı bulunamadı")
            return
            
        liste_penceresi = tk.Toplevel(pencere)
        set_window_icon(liste_penceresi)  
        liste_penceresi.title("Aktif Ödünçler")
        liste_penceresi.geometry("800x400")
        
        tablo = ttk.Treeview(liste_penceresi, 
                           columns=("ID", "Kitap", "Üye", "Alınma Tarihi", "Son Tarih"), 
                           show="headings")

        tablo.heading("ID", text="Kayıt ID")
        tablo.heading("Kitap", text="Kitap Adı")
        tablo.heading("Üye", text="Üye")
        tablo.heading("Alınma Tarihi", text="Alınma Tarihi")
        tablo.heading("Son Tarih", text="Son Teslim Tarihi")

        tablo.column("ID", width=50)
        tablo.column("Kitap", width=200)
        tablo.column("Üye", width=150)
        tablo.column("Alınma Tarihi", width=150)
        tablo.column("Son Tarih", width=150)
        
        for kayit in kayitlar:
            tablo.insert("", tk.END, values=kayit)
        
        tablo.pack(fill="both", expand=True)
        
    except Exception as hata:
        messagebox.showerror("Hata", f"Listeleme sırasında hata oluştu: {hata}")

tk.Button(odunc_sekmesi, text="Kitap Ödünç Ver", command=odunc_ver_penceresi).pack(pady=10)
tk.Button(odunc_sekmesi, text="Kitap İade Al", command=iade_al_penceresi).pack(pady=10)
tk.Button(odunc_sekmesi, text="Aktif Ödünçleri Listele", command=odunc_listele).pack(pady=10)

try:
    pencere.iconphoto(False, tk.PhotoImage(file='logo.png'))
except Exception as e:
    print("Icon yüklenemedi:", e)

try:
    logo_image = tk.PhotoImage(file='logo.png')

    logo_image = logo_image.subsample(2) 
    
    logo_label = tk.Label(pencere, image=logo_image)
    logo_label.image = logo_image  
    logo_label.pack(pady=10)
    
except Exception as e:
    print("Logo yüklenemedi:", e)
    logo_label = tk.Label(pencere, text="Kütüphane Otomasyonu", font=('Arial', 16, 'bold'))
    logo_label.pack(pady=20)

pencere.mainloop()