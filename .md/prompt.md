## 📌 Ajoutes ou complete ces elements dans le projet

### **Usecases: `UpdateCoolingLoadFastCoefficientUseCase`**
#### Objectif : 
- Ce usecase permettra de modifier un coefficient.
- Ce usecase n'aura pas la responsabilité de chercher le coefficient à modifier.
- Ce usecase aura un methode `execute()`
#### Spéficication :
- La methode aura deux paramètres : 
  - un `id`pour recuperer le coefficient avec son identifiant unique.
  - un paramètre `data`.
- La methode renverra une entité `CoolingLoadFastCoefficient`.
- Si la methode ne trouve pas de coefficient, `execute()`levera une erreur `CoolingLoadFastCoefficientNotFoundException()`

---

### **Repository : `ColdRoomCoolingCoefficientSQLRepository`**
#### Objectif :
- Dans ce repository, créer un methode `update_coefficient()`.
#### Spécification : 
- La methode prendra deux paramètres :
  - un `id`pour recuperer le coefficient avec son identifiant unique.
  - un paramètre `data`.
- La methode utilisera `CoolingLoadFastCoefficientSQLModel` pour la requete.
- La methode renverra une entité de `CoolingLoadFastCoefficient` ou `None`. Pour renvoyer `CoolingLoadFastCoefficient`, il faudra utiliser la methode `to_entity()` de `CoolingLoadFastCoefficientSQLModel`.

---

### **Container d'injection de dépendances : `AppContainer`**
#### Objectif :
- Dans ce container, ajouter ou modifier les usescases si nécessaires.
- Dans ce container, ajouter ou modifier les repositories si nécessaires.

### **Routes**
#### Objectif :
- Ajoute la route `update_cooling_load_fast_coefficient`.
- Utilise des dtos de requete et de reponse qui herite de `BaseModel` et utilise `Field()` de pydantic.
#### Spécifications :
- Ajoute les décorateurs `@cast("Callable[..., Response]", jwt_required())` et `@cast("Callable[..., Response]", role_required("moderator", "admin"))`.
- Ajoute `security=security` et `responses`dans `@router.get()`.
- `responses` prendra `HTTPStatus.NOT_FOUND` et `HTTPStatus.OK` avec les dtos `ClientErrorResponse` et `GetCoolingLoadFastCoefficientResponse`.
- Fait un `try-except`