from tkinter import *
from tkinter import ttk
import sqlite3


def create_table():
    conn = sqlite3.connect("verıtabanı.cıve.db")
    cursor = conn.cursor()

    # "Eser" tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Eser (
            eserID INTEGER PRIMARY KEY AUTOINCREMENT,
            eserAdi TEXT,
            eserBasim INTEGER,
            eserSayfa TEXT
        )
    ''')

    conn.commit()
    conn.close()


def insert_eser(eserAdi, eserBasim, eserSayfa):
    conn = sqlite3.connect("verıtabanı.cıve.db")
    cursor = conn.cursor()

    # Yeni bir eser ekle
    cursor.execute('''
        INSERT INTO Eser (eserAdi, eserBasim, eserSayfa)
        VALUES (?, ?, ?)
    ''', (eserAdi, eserBasim, eserSayfa))

    conn.commit()
    conn.close()


def update_eser(eserID, eserAdi, eserBasim, eserSayfa):
    conn = sqlite3.connect('verıtabanı.cıve.db')
    cursor = conn.cursor()

    # Eser bilgilerini güncelle
    cursor.execute('''
        UPDATE Eser SET eserAdi=?, eserBasim=?, eserSayfa=?
        WHERE eserID=?
    ''', (eserAdi, eserBasim, eserSayfa, eserID))

    conn.commit()
    conn.close()


def delete_eser(eserID):
    conn = sqlite3.connect("verıtabanı.cıve.db")
    cursor = conn.cursor()

    # Eseri sil
    cursor.execute('''
        DELETE FROM Eser WHERE eserID=?
    ''', (eserID,))

    conn.commit()
    conn.close()


def list_eserler():
    conn = sqlite3.connect("verıtabanı.cıve.db")
    cursor = conn.cursor()

    # Tüm eserleri listele
    cursor.execute("SELECT * FROM Eser")
    eserler = cursor.fetchall()

    conn.close()
    return eserler


class EserApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Katalog: Eserleri Yönet')
        self.master.geometry('800x300')
        self.master.resizable = True
        self.master['bg'] = '#cff8B8B83'

        create_table()

        self.eserTabloCercevesi = ttk.Frame(self.master, padding=25)
        self.eserTabloCercevesi.pack()

        self.eserTablosu = ttk.Treeview(self.eserTabloCercevesi)
        self.populate_table()

        self.eserTablosu['columns'] = ('eserID', 'eserAdi', 'eserBasim', 'eserSayfa')

        self.eserTablosu.column("#0", width=0, stretch=NO)
        self.eserTablosu.column("eserID", anchor=CENTER, width=50)
        self.eserTablosu.column("eserAdi", anchor=CENTER, width=250)
        self.eserTablosu.column("eserBasim", anchor=CENTER, width=75)
        self.eserTablosu.column("eserSayfa", anchor=CENTER, width=250)

        self.eserTablosu.heading("#0", text="", anchor=CENTER)
        self.eserTablosu.heading("eserID", text="Eser ID", anchor=CENTER)
        self.eserTablosu.heading("eserAdi", text="Eser Adı", anchor=CENTER)
        self.eserTablosu.heading("eserBasim", text="Eser Basım", anchor=CENTER)
        self.eserTablosu.heading("eserSayfa", text="Eser Sayfa", anchor=CENTER)

        self.eserTablosu.pack()

        # Ekleme Butonları
        self.label_adi = Label(self.master, text="Eser Adı:")
        self.label_adi.pack()
        self.entry_adi = Entry(self.master)
        self.entry_adi.pack()

        self.label_basim = Label(self.master, text="Eser Basım Yılı:")
        self.label_basim.pack()
        self.entry_basim = Entry(self.master)
        self.entry_basim.pack()

        self.label_url = Label(self.master, text="Eser URL:")
        self.label_url.pack()
        self.entry_url = Entry(self.master)
        self.entry_url.pack()

        self.button_ekle = Button(self.master, text="Eser Ekle", command=self.ekle)
        self.button_ekle.pack()

        # Güncelleme ve Silme Butonları
        self.label_eserID_guncelle = Label(self.master, text="Güncellenecek Eser ID:")
        self.label_eserID_guncelle.pack()
        self.entry_eserID_guncelle = Entry(self.master)
        self.entry_eserID_guncelle.pack()

        self.label_adi_guncelle = Label(self.master, text="Yeni Eser Adı:")
        self.label_adi_guncelle.pack()
        self.entry_adi_guncelle = Entry(self.master)
        self.entry_adi_guncelle.pack()

        self.label_basim_guncelle = Label(self.master, text="Yeni Eser Basım Yılı:")
        self.label_basim_guncelle.pack()
        self.entry_basim_guncelle = Entry(self.master)
        self.entry_basim_guncelle.pack()

        self.label_url_guncelle = Label(self.master, text="Yeni Eser URL:")
        self.label_url_guncelle.pack()
        self.entry_url_guncelle = Entry(self.master)
        self.entry_url_guncelle.pack()

        self.button_guncelle = Button(self.master, text="Eser Güncelle", command=self.guncelle)
        self.button_guncelle.pack()

        self.label_eserID_sil = Label(self.master, text="Silinecek Eser ID:")
        self.label_eserID_sil.pack()
        self.entry_eserID_sil = Entry(self.master)
        self.entry_eserID_sil.pack()

        self.button_sil = Button(self.master, text="Eser Sil", command=self.sil)
        self.button_sil.pack()

        # Listeleme Butonu
        self.button_listele = Button(self.master, text="Tüm Eserleri Listele", command=self.populate_table)
        self.button_listele.pack()

    def ekle(self):
        eserAdi = self.entry_adi.get()
        eserBasim = self.entry_basim.get()
        eserURL = self.entry_url.get()

        insert_eser(eserAdi, eserBasim, eserURL)
        self.populate_table()

        self.entry_adi.delete(0, END)
        self.entry_basim.delete(0, END)
        self.entry_url.delete(0, END)

    def guncelle(self):
        eserID = self.entry_eserID_guncelle.get()
        eserAdi = self.entry_adi_guncelle.get()
        eserBasim = self.entry_basim_guncelle.get()
        eserURL = self.entry_url_guncelle.get()

        update_eser(eserID, eserAdi, eserBasim, eserURL)
        self.populate_table()

        self.entry_eserID_guncelle.delete(0, END)
        self.entry_adi_guncelle.delete(0, END)
        self.entry_basim_guncelle.delete(0, END)
        self.entry_url_guncelle.delete(0, END)

    def sil(self):
        eserID = self.entry_eserID_sil.get()
        delete_eser(eserID)
        self.populate_table()

        self.entry_eserID_sil.delete(0, END)

    def populate_table(self):
        for row in self.eserTablosu.get_children():
            self.eserTablosu.delete(row)

        eserler = list_eserler()
        for index, eser in enumerate(eserler):
            self.eserTablosu.insert(parent='', index='end', iid=index, text='',
                                    values=(eser[0], eser[1], eser[2], eser[3]))


if __name__ == "__main__":
    root = Tk()
    app = EserApp(root)
    root.mainloop()
