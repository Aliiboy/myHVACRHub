import os


def merge_python_files(input_directory: str, output_file: str) -> None:
    """
    Parcourt les sous-dossiers d'un répertoire pour collecter les lignes de tous les fichiers .py
    et les écrit dans un fichier de sortie en supprimant les lignes vides.

    :param input_directory: Chemin du dossier contenant les fichiers .py
    :param output_file: Chemin du fichier de sortie
    """
    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(input_directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, encoding="utf-8") as infile:
                            outfile.write(f"# Contenu du fichier: {file_path}\n")
                            for line in infile:
                                if line.strip():
                                    outfile.write(line)
                            outfile.write("\n")
                    except Exception as e:
                        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")


if __name__ == "__main__":
    input_directory: str = input(
        "Entrez le chemin du dossier contenant les fichiers .py : "
    )
    output_file: str = input(
        "Entrez le chemin du fichier de sortie (ex: merged_files.py) : "
    )

    if not os.path.isdir(input_directory):
        print("Le dossier spécifié n'existe pas ou n'est pas valide.")
    else:
        merge_python_files(input_directory, output_file)
        print(f"Les fichiers ont été fusionnés dans {output_file}.")
