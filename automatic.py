# from datetime import datetime
# from deep_translator import GoogleTranslator

# def add_to_document(word, filename, repeat=False):
#     # Translate the word from English to Russian
#     translator = GoogleTranslator(source='en', target='ru')
#     translated_word = translator.translate(word)

#     # Prepare the line to be added to the document
#     if repeat:
#         line = f"|({word})|{translated_word}|\n"
#     else:
#         line = f"|{word}|{translated_word}|\n"
#     print(translated_word)

#     # Append the line to the file
#     with open(filename, "a", encoding="utf-8") as file:
#         file.write(line)

# # Generate the filename based on today's date
# filen = datetime.today().strftime('%Y-%m-%d') + ".md"

# # Create the markdown file if it doesn't exist and write the header
# with open(filen, "a+", encoding="utf-8") as file:
#     file.seek(0)  # Go to the beginning of the file
#     if not file.read():  # Check if the file is empty
#         file.write("|English|Russian|\n|----|-----------|\n")

# # Main loop to continuously add words
# while True:
#     word = input("word: ")
#     if word.endswith("/r"):
#         wordf = word.replace(" /r", "")
#         add_to_document(wordf, filen, repeat=True)
#     else:
#         add_to_document(word, filen)

from datetime import datetime
from googletrans import Translator

def add_to_document(word, filename, transcription, repeat=False):
    # Create a translator object
    translator = Translator()
    translated_word = translator.translate(word, src='en', dest='ru').text
    ser = input(f"{translated_word}? ")
    if len(ser) > 0:
        translated_word = ser

    # Prepare the line to be added to the document
    if repeat:
        line = f"|({word})|{transcription}|{translated_word}|\n"
    else:
        line = f"|{word}|{transcription}|{translated_word}|\n"
    print(translated_word)

    # Append the line to the file
    with open(filename, "a", encoding="utf-8") as file:
        file.write(line)

# Generate the filename based on today's date
filen = datetime.today().strftime('%Y-%m-%d') + ".md"

# Create the markdown file if it doesn't exist and write the header
with open(filen, "a+", encoding="utf-8") as file:
    file.seek(0)  # Go to the beginning of the file
    if not file.read():  # Check if the file is empty
        file.write("|English|Transcription|Russian|\n|-------|-------------|-------|\n")

# Main loop to continuously add words
while True:
    word = input("word: ")
    transcription = input("transcription: ")
    if word.endswith("/r"):
        wordf = word.replace(" /r", "")
        add_to_document(wordf, filen, transcription, repeat=True)
    else:
        add_to_document(word, filen, transcription)