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
subby = []
def resetsubby():
	global subby
	del subby
	subby= []
	return subby

def subverb(strthing, subby):
	for k in strthing:
		if type(k[0]) != str:
			subverb(k, subby)
		else:
			subby.append(str(k))

	coordfound = False
	subfound = False
	profound = None
	newsub=[]
	for j in range(len(subby)):
		newsub.append(subby[j].replace("(", "").replace(")", "").split(" "))
	for i in range(len(newsub)):
		print(newsub[i][0])
		if newsub[i][0] == "NC" or newsub[i][0] == "CLS" or newsub[i][0] == "CLO" or newsub[i][0] == "PRO":
			if newsub[i+1][0] != "CC" or newsub[i+1][0] != "VINF" or newsub[i+1][0] != "V":
				print("this code is shit")
			else:
				subfound = True
				if newsub[i][1] == "toi" or newsub[i+2][1] == "toi":
					profound = "toi"
				if newsub[i][1] == "moi" or newsub[i+2][1] == "moi":
					profound = "moi"
				if newsub[i+1][0] == "CC":
					coordfound = True

	return newsub, coordfound, subfound, profound


def parsesub(strthing):
	sentence_words = strthing.split(" ")
	input_sentence = benepar.InputSentence(
		words = sentence_words
		)
	parsley = parser.parse(input_sentence)
	sent = parsley[0]
	nps = subverb(sent, subby)
	print(nps)
	resetsubby()
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