import os
import datetime
from pathlib import Path
import geopandas as gpd
import fiona
from src.utils.logger import log_conversion

def convert_gdb_to_kml(input_folder, output_folder):
    """Mengonversi setiap layer dalam file GDB ke KML, menyimpannya dalam satu folder per GDB."""
    start_time = datetime.datetime.now()
    os.makedirs(output_folder, exist_ok=True)

    # Cari folder .gdb dalam input_folder
    gdb_folders = [f for f in os.listdir(input_folder) if (Path(input_folder) / f).is_dir() and f.endswith(".gdb")]

    if not gdb_folders:
        print("❌ Tidak ada folder GDB ditemukan!")
        log_conversion("GDB → KML", "GAGAL", "Tidak ada file GDB di input folder")
        return False

    for gdb in gdb_folders:
        gdb_name = Path(gdb).stem  # Nama tanpa ekstensi
        timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")

        # Buat folder output khusus untuk setiap GDB
        gdb_output_folder = Path(output_folder) / f"{gdb_name}_{timestamp}"
        gdb_output_folder.mkdir(parents=True, exist_ok=True)

        input_path = Path(input_folder) / gdb

        print(f"🔄 Mengonversi {gdb} ke KML...")

        # Dapatkan daftar layer dalam GDB
        try:
            layers = fiona.listlayers(str(input_path))
        except Exception as e:
            print(f"❌ Gagal membaca layer dari {gdb}: {e}")
            log_conversion("GDB → KML", "ERROR", f"Gagal membaca layer dari {gdb}: {e}")
            continue

        for layer in layers:
            print(f"📂 Memproses layer: {layer} ...")

            try:
                gdf = gpd.read_file(str(input_path), layer=layer)

                # Buat folder untuk menyimpan KML dalam subfolder
                layer_output_folder = gdb_output_folder / layer
                layer_output_folder.mkdir(parents=True, exist_ok=True)

                output_kml_path = layer_output_folder / f"{layer}.kml"
                gdf.to_file(output_kml_path, driver="KML")

                print(f"✅ Berhasil menyimpan {layer}.kml di {layer_output_folder}")
                log_conversion(f"GDB {gdb} → {layer}.kml", "SUKSES")

            except Exception as e:
                print(f"❌ Gagal mengonversi layer {layer}: {e}")
                log_conversion(f"GDB {gdb} → {layer}.kml", "ERROR", f"Gagal mengonversi {layer}: {e}")

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"🎉 Konversi selesai dalam {duration.total_seconds():.2f} detik!")
    log_conversion("GDB → KML", "SUKSES", f"Waktu konversi: {duration.total_seconds():.2f} detik")

    return True