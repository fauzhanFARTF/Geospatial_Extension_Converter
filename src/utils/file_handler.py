import os

def get_input_files(folder, extension):
    return [f for f in os.listdir(folder) if f.endswith(extension)]