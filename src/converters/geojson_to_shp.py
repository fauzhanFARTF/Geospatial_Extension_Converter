import geopandas as gpd
import os
import datetime
import shutil

def convert_geojson_to_shp(input_folder, output_folder):
    """ Mengonversi semua file GeoJSON dalam folder input ke SHP """
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.endswith(".geojson") or f.endswith(".json")]

    if not files:
        print("❌ Tidak ada file GeoJSON ditemukan!")
        return False

    for file in files:
        file_name = os.path.splitext(file)[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        file_output_folder = os.path.join(output_folder, f"{file_name}_{timestamp}")
        os.makedirs(file_output_folder, exist_ok=True)

        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(file_output_folder, f"{file_name}.shp")

        print(f"🔄 Mengonversi {file} ke {output_path} ...")
        gdf = gpd.read_file(input_path)
        gdf.to_file(output_path, driver="ESRI Shapefile")

        # Buat ZIP hasil konversi
        zip_file = os.path.join(output_folder, f"{file_name}_{timestamp}.zip")
        shutil.make_archive(zip_file.replace(".zip", ""), 'zip', file_output_folder)

        print(f"📦 Hasil dikompres ke {zip_file}")

    return True
