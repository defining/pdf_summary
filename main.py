import os
import argparse
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

# Définition des valeurs par défaut
DEFAULT_PDF_PATH = "/Users/Amzur/Desktop/paper_1.pdf"
DEFAULT_START_PAGE = 93
DEFAULT_END_PAGE = 110
DEFAULT_SYSTEM_PROMPT = "Fais moi un résumé du livre entre les pages {start_page} et {end_page} pour me donner l'idée globale de cette partie."
DEFAULT_ASSISTANT_PROMPT = "En tant qu'assistant de résumé de livres, je vais faire de mon mieux pour résumer le contenu clé de manière concise et informative, tout en capturant l'essence et les points les plus importants."

def main():
    # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(description="Extrait et résume des pages d'un document PDF.")
    parser.add_argument("--pdf_path", type=str, default=DEFAULT_PDF_PATH, help="Chemin vers le fichier PDF.")
    parser.add_argument("--start_page", type=int, default=DEFAULT_START_PAGE, help="Page de début (indexation à base zéro).")
    parser.add_argument("--end_page", type=int, default=DEFAULT_END_PAGE, help="Dernière page à inclure (indexation à base zéro).")
    parser.add_argument("--system_prompt", type=str, default=DEFAULT_SYSTEM_PROMPT, help="Message système pour démarrer le processus de dialogue.")
    parser.add_argument("--assistant_prompt", type=str, default=DEFAULT_ASSISTANT_PROMPT, help="Réponse initiale de l'assistant.")

    # Lecture des arguments
    args = parser.parse_args()

    # Affichage des paramètres utilisés
    print("Paramètres utilisés:")
    print(f"Chemin du PDF: {args.pdf_path}")
    print(f"Page de début: {args.start_page}")
    print(f"Page de fin: {args.end_page}")
    print(f"Prompt système: {args.system_prompt}")
    print(f"Prompt assistant: {args.assistant_prompt}")

    # Vérification de l'existence du fichier PDF
    if not os.path.exists(args.pdf_path):
        print(f"Erreur: Le fichier {args.pdf_path} n'existe pas.")
        return

    # Charge les variables d'environnement depuis `.env`
    load_dotenv()

    # Accède à la variable d'environnement
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    # Initialisation du chat avec LangChain Anthropic
    chat = ChatAnthropic(temperature=0, model_name="claude-3-opus-20240229")

    # Chargement du document PDF
    loader = PyPDFLoader(args.pdf_path)
    pages = loader.load_and_split()

    # Validation des indices de pages
    if args.start_page < 0 or args.end_page >= len(pages) or args.start_page > args.end_page:
        print("Erreur: Les indices de page spécifiés sont invalides.")
        return

    # Extraire les pages souhaitées
    selected_pages = pages[args.start_page:min(args.end_page + 1, len(pages))]
    texte = ""

    # Compilation du texte des pages sélectionnées
    for page in selected_pages:
        texte += page.page_content

    # Création du template de dialogue
    system = args.system_prompt.format(start_page=args.start_page, end_page=args.end_page)
    human = "{text}"
    assistant = args.assistant_prompt

    # Création du template de dialogue
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human),
        ("assistant", assistant)
    ], template_format='f-string')

    # Configuration de la chaîne de traitement avec le template de dialogue
    chain = prompt | chat

    # Préparer les données d'entrée pour le modèle
    input_data = {
        "text": texte,
        "start_page": args.start_page,
        "end_page": args.end_page
    }

    # Envoyer le dictionnaire au modèle pour invoquer le traitement
    response = chain.invoke(input_data)

    # Afficher la réponse
    # print(response.content)

    # Enregistrer la réponse
    with open('resultat.txt', 'w') as file:
        file.write(response.content)

if __name__ == "__main__":
    main()
