from pathlib import Path
from datetime import datetime
import geopandas as gpd
import shutil
from src.utils.logger import log_conversion

def convert_kml_to_shp_zip(input_folder, output_folder):
    """
    Mengonversi setiap file KML dalam input_folder ke format Shapefile (SHP)
    dan kemudian mengarsipkan hasil konversinya ke dalam file ZIP.
    Setiap file KML akan dikonversi dan disimpan dalam folder terpisah di output_folder,
    dengan nama folder yang mengandung timestamp (YYYY-MM-DD_HH-MM-SS) untuk menghindari duplikasi.
    
    Logging hasil konversi akan disimpan ke logs/conversion.log.
    
    Args:
        input_folder (str): Path folder input yang berisi file KML.
        output_folder (str): Path folder output untuk menyimpan file SHP dan ZIP.
        
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
        log_conversion("KML → SHP & ZIP", "GAGAL", "Tidak ada file KML ditemukan")
        return False
    
    for file in kml_files:
        # Buat folder output khusus untuk file KML ini dengan timestamp
        timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = f"{file.stem}_{timestamp}"
        file_output_folder = output_path / folder_name
        file_output_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"🔄 Mengonversi {file.name} ke SHP...")
        
        try:
            # Membaca file KML
            gdf = gpd.read_file(str(file))
        except Exception as e:
            print(f"❌ Gagal membaca file {file.name}: {e}")
            log_conversion("KML → SHP & ZIP", "ERROR", f"Gagal membaca file {file.name}: {e}")
            continue
        
        output_shp_path = file_output_folder / f"{file.stem}.shp"
        try:
            # Menyimpan sebagai SHP
            gdf.to_file(str(output_shp_path), driver="ESRI Shapefile")
            print(f"✅ Berhasil menyimpan {file.stem}.shp di {file_output_folder}")
            log_conversion("KML → SHP & ZIP", "SUKSES", f"{file.name} dikonversi dan disimpan di {file_output_folder}")
        except Exception as e:
            print(f"❌ Gagal mengonversi {file.name}: {e}")
            log_conversion("KML → SHP & ZIP", "ERROR", f"Gagal mengonversi {file.name}: {e}")
            continue
        
        # Setelah konversi, buat file ZIP dari folder output
        try:
            # Mengarsipkan folder yang baru saja dibuat ke dalam ZIP
            zip_file = shutil.make_archive(str(file_output_folder), 'zip', root_dir=str(file_output_folder))
            print(f"✅ Berhasil membuat arsip ZIP: {zip_file}")
            log_conversion("KML → SHP & ZIP", "SUKSES", f"{file.name} diarsipkan ke {zip_file}")
        except Exception as e:
            print(f"❌ Gagal membuat arsip ZIP untuk {file.name}: {e}")
            log_conversion("KML → SHP & ZIP", "ERROR", f"Gagal membuat arsip ZIP untuk {file.name}: {e}")
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"🎉 Konversi dan arsip ZIP selesai dalam {duration.total_seconds():.2f} detik!")
    return True
