import googletrans
from googletrans import Translator

translator = Translator()


def translate(text):
    return translator.translate(text, dest='de').text
