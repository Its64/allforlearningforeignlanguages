import requests
from datetime import datetime
from googletrans import Translator

ANKI_CONNECT_URL = "http://localhost:8765"
DECK_NAME = "EnglishWords"
MODEL_NAME = "Basic"


def invoke(action, **params):
    """
    Send a request to the AnkiConnect API.

    Args:
        action (str): The action to perform.
        **params: Additional parameters for the action.

    Returns:
        dict: The JSON response from AnkiConnect.
    """
    response = requests.post(
        ANKI_CONNECT_URL,
        json={
            "action": action,
            "version": 6,
            "params": params
        }
    )
    return response.json()


def ensure_deck_exists(deck_name):
    """
    Ensure that the specified Anki deck exists. Create it if it does not.

    Args:
        deck_name (str): The name of the deck to check or create.
    """
    result = invoke("deckNames")
    if deck_name not in result.get("result", []):
        invoke("createDeck", deck=deck_name)


def add_anki_cards(word, translation, transcription):
    """
    Add two Anki cards for the given word and its translation, one in each direction.

    Args:
        word (str): The English word.
        translation (str): The translated word.
        transcription (str): The word's transcription.
    """
    note_fields = [
        {"Front": f"{word} {transcription}", "Back": translation},
        {"Front": translation, "Back": f"{word} {transcription}"}
    ]
    for fields in note_fields:
        invoke(
            "addNote",
            note={
                "deckName": DECK_NAME,
                "modelName": MODEL_NAME,
                "fields": fields,
                "tags": ["auto-added"]
            }
        )


def add_to_document(word, filename, transcription, translation, is_repeat=False):
    """
    Append a formatted line to the markdown document.

    Args:
        word (str): The word to add.
        filename (str): The markdown filename.
        transcription (str): The transcription of the word.
        translation (str): The translation of the word.
        is_repeat (bool): Whether the word is a repeat.
    """
    line = (
        f"|({word})|{transcription}|{translation}|\n"
        if is_repeat else
        f"|{word}|{transcription}|{translation}|\n"
    )
    with open(filename, "a", encoding="utf-8") as file:
        file.write(line)


def initialize_markdown_file(filename):
    """
    Initialize the markdown file with headers if it is empty.

    Args:
        filename (str): The markdown filename.
    """
    with open(filename, "a+", encoding="utf-8") as file:
        file.seek(0)
        if not file.read():
            file.write("|English|Transcription|Russian|\n|-------|-------------|-------|\n")


def main():
    """
    Main loop for adding words, their transcriptions, and translations to Anki and a markdown file.
    """
    ensure_deck_exists(DECK_NAME)

    today_filename = datetime.today().strftime('%Y-%m-%d') + ".md"
    initialize_markdown_file(today_filename)

    translator = Translator()

    while True:
        word_input = input("word: ").strip()
        if not word_input:
            continue

        transcription = input("transcription: ").strip()
        translation = translator.translate(word_input, src='en', dest='ru').text

        user_translation = input(
            f"{translation}? (Press Enter to accept, or type your own): "
        ).strip()
        if user_translation:
            translation = user_translation

        is_repeat = word_input.endswith("/r")
        word_clean = word_input.replace(" /r", "") if is_repeat else word_input

        add_to_document(word_clean, today_filename, transcription, translation, is_repeat)
        add_anki_cards(word_clean, translation, transcription)

        print(
            f"Added to Anki and document: {word_clean} - {translation} {transcription}"
        )


if __name__ == "__main__":
    main()
