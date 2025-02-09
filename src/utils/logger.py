import os
import logging
from datetime import datetime

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "conversion.log")

# Pastikan folder logs tersedia
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# Konfigurasi logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_conversion(conversion_type, status):
    """
    Menyimpan log konversi ke file logs/conversion.log

    Args:
        conversion_type (str): Jenis konversi yang dilakukan.
        status (str): Status konversi ("SUKSES" atau "GAGAL").
    """
    message = f"{conversion_type}: {status}"
    logging.info(message)
    print(f"📝 Log tersimpan: {message}")
