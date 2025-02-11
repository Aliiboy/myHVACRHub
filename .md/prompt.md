## 📌 Ajoutes ou complete ces elements dans le projet

### **Usecases: `GetAllCoolingLoadFastCoefficienUseCase`**
#### Objectif : 
- Ce usecase permettra d'afficher l'ensemble des coefficients.
- Ce usecase aura un methode `execute()`
#### Spéficication :
- La methode aura un parametre `limit: int` pour limiter le nombre de coefficients à afficher et renverra une liste de l'entité `CoolingLoadFastCoefficient`.

---

### **Repository : `ColdRoomCoolingCoefficientSQLRepository`**
#### Objectif :
- Dans ce repository, créer un methode `get_all_coefficients()`.
#### Spécification :
- La methode prendra `limit: int` en paramètre.
- La methode utilisera `CoolingLoadFastCoefficientSQLModel` pour la requete.
- La methode renverra une liste de `CoolingLoadFastCoefficient`. Pour renvoyer une liste de `CoolingLoadFastCoefficient`, il faudra utiliser la methode `to_entity()` de `CoolingLoadFastCoefficientSQLModel`.
- Il faudra ranger la liste par ordre de `category`et par ordre de `vol_min`.

---

### **Container d'injection de dépendances : `AppContainer`**
#### Objectif :
- Dans ce container, ajouter ou modifier les usescases si nécessaires.
- Dans ce container, ajouter ou modifier les repositories si nécessaires.

### **Routes**
#### Objectif :
- Ajoute la route `get_all_cooling_load_fast_coefficients`.
#### Spécifications :
- Ajoute les décorateurs `jwt_required()`et `role_required("moderator")`
- Ajoute `security=security` et `responses`dans `@router.get()`
- `responses` prendra `HTTPStatus.FORBIDDEN` et `HTTPStatus.OK` avec les dtos `ClientErrorResponse` et `GetAllCoolingLoadFastResponse`.
- Fait un `try-except`