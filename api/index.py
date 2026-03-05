from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

URL_SCRIPT = 'https://script.google.com/macros/s/AKfycbxswO_yhj0fj0iJ1k-kdVE_hhRiKYqEMJWy_kvV_VZxiolZiK86hZrXXGH3ZicwZGDO/exec'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-peserta')
def get_peserta():
    r = requests.get(URL_SCRIPT)
    return jsonify(r.json())

@app.route('/pilih-pemenang', methods=['POST'])
def pilih_pemenang():
    nama = request.json.get('nama')
    requests.post(URL_SCRIPT, json={'nama': nama})
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)