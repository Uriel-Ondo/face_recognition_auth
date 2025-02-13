

✅ 3. Recréer la base de données avec les bonnes colonnes
📌 Dans ton terminal, exécute le script suivant pour recréer la table correctement :

from models.database import init_db

init_db()
print("Base de données initialisée avec succès !")


📌 si vous etes sur windows Pour exécuter ce code, ouvre un terminal et lance la commande suivante :


python -c "from models.database import init_db; init_db(); print('Base de données initialisée avec succès !')"

