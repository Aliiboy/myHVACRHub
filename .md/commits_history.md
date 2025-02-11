### 📌 Résumé des commits (29/01/2025)

#### 🆕 **8fff3d8 - Initialisation du projet**
- Ajout d’un `.gitignore` contenant les fichiers à exclure.
- Définition de la version de Python (`.python-version` → `3.10.5`).
- Installation des dépendances.

#### 🏗 **Infrastructure du Projet**
- Mise en forme de l'arborescence et de l'architecture (Clean Architecture).
- Mise en place d’Alembic pour la gestion des migrations SQL (`alembic.ini`).
- Ajout des scripts :
  - `setup.sh` : installation des dépendances.
  - `deploy.sh` : mise à jour des dépendances sur **PythonAnywhere**.
  - `lint.sh` : vérification du code avec `mypy` et `ruff`.
  - `test.sh` : exécution des tests avec **pytest** et couverture de code.

#### 🗃 **Base de Données & Modèles**
- Configuration du moteur SQL.

#### ⚙ **Repositories & Use Cases**
- Ajout des interfaces de repository.
- Ajout des usescases.

#### 🔗 **API Flask & Routes**
- Ajout du **container d’injection de dépendances** (`container.py`).
- Définition des routes
- Intégration de la documentation OpenAPI.


En résumé : Le projet est prêt pour des évolutions futures ! 🚀

---

### 📌 Résumé des commits (30/01/2025)

#### 📝 8aa6b8f - Mise à jour des dépendances
- Ajout de `coolprop==6.6.0` dans `requirements.txt` et `pyproject.toml`.

#### ✨ 722eac2 - Ajout des propriétés de l'air humide
- Ajout de la classe `GetFullHAPropertyUseCase` pour récupérer les propriétés de l'air humide.
- Ajout de nouvelles routes `humid_air_routes.py`.
- Modification du `router.py` pour inclure la nouvelle route.

#### 🔧  eeacbc0 - Refactoring et tests
- Ajout de tests unitaires pour `HumidAir` et `GetFullHAPropertyUseCase`.

En résumé : intégration de la gestion de l’air humide, refactorisation et amélioration des tests ! 🚀

---

### 📌 Résumé des commits (02/02/2025)

#### 🔧 913671b - Suppression de `coolprop` des dépendances directes
- `coolprop` n'est plus une dépendance directe de `pyproject.toml`, elle est désormais incluse via `pyfluids`.

#### ✨ 32813dd - Ajout de `pyfluids`
- Ajout de `pyfluids==2.7.2` dans `pyproject.toml` pour la gestion des propriétés thermodynamiques.

#### 🚀 2125314 - Migration vers `pyfluids` pour l'air humide
- Remplacement de `CoolProp` par `pyfluids` dans `ha_entity.py`.
- Modification de `get_full_ha_props.py` pour prendre en charge la nouvelle structure.
- Mise à jour des paramètres dans `ha_settings.py`.
- Modification des routes `humid_air_routes.py` avec une gestion des erreurs améliorée.
- Ajout d'un fichier `TIPS.md` contenant des commandes utiles (`git`, `pip`, `flask`, etc.).

En résumé : **migration complète vers `pyfluids`**, meilleure gestion des erreurs et documentation améliorée ! 🚀

---

### 📌 Résumé des commits (04/02/2025)

#### 🔄 d367eb5 - Implémentation du pattern UnitOfWork
- Ajout de `SQLUnitOfWork` pour gérer les transactions en base de données de manière cohérente.
- Modification du repositorie `UserSQLRepository` pour utiliser `UnitOfWork` au lieu de `session_factory`.

#### 🔐 c6a4765 - Ajout du module d'authentification
- Ajout des entités `User` et `UserSQLModel` avec gestion des utilisateurs.
- Création des `usecases` :
  - `CreateUserUseCase` (inscription avec hachage de mot de passe `bcrypt`).
  - `AuthenticateUserUseCase` (authentification avec `JWT`).
- Intégration de `Flask-JWT-Extended` pour la gestion des tokens.
- Ajout des routes `auth/register` et `auth/login`.

#### 🛠️ Refactoring & Tests
- Refactorisation des tests pour un meilleur découplage (`BaseRepositoryTest`, `BaseAPITest`).
- Ajout de tests unitaires pour l’authentification et la gestion des livres.
- Ajout de validations pour `Book`, `User` et `HumidAirEntity`.

En résumé : **Mise en place de l’authentification, refactorisation du backend et adoption d’un pattern transactionnel sécurisé** 🚀.

---

### 📌 Résumé des commits (05/02/2025)

#### 🔐 da28fe7 - Gestion des permissions utilisateur
- Ajout du champ `role` (`admin`, `moderator`, `user`) dans `UserEntity`.
- Modification du service de token pour inclure le rôle utilisateur.
- Création du décorateur `role_required` pour sécuriser les routes.
- Mise à jour de l’authentification avec validation du rôle.

#### 🔑 0b72fba - Renforcement de la validation des mots de passe
- Ajout d’une contrainte de mot de passe contenant **au moins un chiffre et un caractère spécial**.
- Mise à jour de `UserSettings` et du DTO d’enregistrement.
- Adaptation des tests pour respecter ces nouvelles règles.

#### 🔄 274a4ac - Refactoring des services de mot de passe et token
- Introduction d’interfaces `PasswordHasherInterface` et `TokenServiceInterface`.
- Implémentation de `BcryptPasswordHasher` et `JWTTokenService` pour séparer les responsabilités.
- Ajustement des cas d’utilisation (`AuthenticateUserUseCase`, `CreateUserUseCase`).
- Mise à jour des tests unitaires.

#### 🚀 8dbe193 - Optimisation du bundle OpenAPI et refonte des routes
- Suppression des dépendances OpenAPI inutilisées (`redoc`, `rapidoc`, `scalar`…).
- Changement de la route principale de documentation `/openapi` → `/`.
- Extraction des routes protégées dans un module dédié (`protected_routes.py`).

En résumé : **Renforcement de la sécurité, gestion avancée des permissions et amélioration des performances de l’API !** 🔥

---

### 📌 Résumé des commits (07/02/2025 - 09/02/2025)

#### 🔄 **7833a44 - Ajout de l'endpoint `get_all_users`**
- Création du **cas d’utilisation** `GetAllUsersUsecase`.
- Ajout de la méthode `get_all_users(limit: int)` dans `UserRepositoryInterface`.
- Implémentation dans `UserSQLRepository`.
- Ajout d’une route sécurisée `GET /auth/get_all_users`, accessible uniquement aux **admins**.
- Tests unitaires et d'intégration pour `get_all_users`.

#### 🔄 **6da6550 - Refactoring des repositories**
- Renommage de `uow` → `unit_of_work` pour plus de clarté.
- Ajustement des appels `self.uow` → `self.unit_of_work` dans `UserSQLRepository`.

#### 🚀 **4ee6a73 - Clean Code & renommage**
- **Renommage des use cases :**
  - `AuthenticateUserUseCase` → `LoginUserUseCase`
  - `CreateUserUseCase` → `RegisterUserUseCase`
- Ajustement des routes et des injections de dépendances (`AppContainer`).
- Mise à jour des **tests** (`test_login_user.py`, `test_register_user.py`).

#### 🏗 **6da6550 - Réorganisation du code**
- Suppression des fichiers `__init__.py` inutiles dans plusieurs modules (`tests`, `entities`, `repositories`, etc.).
- Renommage cohérent des fichiers et imports (`ha_settings.py` → `humid_air_settings.py`).

#### 🛡 **e9f005a - Tests du décorateur `role_required`**
- Ajout de tests unitaires pour le décorateur `role_required` (`test_role_required.py`).
- Correction du mock pour `verify_jwt_in_request()`.

En résumé : **amélioration de la structure du code, ajout d’un endpoint admin sécurisé et nettoyage du projet !** 🚀

---

### 📌 Résumé des commits (10/02/2025)

#### 🔄 **Integration et refonte de `Fast Quote` et amélioration de la gestion des données**
- **Ajout de `database.xlsx`** pour stocker les coefficients et prix directement en Excel.
- **Mise à jour du chemin de la base de données** : utilisation de `EXCEL_DATABASE_URL` depuis `AppSettings`.
- **Refonte des formules de prix** pour les équipements frigorifiques et la production de froid.
- **Mise à jour des DTOs** pour inclure de nouveaux types et champs (`LocalFrigoRequest`, `GroupeFroidRequest`, `TuyauterieRequest`).

#### 🔗 **Ajout de nouvelles routes API**
- `GET /fast_quote/prix_frigo_local`
- `GET /fast_quote/prix_groupe_froid`
- `GET /fast_quote/prix_tuyauterie`
- `GET /fast_quote/prix_elec_autom`
- `GET /fast_quote/prix_frais_divers`

#### 🏗 **Refactorisation et standardisation**
- **Séparation des contrôleurs dans `fast_quote_controllers.py`** pour une meilleure organisation.
- **Refonte de `FastQuoteRepositoryInterface`** pour utiliser les nouvelles données Excel.
- **Refactorisation de `GetColdRoomCoolingLoadFastUseCase`** pour intégrer les nouvelles méthodes.

#### 🔧 **Corrections et améliorations**
- **Correction d’un bug d’authentification** sur la vérification du mot de passe utilisateur.
- **Ajout de `UserInvalidPasswordPatternException`** pour mieux gérer les erreurs de validation des mots de passe.


En résumé : **Migration de `Fast Quote` vers une base Excel configurable, ajout de plusieurs routes API pour un chiffrage rapide, refonte de la gestion des coefficients et des prix, amélioration de la sécurité et correction des erreurs**  

---

### 📌 Résumé des commits (11/02/2025)

#### 📦 **156d45d - Suppression des packages Excel**
- Suppression des dépendances lourdes `pandas`, `openpyxl`, `numpy` et `pytz`.
- Nettoyage de `pyproject.toml`, `requirements.txt` et `uv.lock`.
- Suppression du fichier `database.xlsx`.

#### 🔐 **474f0b9 - Ajout de permissions sur `Fast Quote`**
- La route `add_cooling_load_coefficient` est maintenant sécurisée (`jwt_required`).
- Modification de `role_required("moderator", "admin")` pour élargir l’accès.

#### ⚡ **a1199f1 - Refactoring et amélioration `Fast Quote`**
- **Ajout du modèle SQL** pour stocker les coefficients de charge frigorifique.
- Nouvelle entité `CoolingLoadFastCoefficient` avec migrations `Alembic`.
- **Refonte des repositories** :
  - `ColdRoomCoolingCoefficientSQLRepository` (stockage SQL).
  - `ColdRoomCoolingCoefficientExcelRepository` (ancienne version, supprimée).
- **Refonte des cas d'utilisation** :
  - `CalculateColdRoomCoolingLoadFastUseCase` remplace `GetColdRoomCoolingLoadFastUseCase`.
  - `AddCoolingLoadFastCoefficientUseCase` permet d'ajouter des coefficients.

#### 🚀 **cb39ea0 - Nettoyage et standardisation**
- Mise à jour des DTOs (`fast_quote_dtos.py`).
- Suppression des descriptions inutiles dans `user_entity.py`, `book_entity.py`, etc.
- Renommage `ColdRoomType` → `ColdRoomCategory` pour plus de cohérence.

En résumé : **Optimisation des dépendances, migration partielle vers SQL pour `Fast Quote`, renforcement des permissions et nettoyage du code !** 🚀