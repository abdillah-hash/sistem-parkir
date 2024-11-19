from flask import Flask, render_template, request, redirect, url_for
import datetime

# Object-Oriented Programming: Kelas untuk tempat parkir
class TempatParkir:
    def __init__(self, nomor, tersedia=True):
        self.nomor = nomor  # Variable dengan tipe data integer
        self.tersedia = tersedia  # Variable boolean untuk status tempat parkir
    
    # Method untuk menandai tempat sebagai terisi
    def isi(self):
        self.tersedia = False
    
    # Method untuk menandai tempat sebagai kosong
    def kosongkan(self):
        self.tersedia = True

# Membuat array (list) tempat parkir
tempat_parkir = [TempatParkir(i) for i in range(1, 6)]  # Perulangan untuk membuat 5 tempat parkir

# Flask app
app = Flask(__name__)

# Function untuk memilih tempat parkir otomatis
def pilih_tempat_parkir():
    for tempat in tempat_parkir:  # Perulangan untuk mencari tempat yang tersedia
        if tempat.tersedia:  # Pengkondisian: Jika tersedia, gunakan tempat tersebut
            tempat.isi()
            return tempat
    return None  # Jika semua tempat penuh

@app.route('/')
def index():
    return render_template('index.html', tempat_parkir=tempat_parkir)

@app.route('/parkir', methods=['POST'])
def parkir_mobil():
    tempat = pilih_tempat_parkir()
    if tempat:  # Pengkondisian: Jika tempat tersedia
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tiket = f"""
        =======================
               Tiket Parkir
        =======================
        Waktu: {waktu}
        Nomor Tempat: {tempat.nomor}
        =======================
        """
        return render_template('tiket.html', nomor_tempat=tempat.nomor, waktu=waktu, tiket=tiket)
    else:
        return render_template('penuh.html')

@app.route('/keluar/<int:nomor>')
def keluar(nomor):
    for tempat in tempat_parkir:  # Perulangan untuk menemukan tempat parkir berdasarkan nomor
        if tempat.nomor == nomor:
            tempat.kosongkan()  # Method untuk mengosongkan tempat parkir
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
