import sys
import os
import shutil
from src.converters.gdb_to_shp import convert_gdb_to_shp
from src.converters.gdb_to_shp_zip import convert_gdb_to_shp_zip
from src.converters.gdb_to_kml import convert_gdb_to_kml
from src.converters.gdb_to_geojson import convert_gdb_to_geojson
from src.converters.geojson_to_shp import convert_geojson_to_shp
from src.converters.geojson_to_shp_zip import convert_geojson_to_shp_zip
from src.converters.geojson_to_kml import convert_geojson_to_kml
from src.converters.kml_to_shp import convert_kml_to_shp
from src.converters.kml_to_shp_zip import convert_kml_to_shp_zip
from src.converters.kml_to_geojson import convert_kml_to_geojson
from src.converters.shp_to_geojson import convert_shp_to_geojson
from src.converters.shp_to_kml import convert_shp_to_kml
from src.utils.logger import log_conversion
from src.utils.organizer import move_all_to_storage

# Konfigurasi folder input & output
INPUT_FOLDER = "data/input/"
OUTPUT_FOLDER = "data/output/"

# Pastikan Python mengenali folder `src`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Menu utama: Jenis format sumber
MAIN_MENU = {
    "1": "GDB",
    "2": "SHP",
    "3": "GeoJSON",
    "4": "KML",
    "5": "Pindahkan file input & output ke storage 📦",
    "6": "Hapus semua data input & output 🗑️",
    "0": "Keluar 🚪"
}

# Submenu konversi berdasarkan format sumber
SUB_MENUS = {
    "1": {  # GDB
        "1": ("GDB → KML", convert_gdb_to_kml),
        "2": ("GDB → GeoJSON", convert_gdb_to_geojson),
        "3": ("GDB → SHP", convert_gdb_to_shp),
        "4": ("GDB → SHP & ZIP", convert_gdb_to_shp_zip),
        "0": "Kembali ke menu utama 🔙"
    },
    "2": {  # SHP
        "1": ("SHP → GeoJSON", convert_shp_to_geojson),
        "2": ("SHP → KML", convert_shp_to_kml),
        "0": "Kembali ke menu utama 🔙"
    },
    "3": {  # GeoJSON
        "1": ("GeoJSON → KML", convert_geojson_to_kml),
        "2": ("GeoJSON → SHP", convert_geojson_to_shp),
        "3": ("GeoJSON → SHP & ZIP", convert_geojson_to_shp_zip),
        "0": "Kembali ke menu utama 🔙"
    },
    "4": {  # KML
        "1": ("KML → GeoJSON", convert_kml_to_geojson),
        "2": ("KML → SHP", convert_kml_to_shp),
        "3": ("KML → SHP_ZIP", convert_kml_to_shp_zip),
        "0": "Kembali ke menu utama 🔙"
    }
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
        print(f"✅ Semua file di dalam {folder_path} telah dihapus.")
    else:
        print(f"⚠️ Folder {folder_path} tidak ditemukan.")

def delete_all_data():
    """Menghapus semua file dalam input & output tanpa menghapus foldernya"""
    clear_folder(INPUT_FOLDER)
    clear_folder(OUTPUT_FOLDER)
    print("✅ Semua data dalam input & output telah dihapus.")

def show_main_menu():
    """Menampilkan menu utama"""
    print("\n===== Konverter Geospasial =====")
    print("Pilih jenis format sumber yang ingin dikonversi:")
    for key, value in MAIN_MENU.items():
        print(f"{key}. {value}")

def show_sub_menu(menu_id):
    """Menampilkan submenu berdasarkan pilihan pengguna"""
    submenu = SUB_MENUS.get(menu_id, {})
    print("\n===== Pilih Jenis Konversi =====")
    
    for key, value in submenu.items():
        if isinstance(value, tuple):  # Jika berupa tuple, ambil deskripsi saja
            print(f"{key}. {value[0]}")
        else:  # Jika hanya string, langsung cetak
            print(f"{key}. {value}")


def main():
    """Program utama"""
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    while True:
        show_main_menu()
        choice = input("Masukkan pilihan (0-6): ").strip()

        if choice == "0":
            print("👋 Keluar dari program.")
            sys.exit()

        elif choice == "5":
            print("\n📦 Memindahkan file & folder input & output ke storage berdasarkan format...")
            move_all_to_storage()
            print("✅ Semua file & folder telah dipindahkan ke storage!\n")

        elif choice == "6":
            konfirmasi = input("⚠️ Apakah Anda yakin ingin menghapus semua data dalam input & output? (y/n): ")
            if konfirmasi.lower() == "y":
                delete_all_data()

        elif choice in SUB_MENUS:
            while True:
                show_sub_menu(choice)
                sub_choice = input("Masukkan pilihan konversi: ").strip()

                if sub_choice == "0":
                    break  # Kembali ke menu utama

                submenu = SUB_MENUS[choice]
                if sub_choice in submenu:
                    desc, func = submenu[sub_choice]
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

                else:
                    print("⚠️ Pilihan tidak valid! Silakan coba lagi.\n")

        else:
            print("⚠️ Pilihan tidak valid! Silakan coba lagi.\n")

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "conversion.log")

# Buat folder logs jika belum ada
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

if __name__ == "__main__":
    main()
