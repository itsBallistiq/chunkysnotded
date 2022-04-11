import benepar, nltk, spacy
import ssl


# Used to download language models
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# benepar.download('benepar_fr2') # French Model

parser = benepar.Parser("benepar_fr2")
# nlp = spacy.load('fr_core_news_lg')

# if spacy.__version__.startswith('2'):
#     nlp.add_pipe(benepar.BeneparComponent("benepar_fr2"))
# else:
#     nlp.add_pipe("benepar", config={"model": "benepar_fr2"})

sentence = "Eddie adorer manger des pommes et tu aimer manger des pommes"
sentence_words = sentence.split(" ")

input_sentence = benepar.InputSentence(
	words = sentence_words
	)

#a = parser.parse(sentence)
b = parser.parse(input_sentence)

#print(a)
print(b.pos())