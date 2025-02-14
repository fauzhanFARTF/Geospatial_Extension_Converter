import os

def get_input_files(folder, extensions):
    """
    Mengambil daftar file dengan ekstensi tertentu di dalam folder.

    Args:
        folder (str): Path folder input.
        extensions (str | list): Ekstensi file yang ingin dicari (misal: ".geojson" atau [".geojson", ".shp"]).

    Returns:
        list: Daftar file dengan ekstensi yang sesuai.
    """
    if not os.path.exists(folder):
        print(f"⚠️ Folder '{folder}' tidak ditemukan.")
        return []

    if isinstance(extensions, str):  # Jika hanya satu ekstensi, ubah ke list
        extensions = [extensions]

    extensions = tuple(ext.lower() for ext in extensions)  # Case-insensitive check
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(extensions)]
