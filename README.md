# IAsimov Flask API

Une API basée sur **Flask OpenAPI3** propulsé par **PyFluids** et **CoolProp** pour les calculs thermodynamique.
[Iasimov](https://iasimov.pythonanywhere.com/openapi/)

## 🛠 Architecture
  - Clean Architecture avec `dependency-injector`
  - ORM basé sur `sqlmodel`

## 🚀 Fonctionnalités
- 💨 **Propriétés thermodynamiques de l'air humide** :
  - Calculer et récupérer plusieurs paramètres thermodynamiques (humidité, température, enthalpie, etc.)
- 📄 **Documentation OpenAPI** intégrée (Swagger, Redoc)

## 📦 Dépendances
Ce projet utilise les bibliothèques suivantes :
- [`flask-openapi3`](https://luolingchun.github.io/flask-openapi3/v4.x/)
- [`pyfluids`](https://github.com/portyanikhin/PyFluids)
- [`coolprop`](http\://coolprop.org/)

## ✅ TODO
COMMON :
- Créer des README par module
- Systeme de cache dans pour la db.
HUMID AIR :
- Doc string in humid_air.
PROJECTS : 
- UseCase : Faire lever ValidationException de Pydantic.
- Routes !!!.
- Integrer les roles (propriétaire et membres).
- 100% coverage.
USERS :
- Update user.
- voir les projets des utilisateurs (membre et propriétaire) ?.
- Changer les exceptions de users.
- Interdir la suppression d'un utilisateur s'il est proprietaire d'un projet.
---

🎉 **Merci d'utiliser IAsimov Flask API !** 🚀
