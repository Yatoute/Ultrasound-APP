import gzip
import shutil
import os

def decompress_h5_file(input_file, output_file):
    # Vérifier si le fichier d'entrée existe
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Le fichier {input_file} n'existe pas.")
    
    # Décompresser le fichier gzip
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Chemins des fichiers
input_path = '/home/EnsaeUltrasound/Utrasound-API/static/model/Hyperband.h5.gz'
output_path = '/home/EnsaeUltrasound/Utrasound-API/static/model/Hyperband.h5'

# Appeler la fonction de décompression
decompress_h5_file(input_path, output_path)
