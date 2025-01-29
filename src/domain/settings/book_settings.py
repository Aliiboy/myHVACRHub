class BookEntitieSettings:
    # id
    id_description: str = "Identifiant unique du livre"
    # title
    title_description: str = "Titre du livre"
    title_min_length: int = 1
    title_max_length: int = 250
    # author
    author_decription: str = "Auteur du livre"
    author_min_length: int = 1
    author_max_length: int = 250
    # date
    created_at_description: str = (
        "Date a laquelle le livre est rentré dans la base de données"
    )
