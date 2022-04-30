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
def subverb(strthing):
    if type(strthing) == nltk.tree.Tree:
        if labellogic[strthing.label()][0] == [""]:
            return strthing
        for i in labellogic:
            if i == str(strthing.label()):
                for j in labellogic[i][0]:
                    if type(strthing._.children) == nltk.tree.Tree:
                        pass
            
                break

finalsubs = []
def findleaves(tree):
    leaves = tree.pos()
    print(leaves)
    tempsub = ""
    for leaf in range(len(leaves)):
        if leaf + 2 < len(leaves):
            if leaves[leaf+1][1] == "CC" and (leaves[leaf][0] == "moi" or leaves[leaf+2][0] == "moi"):
                tempsub = "nous"
            elif leaves[leaf+1][1] == "CC" and (leaves[leaf+2][0] == "toi" or leaves[leaf][0] == "toi"):
                tempsub = "vous"
            elif leaves[leaf+1][1] == "CC" and (leaves[leaf+2][1] == "CLS" or leaves[leaf+2][1] == "CLO"):
                if leaves[leaf+2][0] == "je" or leaves[leaf+2][0] == "nous":
                    tempsub = "nous"
                elif leaves[leaf+2][0] == "tu" or leaves[leaf+2][0] == "vous":
                    tempsub = "vous"
                elif leaves[leaf+2][0] == "ils" or leaves[leaf+2][0] == "il":
                    tempsub = "ils"
            elif leaves[leaf+1][1] == "CC" and (leaves[leaf+2][1] == "CLS" or leaves[leaf][1] == "CLO"):
                if leaves[leaf][0] == "je" or leaves[leaf][0] == "nous":
                    tempsub = "nous"
                elif leaves[leaf][0] == "tu" or leaves[leaf][0] == "vous":
                    tempsub = "vous"
                elif leaves[leaf][0] == "ils" or leaves[leaf][0] == "il":
                    tempsub = "ils"
            elif leaves[leaf+1][1] == "CC":
                tempsub = "ils"
            elif leaves[leaf][0] == "des" or leaves[leaf][0] == "les":
                if leaves[leaf+1][0] == "NC" or leaves[leaf+1][0] == "ADJ" and leaves[leaf+2][0] == "NC":
                    tempsub = "ils"
        elif leaves[leaf] == "moi" or leaves[leaf] == "je":
            tempsub = "je"
        elif leaves[leaf] == "toi" or leaves[leaf] == "tu":
            tempsub = "tu"
        else:
            tempsub = "il"
        if tempsub != "" and leaf+1 < len(leaves):
            if leaves[leaf+1][1] != "CC" and leaves[leaf+1][1] != "V" and leaves[leaf+1][1] != "VINF":
                tempsub = ""
                print("ignoring tempsub...")
            else:
                finalsubs.append([tempsub, leaf])
    #check for the right index for ____ CC ---> ____ instead of ---> ____ CC ____
    #update test cases
    return finalsubs




def parsesub(strthing):
    strthing = strthing.replace("?", ",")
    strthing = strthing.replace("!", ",")
    strthing = strthing.replace(".", ",")
    strthing = strthing.replace(",", "")
    sentence_words = strthing.split(" ")
    input_sentence = benepar.InputSentence(
        words = sentence_words
        )
    parsley = parser.parse(input_sentence)
    sent = parsley[0]
    findleaves(sent)
    for i in finalsubs:
        print(i)
    return finalsubs
    #sent.pretty_print()
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
        finalsubs = []

print(parsesub(strthing))