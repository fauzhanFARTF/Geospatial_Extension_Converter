from pathlib import Path
from datetime import datetime
import geopandas as gpd
from src.utils.logger import log_conversion

def convert_kml_to_geojson(input_folder, output_folder):
    """
    Mengonversi setiap file KML dalam input_folder ke format GeoJSON.
    Setiap file KML akan dikonversi dan disimpan dalam folder terpisah di output_folder,
    dengan nama folder yang mengandung timestamp (YYYY-MM-DD_HH-MM-SS) untuk menghindari duplikasi.
    
    Logging hasil konversi akan disimpan ke logs/conversion.log.
    
    Args:
        input_folder (str): Path folder input yang berisi file KML.
        output_folder (str): Path folder output untuk menyimpan file GeoJSON.
        
    Returns:
        bool: True jika setidaknya satu file berhasil diproses, False jika tidak ada file atau terjadi error.
    """
    start_time = datetime.now()
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Cari file KML di folder input
    kml_files = list(input_path.glob("*.kml"))
    if not kml_files:
        print("❌ Tidak ada file KML ditemukan!")
        log_conversion("KML → GeoJSON", "GAGAL", "Tidak ada file KML ditemukan")
        return False
    
    for file in kml_files:
        # Buat folder output khusus untuk file KML ini dengan timestamp
        timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"{file.stem}_{timestamp}"
        file_output_folder = output_path / folder_name
        file_output_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"🔄 Mengonversi {file.name} ke GeoJSON...")
        
        try:
            # Membaca file KML
            gdf = gpd.read_file(str(file))
        except Exception as e:
            print(f"❌ Gagal membaca file {file.name}: {e}")
            log_conversion("KML → GeoJSON", "ERROR", f"Gagal membaca file {file.name}: {e}")
            continue
        
        output_geojson_path = file_output_folder / f"{file.stem}.geojson"
        try:
            # Menyimpan sebagai GeoJSON
            gdf.to_file(str(output_geojson_path), driver="GeoJSON")
            print(f"✅ Berhasil menyimpan {file.stem}.geojson di {file_output_folder}")
            log_conversion("KML → GeoJSON", "SUKSES", f"{file.name} dikonversi dan disimpan di {file_output_folder}")
        except Exception as e:
            print(f"❌ Gagal mengonversi {file.name}: {e}")
            log_conversion("KML → GeoJSON", "ERROR", f"Gagal mengonversi {file.name}: {e}")
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"🎉 Konversi selesai dalam {duration.total_seconds():.2f} detik!")
    return True
