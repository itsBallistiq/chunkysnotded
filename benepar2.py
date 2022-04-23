import benepar, nltk, spacy
import ssl
subjects = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]

tests = {
	"je manger une pomme": ["je"],
	"tu manger une pomme": ["tu"],
	"leurs avions voler de paris": ["ils"],
	"marc et luis manger une pomme": ["ils"],
	"mon fils voler une pomme": ["il"],
	"marc et luis manger des pommes et vous manger des bananes": ["ils", "vous"],
	"je aller manger une pomme": ["je"],
	"marc et luis aller manger des pommes": ["ils"],
	"ma famille et moi aller manger une pomme ce soir": ["nous"],
	"il aller manger des oranges que boire de l'eau": ["il", "ils"],
	"Romaine et Cristophe choisir un vol air france": ["ils"],
	"quand Romaine faire enregistrer ses bagages, il choisir aussi sa place": ["il", "il"],
	"pendant le voyage, les deux garçons avoir faim. Ils finir tout leur repas": ["ils", "ils"],
	"après, ils remplir leur carte de débarquement": ["ils"],
	"leur avion atterir à new york à 2 h 45": ["il"],
	"on vendre des billets de train au guichet": ["il"],
	"les voyageurs attendre dans la salle d'attente": ["ils"],
	"je entendre l'annonce du départ de notre train": ["je"],
	"nous perdre patience quand le train du retard": ["nous"],
	"le contrôleur répondre aux questions des voyageurs": ["il"],
	"vous descendre à quel arrêt": ["vous"],
	"moi, je descendre à toulouse": ["je"],
	"": [""]
}

labellogic = {
	"NP": [["NC", "COORD", "Srel", "NP", "NPP", "PRO", "SINT", "Ssub"], ["COORD"]],
	"NPP": [["NP", "COORD"], ["COORD"]],
	"COORD": [["NP", "NPP", "VN"], ["VPinf", "NPP", "NP"]],
	"VPinf": [["VINF", "VN", "COORD"], [""]],
	"VN": [["CLS", "CLO"], ["COORD", "SINT", "VPinf"]],
	"SINT": [["VN"], [""]],
	"Ssub": [["NP"], ["NP"]],
	"Srel": [["NP"], ["NP"]],
	"PRO": [[""], ["NP"]],
	"NC": [[""], ["NP"]],
	"CLS": [[""], ["VN"]],
	"CLO": [[""], ["VN"]], 
}

parser = benepar.Parser("benepar_fr2")
nlp = spacy.load('fr_core_news_lg')
subfound = False
profound = False
coordfound = None
verbfound = False
def thankspython():
	global subfound, profound, coordfound, verbfound
	del subfound, profound, coordfound, verbfound
	subfound = False
	profound = False
	coordfound = None
	verbfound = False

def subverb(strthing):
	global subfound, profound, coordfound, verbfound
	
	print("sub me ---> " ,subfound)
	for j in range(len(strthing)):
		if len(strthing[j])>1:
			if type(strthing[j][0]) == str:
				strthing = str(strthing).replace("(", "")
				strthing = strthing.replace(")", "")
				strthing = strthing.split(" ")
				if strthing[0] == "NC"  or strthing[0] == "CLS" or strthing[0] == "CLO" or strthing[0] == "NPP":
					subfound = True 
				if strthing[0] == "PRO":
					profound = True
				if strthing[0] == "COORD":
					coordfound = True
				if strthing[0] == "VPinf" or strthing[0] == "V" or strthing[0] == "VINF":
					verbfound = True
			else:	
				for i in range(len(strthing[j])):
					subverb(strthing[j][i])
	return subfound, profound, coordfound, verbfound





def parsesub(strthing):
	sentence_words = strthing.split(" ")
	input_sentence = benepar.InputSentence(
		words = sentence_words
		)
	parsley = parser.parse(input_sentence)
	sent = parsley[0]
	nps = subverb(sent)
	for np in nps:
		print (np)
	thankspython()
	# compressedsubs = []
	# if len(nps) == 2:
	# 	compressedsubs.append(subconvert(nps))
	# else:
	# 	for np in nps:
	# 		compressedsubs.append(subconvert(np)) 
	# return compressedsubs

czech = input("would you like to manually enter a test? -> ").lower()
if czech == "yes":
	strthing = input("enter a sentence to conjugate -> ").lower()
else:
	for test in tests:
		strthing = test
		answer = parsesub(strthing)
		if answer == tests[test]:
			print("test: <" + test + "> has passed")
		else:
			print("test: <" + test + "> has failed, returned: ", answer)

print(parsesub(strthing))
#need to change coord to actually work with multiple subjects
#need to figure out how to use global variables
#need to figureout how to use python
#i hate this it sucks so badly
#we need to get the location of the subjects that we are returning, so that we can append it to the subjects key in the dictionary. for multiple subjects, it should just work if we take the farthest part of the subject to the right as the index.