import sys
import os
import shutil
from src.converters.geojson_to_shp import convert_geojson_to_shp
from src.converters.kml_to_shp import convert_kml_to_shp
from src.converters.gdb_to_shp import convert_gdb_to_shp
from src.converters.shp_to_geojson import convert_shp_to_geojson
from src.converters.shp_to_kml import convert_shp_to_kml
from src.utils.logger import log_conversion

# Pastikan Python mengenali folder `src`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Konfigurasi folder input & output
INPUT_FOLDER = "data/input/"
OUTPUT_FOLDER = "data/output/"

# Daftar konversi yang tersedia
CONVERSIONS = {
    "1": ("GeoJSON → SHP", convert_geojson_to_shp),
    "2": ("KML → SHP", convert_kml_to_shp),
    "3": ("GDB → SHP", convert_gdb_to_shp),
    "4": ("SHP → GeoJSON", convert_shp_to_geojson),
    "5": ("SHP → KML", convert_shp_to_kml),
}

def clear_folder(folder_path):
    """Menghapus semua file dalam folder tanpa menghapus folder itu sendiri"""
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print(f"✅ Semua file di dalam {folder_path} telah dihapus, tetapi folder tetap ada.")
    else:
        print(f"⚠️ Folder {folder_path} tidak ditemukan.")

def delete_all_data():
    """Menghapus semua file dalam input & output tanpa menghapus foldernya"""
    clear_folder(INPUT_FOLDER)
    clear_folder(OUTPUT_FOLDER)
    print("✅ Semua data dalam input & output telah dihapus, tetapi folder tetap ada.")

def show_menu():
    """ Menampilkan menu pilihan konversi """
    print("\n===== Konverter Geospasial =====")
    print("Pilih jenis konversi yang ingin dilakukan:")
    for key, (desc, _) in CONVERSIONS.items():
        print(f"{key}. {desc}")
    #print("6. Hapus hanya output")
    #print("7. Hapus seluruh data (input & output, tetapi folder tetap)")
    print("0. Keluar")

def main():
    """ Program utama """
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    while True:
        show_menu()
        choice = input("Masukkan pilihan (0-7): ").strip()

        if choice == "0":
            print("👋 Keluar dari program.")
            sys.exit()

        elif choice in CONVERSIONS:
            desc, func = CONVERSIONS[choice]
            print(f"\n🚀 Menjalankan konversi: {desc} ...")
            try:
                success = func(INPUT_FOLDER, OUTPUT_FOLDER)
                if success:
                    log_conversion(desc, "SUKSES")
                    print(f"✅ Konversi {desc} selesai!\n")
                else:
                    log_conversion(desc, "GAGAL")
                    print(f"❌ Konversi {desc} gagal!\n")
            except Exception as e:
                log_conversion(desc, "ERROR")
                print(f"❌ Terjadi kesalahan pada {desc}: {e}\n")

        elif choice == "6":
            clear_folder(OUTPUT_FOLDER)

        elif choice == "7":
            konfirmasi = input("⚠️ Apakah Anda yakin ingin menghapus semua data dalam input & output? (y/n): ")
            if konfirmasi.lower() == "y":
                delete_all_data()

        else:
            print("⚠️ Pilihan tidak valid! Silakan coba lagi.\n")
            
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "conversion.log")

# Buat folder logs jika belum ada
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

if __name__ == "__main__":
    main()
