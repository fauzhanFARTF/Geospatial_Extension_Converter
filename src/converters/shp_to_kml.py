import geopandas as gpd
import os
import datetime

def find_shp_files(root_folder):
    """Mencari semua file .shp di dalam subfolder secara rekursif"""
    shp_files = []
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".shp"):
                shp_files.append(os.path.join(root, file))
    return shp_files

def convert_shp_to_kml(input_folder, output_folder):
    """Mengonversi semua file SHP dalam subfolder ke KML"""
    os.makedirs(output_folder, exist_ok=True)
    shp_files = find_shp_files(input_folder)

    if not shp_files:
        print("❌ Tidak ada file SHP ditemukan dalam folder atau subfolder!")
        return False

    for shp_path in shp_files:
        file_name = os.path.splitext(os.path.basename(shp_path))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_kml_path = os.path.join(output_folder, f"{file_name}_{timestamp}.kml")

        print(f"🔄 Mengonversi {shp_path} → {output_kml_path} ...")

        try:
            gdf = gpd.read_file(shp_path)
            gdf.to_file(output_kml_path, driver="KML")
            print(f"✅ Berhasil: {output_kml_path}")

        except Exception as e:
            print(f"❌ Gagal mengonversi {shp_path}: {e}")

    return True
