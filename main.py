import sys 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from GUI import *


uygulama = QApplication(sys.argv)
pencere = QMainWindow() 
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

# Not = Veri tabanı işlemleri


import mysql.connector

baglanti = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345",
  database="mytoqt")

cursor = baglanti.cursor()
baglanti.commit()

def kayit_ekle():

    UrunKodu = ui.lneCode.text()
    UrunAdi = ui.lneName.text()
    BirimFiyati = int(ui.lnePreis.text())
    StokMiktari = int(ui.lneLager.text())
    UrunAciklamasi = ui.lneBschreibung.text()
    Marka = ui.cmbMarke.currentText()
    Kategori = ui.cmbKategorie.currentText()

    try:
        ekle = "INSERT INTO produkt (produktcode, produktname, stückpreis, lagermenge, beschreibung, marke, kategorie) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(ekle, (UrunKodu, UrunAdi, BirimFiyati, StokMiktari, UrunAciklamasi, Marka, Kategori))
        baglanti.commit()
        kayit_listele()
        ui.statusbar.showMessage("Registrierung erfolgreich", 10000)
    except Exception as error:
        ui.statusbar.showMessage("Fehler beim Hinzufügen eines Datensatzes ==="+str(error))


def kayit_listele():
    ui.tblGros.clear()
    ui.tblGros.setHorizontalHeaderLabels(("Code", "Name", "Stückpreis", "Lagermenge", "Beschreibung", "Marke", "Kategorie"))
    ui.tblGros.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    sorgu = "SELECT * FROM produkt"
    cursor.execute(sorgu)


    for IndexRow, rows in enumerate(cursor):
        for IndexColumn, columns in enumerate(rows):
            ui.tblGros.setItem(IndexRow, IndexColumn, QTableWidgetItem(str(columns)))


kayit_listele() # bu sayede program acilir acilmaz bütün satirlar listelenecektir.


def kategoriye_gore_listele():
    listelenecek_kategori = ui.cmbNachKategorie.currentText()

    sorgu = "select * from produkt where kategorie = %s"
    cursor.execute(sorgu,(listelenecek_kategori,))
    ui.tblGros.clear()

    for IndexRow, rows in enumerate(cursor):
        for IndexColumn, columns in enumerate(rows):
            ui.tblGros.setItem(IndexRow, IndexColumn, QTableWidgetItem(str(columns)))


def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere, "Löschungsbestätigung", "Sind Sie sicher, dass Sie es löschen wollen%s", QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        secilen_satir = ui.tblGros.selectedItems()
        silinecek_satir = secilen_satir[0].text()

        sorgu = " delete from produkt where produktcode = %s"
        try:
            cursor.execute(sorgu,(silinecek_satir,))
            baglanti.commit()
            ui.statusbar.showMessage("Zeile erfolgreich gelöscht")
            kayit_listele()

        except Exception as error:
            ui.statusbar.showMessage("Fehler beim Löschen einer Zeile === "+str(error))
    
    else:
        ui.statusbar.showMessage("Löschung Storniert")


def kayit_guncelle():
    guncelle_mesaj = QMessageBox.question(pencere, "Aktualisierungsbestätigung","Sind Sie sicher, dass Sie diese Zeile aktualisieren wollen?",QMessageBox.Yes | QMessageBox.No)

    UrunKodu = ui.lneCode.text()
    UrunAdi = ui.lneName.text()
    BirimFiyati = ui.lnePreis.text()
    StokMiktari = ui.lneLager.text()
    UrunAciklamasi = ui.lneBschreibung.text()
    Marka = ui.cmbMarke.currentText()
    Kategori = ui.cmbKategorie.currentText()


    if guncelle_mesaj == QMessageBox.Yes:
        try:
            if UrunAdi != "" and BirimFiyati != "" and StokMiktari != "" and UrunAciklamasi != "" and Marka != "" :
                sorgu =("update produkt set produktname = %s, stückpreis = %s, lagermenge = %s, beschreibung = %s, marke = %s, kategorie = %s where produktcode = %s")
                cursor.execute(sorgu,(UrunAdi, BirimFiyati, StokMiktari, UrunAciklamasi, Marka, Kategori, UrunKodu,))


            else:
                sorgu = ("update produkt set produktname = %s, stückpreis = %s, lagermenge = %s, beschreibung = %s, marke = %s, kategorie = %s where produktcode = %s")
                cursor.execute(sorgu,(UrunAdi, BirimFiyati, StokMiktari, UrunAciklamasi, Marka, Kategori, UrunKodu,))
            kayit_listele()
            ui.statusbar.showMessage("Registrierung erfolgreich aktualisiert")
        except Exception as error:
            ui.statusbar.showMessage("Fehler bei der Zeilenaktualisierung === "+str(error))
    else:
        ui.statusbar.showMessage("Aktualisierung abgebrochen")




# butonlar
ui.btnHinzufgen.clicked.connect(kayit_ekle)
ui.btnProduktListe.clicked.connect(kayit_listele)
ui.btnNachKategorie.clicked.connect(kategoriye_gore_listele)
ui.btnLoschen.clicked.connect(kayit_sil)
ui.btnAktual.clicked.connect(kayit_guncelle)


sys.exit(uygulama.exec_())









