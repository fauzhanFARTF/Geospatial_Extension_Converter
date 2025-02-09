# Geospatial Extension Converter

## 📌 Pendahuluan
Geospatial Extension Converter adalah alat yang memungkinkan pengguna untuk mengonversi berbagai format data geospasial dengan mudah, seperti GeoJSON ke SHP, KML ke SHP, GDB ke SHP, SHP ke GeoJSON, dan SHP ke KML.

## ⚙️ Instalasi

### 1. Persyaratan
Pastikan Anda telah menginstal Python (versi 3.8 ke atas) dan pip.

### 2. Instalasi Package
Jalankan perintah berikut untuk menginstal paket:
```sh
pip install .
```
Atau jika menggunakan virtual environment:
```sh
python -m venv env
source env/bin/activate  # Untuk Linux/Mac
env\Scripts\activate  # Untuk Windows
pip install .
```

### 3. Instalasi dengan `geo_converter`
Setelah instalasi, Anda dapat menjalankan aplikasi dengan perintah berikut:
```sh
geo_converter
```

## 🚀 Penggunaan
Setelah menjalankan `geo_converter`, Anda akan diberikan pilihan menu untuk melakukan konversi format data geospasial.

1. Pilih jenis konversi yang diinginkan.
2. Masukkan file ke dalam folder `data/input/`.
3. File hasil konversi akan disimpan di `data/output/`.

## 📂 Struktur Folder
```
geospatial_extension_converter/
│── data/
│   ├── input/                # Folder untuk file input
│   ├── output/               # Folder untuk hasil konversi
│── logs/                     # Folder untuk menyimpan log proses konversi
│── src/
│   ├── converters/           # Modul konversi format geospasial
│   │   ├── geojson_to_shp.py 
│   │   ├── kml_to_shp.py     
│   │   ├── gdb_to_shp.py     
│   │   ├── shp_to_geojson.py 
│   │   ├── shp_to_kml.py     
│   ├── utils/                # Modul utilitas (file handling, logging, dll.)
│── config/
│   ├── settings.py           # Konfigurasi aplikasi
│── tests/                    # Unit test untuk modul konversi
│── docs/                     # Dokumentasi aplikasi
│── requirements.txt          # Daftar dependensi Python
│── .gitignore                # File yang tidak perlu di-tracking oleh Git
│── main.py                   # Skrip utama untuk menjalankan aplikasi
```

## 📜 Log Konversi
Semua log proses konversi akan disimpan di folder `logs/` dan mencatat informasi berikut:
- Nama file yang dikonversi.
- Waktu mulai dan selesai konversi.
- Lama waktu proses.
- Status keberhasilan atau kegagalan konversi.

## ❌ Menghapus Data
Terdapat pilihan untuk menghapus hasil konversi atau keseluruhan data input dan output:
```sh
geo_converter --clear-output   # Hanya menghapus hasil konversi
geo_converter --clear-all      # Menghapus semua data input & output
```

## 🛠 Pengembangan & Kontribusi
Jika ingin mengembangkan atau berkontribusi, silakan fork repository ini dan lakukan pull request.

Happy coding! 🚀