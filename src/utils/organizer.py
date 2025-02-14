from pathlib import Path
import shutil

# Definisikan folder input, output, dan storage menggunakan Pathlib
STORAGE_FOLDER = Path("data/storage")
OUTPUT_FOLDER = Path("data/output")
INPUT_FOLDER = Path("data/input")

def move_all_to_storage():
    """
    Memindahkan file dan folder dari folder output dan folder input ke dalam folder storage.
    
    Pemindahan dilakukan berdasarkan ekstensi file:
      - .geojson → storage/geojson
      - .shp, .shx, .dbf, .prj, .cpg → storage/shp
      - .kml → storage/kml
      - .zip → storage/zip
      
    Selain itu, jika ditemukan folder dengan ekstensi .gdb, 
    maka folder tersebut dipindahkan secara utuh ke storage/gdb.
    
    Fungsi ini berjalan secara rekursif untuk folder output dan input.
    """
    STORAGE_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Daftar folder sumber yang akan dipindahkan isinya ke storage
    source_folders = [OUTPUT_FOLDER, INPUT_FOLDER]
    files_moved = 0  # Counter untuk jumlah file/folder yang dipindahkan

    # Mapping ekstensi ke folder tujuan di dalam storage
    ext_map = {
        ".geojson": "geojson",
        ".shp": "shp",
        ".shx": "shp",
        ".dbf": "shp",
        ".prj": "shp",
        ".cpg": "shp",
        ".kml": "kml",
        ".zip": "zip"
    }

    def move_files_recursively(source_folder: Path, relative_path=""):
        nonlocal files_moved
        for item in source_folder.iterdir():
            new_relative_path = Path(relative_path) / item.name if relative_path else Path(item.name)
            if item.is_dir():
                # Jika folder memiliki ekstensi .gdb, pindahkan seluruh folder tanpa rekursi
                if item.suffix.lower() == ".gdb":
                    target_folder = STORAGE_FOLDER / "gdb" / new_relative_path.parent
                    target_folder.mkdir(parents=True, exist_ok=True)
                    target_path = target_folder / item.name
                    shutil.move(str(item), str(target_path))
                    files_moved += 1
                    print(f"📂 {new_relative_path} (folder .gdb) dipindahkan ke {target_path}")
                else:
                    # Lakukan rekursi untuk folder lain
                    move_files_recursively(item, str(new_relative_path))
                    # Hapus folder jika sudah kosong
                    if not any(item.iterdir()):
                        item.rmdir()
                        print(f"🗑️ Folder kosong dihapus: {item}")
            else:
                ext = item.suffix.lower()
                if ext in ext_map:
                    target_folder = STORAGE_FOLDER / ext_map[ext] / new_relative_path.parent
                    target_folder.mkdir(parents=True, exist_ok=True)
                    target_path = target_folder / item.name
                    shutil.move(str(item), str(target_path))
                    files_moved += 1
                    print(f"📂 {new_relative_path} dipindahkan ke {target_path}")

    # Proses setiap folder sumber (output dan input)
    for source in source_folders:
        if source.exists():
            move_files_recursively(source)
        else:
            print(f"⚠️ Folder {source} tidak ditemukan.")

    if files_moved == 0:
        print("⚠️ Tidak ada file atau folder yang dapat dipindahkan.")
    else:
        print(f"✅ {files_moved} file/folder telah dipindahkan ke folder storage sesuai ekstensinya.")

# Contoh penggunaan:
# move_all_to_storage()
