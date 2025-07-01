from flask import Flask, render_template, jsonify, request
import os
import logging
from flask_mysqldb import MySQL

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# Menampilkan direktori kerja saat ini dan isi folder templates
print("Current working directory:", os.getcwd())
print("Contents of ./templates:", os.listdir("templates"))

app = Flask(__name__)

# Konfigurasi koneksi ke database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ppk_uas'
mysql = MySQL(app)

# Route halaman utama
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/home")
def root():
    return 'Selamat datang Pembeli di Toko Makmur'

@app.route('/person')
def person():
    return jsonify({'name': 'Ayie', 'address': 'Bogor'})

# Route untuk menangani data pembeli (CRUD)
@app.route('/pembeli', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_pembeli():
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM pembeli")
        column_names = [i[0] for i in cursor.description]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        cursor.close()
        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()
        try:
            nama = data['nama']
            umur = data['umur']
            warna = data.get('warna') or data.get('warnafavorit')
            sql = "INSERT INTO pembeli (nama, umur, warna) VALUES (%s, %s, %s)"
            val = (nama, umur, warna)
            cursor.execute(sql, val)
            mysql.connection.commit()
            return jsonify({'message': 'Data pembeli berhasil ditambahkan!'})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            cursor.close()

    elif request.method == 'PUT':
        data = request.get_json()
        try:
            pembeli_id = data['pembeli_id']
            nama = data['nama']
            umur = data['umur']
            warna = data.get('warna') or data.get('warnafavorit')
            sql = "UPDATE pembeli SET nama=%s, umur=%s, warna=%s WHERE pembeli_id=%s"
            val = (nama, umur, warna, pembeli_id)
            cursor.execute(sql, val)
            mysql.connection.commit()
            return jsonify({'message': 'Data pembeli berhasil diperbarui!'})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            cursor.close()

    elif request.method == 'DELETE':
        data = request.get_json()
        try:
            pembeli_id = data['pembeli_id']
            sql = "DELETE FROM pembeli WHERE pembeli_id=%s"
            val = (pembeli_id,)
            cursor.execute(sql, val)
            mysql.connection.commit()
            return jsonify({'message': 'Data pembeli berhasil dihapus!'})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            cursor.close()

# Endpoint tambahan: GET pembeli by ID
@app.route('/pembeli/<int:pembeli_id>', methods=['GET'])
def get_pembeli_by_id(pembeli_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT * FROM pembeli WHERE pembeli_id = %s", (pembeli_id,))
        row = cursor.fetchone()
        if row:
            column_names = [i[0] for i in cursor.description]
            data = dict(zip(column_names, row))
            return jsonify(data)
        else:
            return jsonify({'message': 'Pembeli tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)
