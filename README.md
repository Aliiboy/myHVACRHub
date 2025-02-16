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
- Systeme de cache dans pour la db
- Mettre les requests (ou les renommer en CommandType) dans le dossier domain (request des usescases) voir `UpdateCoolingLoadFastCoefficientUseCase`. Et garder les Responses et les QueryParams dans le dossier api.
- Reprendre le testing
- Faire le point sur les Field(), centraliser dans des fichiers config
- renommer les bon fichiers et les endpoints suite au refacto
---

🎉 **Merci d'utiliser IAsimov Flask API !** 🚀
