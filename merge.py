import os


def merge_python_files(
    input_directory: str, output_file: str, ignore_files: list[str] | None = None
) -> None:
    """
    Fusionne tous les fichiers .py d'un répertoire et de ses sous-dossiers en un seul fichier.
    Supprime les lignes vides et ajoute un commentaire avant chaque fichier.

    :param input_directory: Chemin du dossier contenant les fichiers .py
    :param output_file: Chemin du fichier de sortie
    :param ignore_files: Liste des fichiers à ignorer (ex: ["__init__.py"])
    """
    if ignore_files is None:
        ignore_files = []

    with open(output_file, "w", encoding="utf-8") as outfile:
        for root, _, files in os.walk(input_directory):
            for file in files:
                if file.endswith(".py") and file not in ignore_files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, encoding="utf-8") as infile:
                            outfile.write("#" * 80 + "\n")
                            outfile.write(f"# Fichier : {file_path}\n")
                            outfile.write("#" * 80 + "\n\n")
                            for line in infile:
                                if line.strip():  # Supprime les lignes vides
                                    outfile.write(line)
                            outfile.write("\n")
                    except Exception as e:
                        print(f"Erreur lors de la lecture du fichier {file_path}: {e}")


if __name__ == "__main__":
    input_directory = input(
        "Entrez le chemin du dossier contenant les fichiers .py : "
    ).strip()
    output_file = input(
        "Entrez le chemin du fichier de sortie (ex: merged_files.py) : "
    ).strip()

    if not os.path.isdir(input_directory):
        print("Le dossier spécifié n'existe pas ou n'est pas valide.")
    else:
        merge_python_files(input_directory, output_file, ignore_files=["__init__.py"])
        print(f"Les fichiers ont été fusionnés dans {output_file}.")
