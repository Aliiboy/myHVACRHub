## TIPS
### zsh
> Zsh
- Commands
```
chmod +x script.sh

```
### git
> Git is a free and open source distributed version control system.
- Commands
```
git status     # verifie l'etat des fichiers (modifié, staged, untracked)
git pull       # recupere et fusionne les modifications depuis le repoIncorporates change
git clean -f   #  
git restore .   # Restore specified paths in the working tree
git log -p --pretty=format:"Commit: %h - %s (%an, %ar)" --since="2025-02-10 00:00:00" --until="2025-02-11 00:00:00" > commits_files.txt
```
## pip
> Python standard package manager.
- Commands
```
pip freeze | xargs pip uninstall -y # Uninstall all packages
pip install -r requirements.txt
```

### uv
> An extremely fast Python package and project manager, written in Rust.
- Package commands
```
uv add
uv remove
```
- Install commands
```
uv sync
uv pip install -r pyproject.toml
uv pip compile pyproject.toml -o requirements.txt
```

### Ruff
> An extremely fast Python linter and code formatter, written in Rust.
- Commands
```
uv venv --python 3.10.5
uv run ruff check --fix
uv run ruff format
```

### Test
> pytest-watch a zero-config CLI tool that runs pytest, and re-runs it when a file in your project changes. It beeps on failures and can run arbitrary commands on each passing and failing test run.
- Commands
```
ptw
pytest --cov
```
Voir egalement les options de lancement dans pyproject.toml

### Flask
> Flask is a lightweight WSGI web application framework.
- Commands
```
flask --app main run
```

### Alembic
> Alembic provides for the creation, management, and invocation of change management scripts for a relational database, using SQLAlchemy as the underlying engine. 
- Commands
```
alembic revision -m "init"                # Init
alembic revision --autogenerate -m "add"  # Add field or new table
alembic upgrade head                      # Make migration
alembic stamp head (ne pas migrer)        # Roolback
```
- Notes : Lors de l'ajout d'un field, dans une table existant : 
  * indiquer que sa valeur peut etre null.
- Notes : Lors de l'ajout d'une table :
  * le rajouter dans env.py de alembic
