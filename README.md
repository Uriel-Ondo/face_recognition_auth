# Face Recognition Auth

Un petit programme de reconnaissance faciale associé à l'authentification.

---

## 3. Recréer la base de données avec les bonnes colonnes

✅ Pour recréer la base de données et ses tables correctement, exécute le script suivant dans ton terminal Python :

```python
from models.database import init_db

init_db()
print("Base de données initialisée avec succès !")
```

📌 **Si vous êtes sous Windows**, ouvrez un terminal (CMD ou PowerShell) et exécutez cette commande :

```bash
python -c "from models.database import init_db; init_db(); print('Base de données initialisée avec succès !')"
```

---

## 4. Lancer le projet

Démarrez l’application avec :

```bash
python3 face_recognition_app.py
```

---

**Remarque :**  
Assurez-vous d’avoir installé toutes les dépendances nécessaires (voir `requirements.txt`) avant de lancer le projet.
```
