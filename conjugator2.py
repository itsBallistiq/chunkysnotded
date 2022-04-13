from verbecc import Conjugator
from napoleanbenepar import parsesub
cg = Conjugator(lang='fr')
subjects = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
plursing2 = [1, 2, 3, 3, 3, 4, 5, 6, 6]
verbs = open("verbs.txt", "r", encoding="utf8").read().splitlines()
preference = open("preference.txt", "r", encoding="utf8").read().splitlines()
passe = ['ai', 'as', 'a', 'avons', 'avez', 'vont', 'suis', 'es', 'est','sommes', 'êtes', 'sont']
strthing = input("enter a sentence to conjugate -> ").lower()

dictionary = {
	"subject": [],
	"conjugatables": [],
	"infinitives": [],
	"pasttense": []
}

def GoThrough(word, index):
	for i in dictionary["infinitives"]:
		for j in i:
			if word == j and index in i:
				return False
	for i in dictionary["pasttense"]:
		for j in i:
			if word == j and index in i:
				return False
	return True

def IsNegative(word, nextword, wordafterthat):
	if word in verbs:
		if nextword	== "pas" or nextword == "de" or nextword == "d\'" or nextword == "à":
			if wordafterthat in verbs:
				return True
	return False

def VerbParse(strthing):
	subs = parsesub(strthing)
	print(subs, "<---subs")
	strthing = strthing.replace(".", ",")
	sentances = strthing.split(",")
	for sentance in sentances:
		words = sentance.split(" ")
		while "" in words:
			words.remove("")
		for i in range(len(words)):
			if i < len(words):
				word = words[i]
			if word in subjects:
				dictionary["subject"].append([word, i])
			if i < len(words)-1 and word == "aller" and (words[i+1] in verbs or words[i+2] in verbs):
				if IsNegative(word, words[i+1], words[i+2]):
					dictionary["infinitives"].append([words[i+2], i+2])
				else:
					dictionary["infinitives"].append([words[i+1], i+1])
				dictionary["conjugatables"].append([word, i])
			elif i < len(words)-1 and (word == "avoir" or word == "être") and (words[i+1] in verbs or words[i+2] in verbs):
				if IsNegative(word, words[i+1], words[i+2]):
					dictionary["pasttense"].append([words[i+2], i+2])
				else:
					dictionary["pasttense"].append([words[i+1], i+1])
				dictionary["conjugatables"].append([word, i])
			elif word in preference:
				if IsNegative(word, words[i+1], words[i+2]):
					dictionary["infinitives"].append([words[i+2], i+2])
				else:
					dictionary["infinitives"].append([words[i+1], i+1])
				dictionary["conjugatables"].append([word, i])
			elif word in verbs and GoThrough(word, i):
				dictionary["conjugatables"].append([word, i])



def Conjugate():
	print(dictionary)
	for i in range(len(dictionary["subject"])):
		checksub = False
		if i < len(dictionary["subject"]):
			sub = dictionary["subject"][i][0]
			sublocate = dictionary["subject"][i][1]
			if i < len(dictionary["subject"])-1:
				nexsublocate = dictionary["subject"][i+1][1]
			else:
				nexsublocate = 2147483647
		#regular conjugations		
		for j in range(len(dictionary["conjugatables"])):
			if j < len(dictionary["conjugatables"]):
				verb = dictionary["conjugatables"][j][0]
				verblocate = dictionary["conjugatables"][j][1]
				if verblocate > nexsublocate:
					pass
				else:
					if verb in verbs:
						converbs = cg.conjugate(verb)['moods']['indicatif']['présent']
						if converbs[0][0:2] == "j'":
							converbs[0] = "je " + converbs[0][2:]
						for converb in converbs:
							converb = converb.split(" ")
							for i in converb:
								if sub == i:
									dictionary["conjugatables"][j][0] = converb[1]
		#past tense conjugations
		for j in range(len(dictionary["pasttense"])):
			if j < len(dictionary["pasttense"]):
				verb = dictionary["pasttense"][j][0]
				verblocate = dictionary["pasttense"][j][1]
				if verblocate > nexsublocate:
					pass
				else:
					if verb in verbs:
						converbs = cg.conjugate(verb)['moods']['indicatif']['passé-composé']
						if converbs[0][0:2] == "j'":
							converbs[0] = "je " + converbs[0][2:]
						for converb in converbs:
							converb = converb.split(" ")
							for i in converb:
								if sub == i:
									dictionary["pasttense"][j][0] = converb[2]

def Construct(strthing):
	dictindex = ["subject", "conjugatables", "infinitives", "pasttense"]
	strthing = strthing.replace(".", ",")
	strthing = strthing.replace(",", " ")
	strthing = strthing.split(" ")
	finalstring = ""
	for i in range(len(dictionary)):
		for j in dictionary[dictindex[i]]:
			strthing[j[1]] = j[0]
	for i in strthing:
		finalstring = finalstring + i + " "
	return finalstring


#print(converbs)
VerbParse(strthing)
Conjugate()
print(Construct(strthing))