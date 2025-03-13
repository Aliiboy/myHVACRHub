# myHVACRHub

Propulsé par **PyFluids** et **CoolProp** pour les calculs thermodynamique.
[myHVACRHub](https://myhvacrhub.up.railway.app/)

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
- Créer des README par module
- Systeme de cache dans pour la db.
- faire la chasse au "delete" et "remove", choisir 1 mot sur les 2.

HUMID AIR :
- Doc string in humid_air.

PROJECTS : 
- CreateProject : Message de success plutot que le projet en lui même?
- CreateProject : Le créateur doit directement etre le permier membre ou le propriétaire (tant qu'a faire..)
- UpdateProject : Ne change pas update_at lors de la modification d'un projet.
- GetAllProject : Admin seule.
- UseCase : Faire lever ValidationException de Pydantic.
- Routes !!!.
- Dto : exporter des strings dans ProjetSettings
- Integrer les roles (propriétaire et membres).
- en fonction des role (moderator, user, admin), controller les niveaux d'accés des routes.
- Generer les tests avec 100% coverage.
- Update Project : sortir le uuid du schéma, le mettre en paramètre à part (à l'aide de Path), ensuite la modification du projet pourra se faire mais sans changer le UUID.

USERS :
- UserLoginRequest : password pattern ?
- Update user.
- route sign_in : manque ValidationError ?
- voir les projets des utilisateurs (membre et propriétaire) ?.
- Changer les exceptions de users.
- Interdir la suppression d'un utilisateur s'il est proprietaire d'un projet.