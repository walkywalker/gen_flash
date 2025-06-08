# Anki Language Flash Card Package Generator

Simple script for converting a list of words or phrases into Anki flashcards with generated audio for learning the translations in a target language.

The generated `.apkg` file can be directly imported into Anki.

Each word or phrase will have 4 cards, consider the example translation of "red" from English to Spanish:

- red (no audio)
- roja (no audio)
- roja (roja audio)
- (roja audio)

This script supports 2 modes:

- A: User provides a file containing the source phrases in their primary language, and a separate file containing the corresponding translations in the target language.
- B: User provides a file containing the source phrases in their primary language. [DeepL](https://www.deepl.com/en/translator) performs the translation with the users API key

## Running

```bash
. sourceme

# Help
python3 gen_flash.py -h

# Mode A
python3 gen_flash.py test/english_short.txt th --translations test/thai_short.txt

# Mode B
python3 gen_flash.py test/english_short.txt th --deepl_key <PATH TO KEY> --deepl_lang_code TH

```

The language codes for gTTS audio genereration are [here](https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang) and the language codes for DeepL are [here](https://developers.deepl.com/docs/getting-started/supported-languages).
