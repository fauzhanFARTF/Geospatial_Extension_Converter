from pathlib import Path
from datetime import datetime
import geopandas as gpd
from src.utils.logger import log_conversion

def convert_geojson_to_shp(input_folder, output_folder):
    """
    Mengonversi setiap file GeoJSON dalam input_folder ke format Shapefile (SHP).
    Setiap file GeoJSON akan dikonversi dan disimpan dalam folder terpisah di output_folder,
    dengan nama folder yang mengandung timestamp (YYYY-MM-DD_HH-MM-SS) untuk menghindari duplikasi.
    
    Logging hasil konversi akan disimpan ke logs/conversion.log.
    
    Args:
        input_folder (str): Path folder input yang berisi file GeoJSON.
        output_folder (str): Path folder output untuk menyimpan file SHP.
        
    Returns:
        bool: True jika setidaknya satu file berhasil diproses, False jika tidak ada file atau terjadi error.
    """
    start_time = datetime.now()
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    # Cari file GeoJSON di folder input
    geojson_files = list(input_path.glob("*.geojson"))
    if not geojson_files:
        print("❌ Tidak ada file GeoJSON ditemukan!")
        log_conversion("GeoJSON → SHP", "GAGAL", "Tidak ada file GeoJSON ditemukan")
        return False

    for file in geojson_files:
        # Buat folder output khusus untuk file GeoJSON ini dengan timestamp
        timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"{file.stem}_{timestamp}"
        file_output_folder = output_path / folder_name
        file_output_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"🔄 Mengonversi {file.name} ke SHP...")
        
        try:
            # Membaca file GeoJSON
            gdf = gpd.read_file(str(file))
        except Exception as e:
            print(f"❌ Gagal membaca file {file.name}: {e}")
            log_conversion("GeoJSON → SHP", "ERROR", f"Gagal membaca file {file.name}: {e}")
            continue
        
        output_shp_path = file_output_folder / f"{file.stem}.shp"
        try:
            # Menyimpan sebagai SHP
            gdf.to_file(str(output_shp_path), driver="ESRI Shapefile")
            print(f"✅ Berhasil menyimpan {file.stem}.shp di {file_output_folder}")
            log_conversion("GeoJSON → SHP", "SUKSES", f"{file.name} dikonversi dan disimpan di {file_output_folder}")
        except Exception as e:
            print(f"❌ Gagal mengonversi {file.name}: {e}")
            log_conversion("GeoJSON → SHP", "ERROR", f"Gagal mengonversi {file.name}: {e}")
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"🎉 Konversi selesai dalam {duration.total_seconds():.2f} detik!")
    return True