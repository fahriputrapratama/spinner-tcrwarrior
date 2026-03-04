from flask import Flask, render_template, jsonify
from vercel_kv import KV
import random

# Inisialisasi Flask (template folder diarahkan ke luar folder api)
app = Flask(__name__, template_folder='../templates')
kv = KV()

DB_KEY = "daftar_peserta"

def get_or_init_names():
    # Ambil data dari Redis
    names = kv.get(DB_KEY)
    if names is None:
        # Jika DB kosong (pertama kali run), isi 500 nama
        names = [f"Peserta {i}" for i in range(1, 501)]
        kv.set(DB_KEY, names)
    return names

@app.route('/')
def index():
    names = get_or_init_names()
    return render_template('index.html', total=len(names))

@app.route('/kocok', methods=['POST'])
def kocok():
    names = kv.get(DB_KEY) or []
    
    if not names:
        return jsonify({"error": "Daftar peserta sudah habis!"}), 400

    # Pilih pemenang secara acak
    pemenang = random.choice(names)
    
    # Hapus pemenang dari daftar
    names.remove(pemenang)
    
    # Simpan kembali daftar terbaru ke Redis
    kv.set(DB_KEY, names)

    return jsonify({
        "pemenang": pemenang,
        "sisa_jumlah": len(names)
    })

@app.route('/reset-ulang')
def reset():
    # Fitur untuk mengembalikan ke 500 nama
    names = [f"Peserta {i}" for i in range(1, 501)]
    kv.set(DB_KEY, names)
    return "Data telah direset ke 500 nama."

# Diperlukan untuk Vercel
app = app