from pathlib import Path
from datetime import datetime
import geopandas as gpd
import fiona
import shutil
from src.utils.logger import log_conversion

def convert_gdb_to_shp_zip(input_folder, output_folder):
    """
    Mengonversi setiap layer dalam file GDB di input_folder ke format Shapefile (SHP)
    dan kemudian mengarsipkan hasil konversinya ke dalam file ZIP.
    Untuk setiap file GDB, dibuat folder output khusus dengan nama gabungan nama GDB dan timestamp (YYYY-MM-DD_HH-MM-SS).
    Setiap layer disimpan di dalam subfolder yang berbeda, kemudian seluruh folder tersebut diarsipkan.
    
    Logging hasil konversi akan disimpan ke logs/conversion.log.
    
    Args:
        input_folder (str): Path folder input yang berisi folder GDB (direktori dengan ekstensi .gdb).
        output_folder (str): Path folder output untuk menyimpan file SHP dan ZIP.
        
    Returns:
        bool: True jika setidaknya satu file GDB berhasil diproses, False jika tidak ada file GDB atau terjadi error.
    """
    start_time = datetime.now()
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    # Cari folder GDB di folder input (pastikan hanya mengambil direktori)
    gdb_folders = [folder for folder in input_path.glob("*.gdb") if folder.is_dir()]
    if not gdb_folders:
        print("❌ Tidak ada folder GDB ditemukan!")
        log_conversion("GDB → SHP & ZIP", "GAGAL", "Tidak ada folder GDB ditemukan di folder input")
        return False

    for gdb_folder in gdb_folders:
        gdb_name = gdb_folder.stem  # Nama GDB tanpa ekstensi
        timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        # Buat folder output khusus untuk file GDB ini
        gdb_output_folder = output_path / f"{gdb_name}_{timestamp}"
        gdb_output_folder.mkdir(parents=True, exist_ok=True)

        print(f"🔄 Mengonversi {gdb_folder.name} ke SHP...")
        
        # Dapatkan daftar layer dalam GDB
        try:
            layers = fiona.listlayers(str(gdb_folder))
        except Exception as e:
            print(f"❌ Gagal membaca layer dari {gdb_folder.name}: {e}")
            log_conversion("GDB → SHP & ZIP", "ERROR", f"Gagal membaca layer dari {gdb_folder.name}: {e}")
            continue

        for layer in layers:
            print(f"📂 Memproses layer: {layer} ...")
            try:
                gdf = gpd.read_file(str(gdb_folder), layer=layer)
            except Exception as e:
                print(f"❌ Gagal membaca layer {layer} dari {gdb_folder.name}: {e}")
                log_conversion("GDB → SHP & ZIP", "ERROR", f"Gagal membaca layer {layer} dari {gdb_folder.name}: {e}")
                continue

            # Buat folder output khusus untuk layer ini
            layer_folder = gdb_output_folder / layer
            layer_folder.mkdir(parents=True, exist_ok=True)
            output_shp_path = layer_folder / f"{layer}.shp"
            
            try:
                gdf.to_file(str(output_shp_path), driver="ESRI Shapefile")
                print(f"✅ Berhasil menyimpan {layer}.shp di {layer_folder}")
                log_conversion("GDB → SHP & ZIP", "SUKSES", f"Layer {layer} dari {gdb_folder.name} dikonversi dan disimpan di {layer_folder}")
            except Exception as e:
                print(f"❌ Gagal mengonversi layer {layer} dari {gdb_folder.name}: {e}")
                log_conversion("GDB → SHP & ZIP", "ERROR", f"Gagal mengonversi layer {layer} dari {gdb_folder.name}: {e}")
        
        # Setelah konversi semua layer, buat arsip ZIP dari folder output GDB
        try:
            zip_file = shutil.make_archive(str(gdb_output_folder), 'zip', root_dir=str(gdb_output_folder))
            print(f"✅ Berhasil membuat arsip ZIP: {zip_file}")
            log_conversion("GDB → SHP & ZIP", "SUKSES", f"{gdb_folder.name} diarsipkan ke {zip_file}")
        except Exception as e:
            print(f"❌ Gagal membuat arsip ZIP untuk {gdb_folder.name}: {e}")
            log_conversion("GDB → SHP & ZIP", "ERROR", f"Gagal membuat arsip ZIP untuk {gdb_folder.name}: {e}")
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"🎉 Konversi dan arsip ZIP selesai dalam {duration.total_seconds():.2f} detik!")
    return True
