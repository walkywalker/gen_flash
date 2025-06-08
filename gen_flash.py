from gtts import gTTS, lang
import genanki
import argparse
import os
import deepl
from pathlib import Path

from question import *


DECK_ID = 0xd3397994
MODEL_ID_BASE = 0xbbcb1011


def deepl_translate(words, deepl_key, deepl_lang_code):
	translations = []
	print(f"Using DeepL API key: {deepl_key}")
	deepl_client = deepl.DeepLClient(deepl_key)
	usage = deepl_client.get_usage()
	print(f"DeepL monthly char quota: {usage.character.count}/{usage.character.limit}")

	if (usage.character.count + sum(len(word) for word in words)) >= usage.character.limit:
		raise RuntimeError("Insufficient DeepL quota")

	print(f"Translated:")
	for word in words:
		result = deepl_client.translate_text(word, target_lang=deepl_lang_code)
		print(f"{word}: {result.text}")
		translations.append(result.text)

	return translations

def check_input_file(file):
	if not os.path.exists(file):
		raise RuntimeError(f"{file} does not exist")

def parse_input_file(file):
	lines = []
	with open(file, "r") as file:
	    for line in file:
	        lines.append(line.strip("\n"))

	return lines

def generate_audio(words, gtts_lang_code):
	os.makedirs("audio", exist_ok=True)

	for word in words:
		filename = f"audio/{word}.mp3"
		if not os.path.exists(filename):
			print(f"Creating audio for {word}")
			tts = gTTS(word, lang=gtts_lang_code)
			tts.save(filename)

def get_question_formats():

	return [secondary_text_only,
			secondary,
			secondary_audio_only,
			primary]

def get_formatting():
	return '<div style="text-align: center; font-family: Arial; font-size: 40px; padding: 20px;">'

def generate_anki_deck_genanki(source, translations):

	deck = genanki.Deck(DECK_ID, 'deck')

	for question_format_idx, question_format in enumerate(get_question_formats()):

		qfmt = get_formatting() + '{{Question}}'
		afmt = '{{FrontSide}}<hr id="answer">{{Answer}}'

		if question_format.Q_AUDIO:
			qfmt += '<br>{{MyMedia}}'
		else:
			afmt += '<br>{{MyMedia}}'

		model = genanki.Model(MODEL_ID_BASE + question_format_idx,
	  						 'model',
							  fields=[
							    {'name': 'Question'},
							    {'name': 'Answer'},
							    {'name': 'MyMedia'}, 
							  ],
							  templates=[
							    {
							      'name': 'Card 1',
							      'qfmt': qfmt,              
							      'afmt': afmt,
							    },
							  ],
							  )

		for word0, word1 in zip(source, translations):
			question = question_format(word0, word1)
			fields = [question.get_question(), question.get_answer(), f"[sound:{word1}.mp3]"]
			note = genanki.Note(model=model,
				  			    fields=fields)

			deck.add_note(note)

	return deck

def get_deepl_lang_codes():
	# Copied from deepl docs
	return [
	    "AR", "BG", "CS", "DA", "DE", "EL", "EN", "ES", "ET", "FI", "FR", "HE",
	    "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "RO",
	    "RU", "SK", "SL", "SV", "TH", "TR", "UK", "VI", "ZH"
	]


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A simple demo script.")
	parser.add_argument("source", help="Text file containing primary language")
	parser.add_argument("gtts_lang_code", choices=list(lang.tts_langs().keys()), help="language code for gTTS")
	parser.add_argument('--translations', type=str, help='Text file containing corresponding translations. If provided this will be used instead of using DeepL ')
	parser.add_argument('--deepl_key', type=str, help='Text file containing DeepL API key')
	parser.add_argument('--deepl_lang_code', choices=get_deepl_lang_codes(), help='language code for DeepL')

	args = parser.parse_args()

	check_input_file(args.source)
	source = parse_input_file(args.source)
	translations = None

	if args.translations:
		check_input_file(args.translations)
		translations = parse_input_file(args.translations)
	elif args.deepl_key is None:
		raise RuntimeError("If no translations have been provided a DeepL API key needs to be provided (https://www.deepl.com)")
	elif args.deepl_lang_code is None:
		raise RuntimeError("Use --deepl_lang_code to provide the language code (https://developers.deepl.com/docs/getting-started/supported-languages)")
	else:
		deepl_key = parse_input_file(args.deepl_key)[0]
		translations = deepl_translate(source, deepl_key, args.deepl_lang_code)

	assert len(source) == len(translations)

	generate_audio(translations, args.gtts_lang_code)

	deck = generate_anki_deck_genanki(source, translations)

	package = genanki.Package(deck)
	package.media_files = [f"audio/{word}.mp3" for word in translations]
	package_filename = f'{Path(args.source).stem}_{args.gtts_lang_code}.apkg'
	package.write_to_file(package_filename)
	print(f"Generated {package_filename}")
