# iasimov

Propulsé par **PyFluids** et **CoolProp** pour les calculs thermodynamique.
[iasimov](https://iasimov.pythonanywhere.com/)

## 🚀 Fonctionnalités
- 💨 **Propriétés thermodynamiques de l'air humide** :
  - Calculer et récupérer plusieurs paramètres thermodynamiques (humidité, température, enthalpie, etc.)

## 📦 Dépendances
Ce projet utilise les bibliothèques suivantes :
- [`flask-openapi3`](https://luolingchun.github.io/flask-openapi3/v4.x/)
- [`pyfluids`](https://github.com/portyanikhin/PyFluids)
- [`coolprop`](http\://coolprop.org/)

## ✅ TODO
COMMON :
- 100% de coverage sur les tests.
- Passer avec controller et presenter.

HUMID AIR :
- Doc string in humid_air.

PROJECTS : 
- UpdateProject : Ne change pas update_at lors de la modification d'un projet.
- UpdateProject : Seulement si l'utilisateur est propriétaire.
- DeleteProject : Seulement si l'utilisateur est propriétaire.
- AddProjectMember : Seulement si l'utilisateur est propriétaire.
- en fonction des role (moderator, user, admin), controller les niveaux d'accés des routes.

USERS :
- Update user.
- Interdir la suppression d'un utilisateur s'il est proprietaire d'un projet.