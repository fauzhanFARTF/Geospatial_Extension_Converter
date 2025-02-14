# Geospatial Extension Converter

## 📌 Pendahuluan
Geospatial Extension Converter adalah alat yang memungkinkan pengguna untuk mengonversi berbagai format data geospasial dengan mudah. Alat ini mendukung konversi antara berbagai format, seperti:
- **GeoJSON → SHP**, **GeoJSON → KML**, dan **GeoJSON → SHP & ZIP**
- **KML → SHP**, **KML → GeoJSON**, **KML → SHP & ZIP**
- **GDB → SHP**, **GDB → SHP & ZIP**, **GDB → GeoJSON**
- **SHP → GeoJSON**, **SHP → KML**

Selain konversi format, aplikasi ini juga menyediakan fitur pemindahan file hasil konversi (serta isi folder input) ke folder storage dengan pengelompokkan berdasarkan ekstensi, sehingga memudahkan pengelolaan data.

## ⚙️ Instalasi

### 1. Persyaratan
Pastikan Anda telah menginstal:
- Python (versi 3.8 ke atas)
- pip

### 2. Instalasi Package
Jalankan perintah berikut untuk menginstal paket:
```sh
pip install .
```
Atau jika menggunakan virtual environment:
```sh
python -m venv env
# Untuk Linux/Mac:
source env/bin/activate  
# Untuk Windows:
env\Scripts\activate  
pip install .
```

### 3. Instalasi dengan `geo_converter`
Setelah instalasi, Anda dapat menjalankan aplikasi menggunakan:
```sh
geo_converter
```

## 🚀 Penggunaan
Setelah menjalankan `geo_converter`, Anda akan melihat menu interaktif yang memungkinkan Anda untuk:
1. Memilih jenis konversi format data geospasial (menu bertingkat).
2. Menempatkan file input pada folder `data/input/`.
3. Melihat hasil konversi pada folder `data/output/`.
4. Memindahkan file dan folder (baik dari `data/input/` maupun `data/output/`) ke folder `data/storage/` dengan pengelompokan berdasarkan ekstensi (misalnya, SHP, KML, GeoJSON, GDB, ZIP).

## 📂 Struktur Folder
```
geospatial_extension_converter/
|—— data/
|   ├—— input/                # Folder untuk file input
|   ├—— output/               # Folder untuk hasil konversi
|   ├—— storage/              # Folder penyimpanan file hasil konversi yang telah diorganisir
|       ├—— geojson/
|       ├—— shp/
|       ├—— kml/
|       ├—— gdb/
|       ├—— zip/
|—— logs/                     # Folder untuk menyimpan log proses konversi (logs/conversion.log)
|—— src/
|   ├—— converters/           # Modul konversi format geospasial
|   |   ├—— geojson_to_shp.py
|   |   ├—— geojson_to_shp_zip.py
|   |   ├—— geojson_to_kml.py
|   |   ├—— kml_to_shp.py     
|   |   ├—— kml_to_shp_zip.py     
|   |   ├—— kml_to_geojson.py
|   |   ├—— gdb_to_shp.py     
|   |   ├—— gdb_to_shp_zip.py     
|   |   ├—— gdb_to_geojson.py     
|   |   ├—— shp_to_geojson.py
|   |   ├—— shp_to_kml.py     
|   ├—— utils/                # Modul utilitas (file handling, logging, organizer, dll.)
|       ├—— file_handler.py
|       ├—— logger.py
|       ├—— organizer.py
|—— config/
|   ├—— settings.py           # Konfigurasi aplikasi
|—— tests/                    # Unit test untuk modul konversi
|—— docs/                     # Dokumentasi aplikasi
|—— requirements.txt          # Daftar dependensi Python
|—— .gitignore                # File yang tidak perlu di-tracking oleh Git
|—— src/main.py               # Skrip utama untuk menjalankan aplikasi
```

## 📝 Log Konversi
Semua log proses konversi dicatat di:
```
logs/conversion.log
```
Log mencatat informasi seperti:
- Nama file yang dikonversi
- Waktu mulai dan selesai konversi
- Lama waktu proses
- Status (SUKSES, GAGAL, ERROR) beserta pesan detail jika terjadi kesalahan

## ❌ Menghapus Data
Terdapat opsi untuk menghapus hasil konversi atau seluruh data input dan output:
```sh
geo_converter --clear-output   # Menghapus hanya folder output
geo_converter --clear-all      # Menghapus semua data pada folder input & output
```

## 📆 Pemindahan ke Storage
Anda juga dapat memindahkan semua file dan folder (baik dari `data/input` maupun `data/output`) ke dalam folder `data/storage`. File akan dipindahkan berdasarkan ekstensi (misalnya, file SHP ke folder `shp`, file ZIP ke folder `zip`, dan folder .gdb ke folder `gdb`) serta mempertahankan struktur relatif aslinya.

## 🛠 Pengembangan & Kontribusi
Jika Anda ingin mengembangkan atau memberikan kontribusi:
- Silakan fork repository ini.
- Buat branch fitur/bugfix.
- Lakukan commit dan push.
- Buat pull request ke branch utama.

Happy coding! 🚀

