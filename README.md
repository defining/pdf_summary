# pdf_summary Repository

Ce dépôt contient un script Python pour automatiser le résumé de documents PDF utilisant l'API LangChain. Suivez les instructions ci-dessous pour configurer et exécuter le projet.

## Configuration de l'environnement

### 1. Création d'un environnement virtuel

Utilisez un environnement virtuel pour isoler les dépendances du projet. Pour créer et activer un environnement virtuel, exécutez les commandes suivantes :

\`\`\`bash
python3 -m venv langchain
source langchain/bin/activate
\`\`\`

### 2. Installation des dépendances

Installez les dépendances nécessaires listées dans le fichier `requirements.txt`. Pour cela, exécutez :

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet et ajoutez-y la variable d'environnement requise :

\`\`\`plaintext
ANTHROPIC_API_KEY="votre_clé_api"
\`\`\`

Remplacez `"votre_clé_api"` par votre clé API réelle.

## Exécution du script

Pour lancer le script `main.py`, utilisez la commande suivante :

\`\`\`bash
python3 main.py
\`\`\`

### Paramètres optionnels

Vous pouvez également spécifier des paramètres pour affiner le processus :

\`\`\`bash
python3 main.py --pdf_path "/chemin/fictif/vers/le/document.pdf" --start_page 50 --end_page 75 --system_prompt "Veuillez me résumer le contenu des pages {start_page} à {end_page}." --assistant_prompt "Je vais vous fournir un résumé détaillé et précis des pages demandées."
\`\`\`

## Note importante

Avant d'exécuter le script, assurez-vous que le fichier `.env` est configuré correctement avec votre clé API LangChain. Cela est nécessaire pour que l'API fonctionne correctement.