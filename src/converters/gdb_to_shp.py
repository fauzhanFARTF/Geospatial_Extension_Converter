import os
import datetime
import shutil
import geopandas as gpd
import fiona

def convert_gdb_to_shp(input_folder, output_folder):
    """ Mengonversi setiap layer dalam file GDB ke SHP, menyimpannya dalam satu folder per GDB """
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.endswith(".gdb")]

    if not files:
        print("❌ Tidak ada file GDB ditemukan!")
        return False

    for file in files:
        gdb_name = os.path.splitext(file)[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Buat folder utama untuk setiap GDB
        gdb_output_folder = os.path.join(output_folder, f"{gdb_name}_{timestamp}")
        os.makedirs(gdb_output_folder, exist_ok=True)

        input_path = os.path.join(input_folder, file)

        print(f"🔄 Mengonversi {file} ke Shapefile ...")

        # Dapatkan daftar layer dalam GDB
        layers = fiona.listlayers(input_path)

        for layer in layers:
            print(f"📂 Memproses layer: {layer} ...")

            # Buat folder khusus untuk setiap layer dalam folder GDB utama
            layer_output_folder = os.path.join(gdb_output_folder, layer)
            os.makedirs(layer_output_folder, exist_ok=True)

            # Konversi setiap layer ke SHP
            gdf = gpd.read_file(input_path, layer=layer)
            output_shp_path = os.path.join(layer_output_folder, f"{layer}.shp")
            gdf.to_file(output_shp_path, driver="ESRI Shapefile")

        # Buat ZIP untuk seluruh folder GDB
        zip_file = os.path.join(output_folder, f"{gdb_name}_{timestamp}.zip")
        shutil.make_archive(zip_file.replace(".zip", ""), 'zip', gdb_output_folder)

        print(f"📦 Semua layer dari {file} dikompres ke {zip_file}")

    return True
