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
nlp = spacy.load('fr_core_news_lg')

# if spacy.__version__.startswith('2'):
#     nlp.add_pipe(benepar.BeneparComponent("benepar_fr2"))
# else:
#     nlp.add_pipe("benepar", config={"model": "benepar_fr2"})
def subconvert(tree):
	subs = []
	for i in tree:
		if i.label() == "COORD":
			subs.append(subconvert(i[1]))
		else:
			subs.append(i[0])
	if "moi" in subs or "nous" in subs:
		return "nous"
	if "toi" in subs or "vous" in subs:
		return "vous"
	if len(subs) == 1:
		return "il"
	else:
		return "ils"
def subverb(parenttree):
	print(parenttree)
	npfound = None
	coordfound = None
	vfound = False
	for i in parenttree:
		if i.label() == "NPP" or i.label() == "NP" and npfound == None:
			npfound = i
		if "V" in i.label():
			vfound = True
		print(i)
		if i.label() == "COORD":
			coordfound = i
	if vfound and coordfound != None:
		return npfound, subverb(coordfound)
	elif vfound:
		return npfound
	else:
		return None

def parsesub(strthing):
	#sentence = "pommes et toi adorer manger des pommes, et pommes aimer manger des pommes"
	sentence_words = strthing.split(" ")
	input_sentence = benepar.InputSentence(
		words = sentence_words
		)
	parsley = parser.parse(input_sentence)
	sent = parsley[0]
	nps = subverb(sent)
	compressedsubs = []
	for np in nps:
		compressedsubs.append(subconvert(np)) 
	return compressedsubs

strthing = input("enter a sentence to conjugate -> ").lower()
print(parsesub(strthing))
#look for VINF checking (VN in vinf), Ssub, Srel
#we need to get the location of the subjects that we are returning, so that we can append it to the subjects key in the dictionary. for multiple subjects, it should just work if we take the farthest part of the subject to the right as the index.