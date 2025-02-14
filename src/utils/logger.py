import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "conversion.log")

# Pastikan folder logs tersedia
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# Konfigurasi logging dengan RotatingFileHandler
log_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)  # Maksimal 1MB per file, simpan 5 backup
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def log_conversion(conversion_type, status, error_message=None):
    """
    Menyimpan log konversi ke file logs/conversion.log

    Args:
        conversion_type (str): Jenis konversi yang dilakukan.
        status (str): Status konversi ("SUKSES", "GAGAL", atau "ERROR").
        error_message (str, optional): Pesan kesalahan jika ada.
    """
    if status == "ERROR" and error_message:
        message = f"{conversion_type}: {status} - {error_message}"
        logger.error(message)
    else:
        message = f"{conversion_type}: {status}"
        logger.info(message)

    print(f"📝 Log tersimpan: {message}")
