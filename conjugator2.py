from verbecc import Conjugator
cg = Conjugator(lang='fr')
subjects = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
plursing2 = [1, 2, 3, 3, 3, 4, 5, 6, 6]
verbs = open("verbs.txt", "r", encoding="utf8").read().splitlines()
preference = open("preference.txt", "r", encoding="utf8").read().splitlines()
passe = ['ai', 'as', 'a', 'avons', 'avez', 'vont', 'suis', 'es', 'est','sommes', 'êtes', 'sont']




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
	#subs = parsesub(strthing)
	#print(subs, "<---subs")

  #for sentance in sentances:
  words = strthing.split(" ")
  while "" in words:
    words.remove("")
  for i in range(len(words)):
    if i < len(words):
      word = words[i]
    if word in subjects:
      dictionary["subject"].append([word, i])
    try:
      if i < len(words)-1 and word == "aller" and (words[i+1] in verbs or words[i+2] in verbs):
        if IsNegative(word, words[i+1], words[i+2]):
          dictionary["infinitives"].append([words[i+2], i+2])
        else:
          dictionary["infinitives"].append([words[i+1], i+1])
        dictionary["conjugatables"].append([word, i])
      elif i < len(words)-1 and (word == "avoir" or word == "être") and (words[i+1] in verbs):
        dictionary["pasttense"].append([words[i+1], i+1])
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
    except:
      pass
    if word in verbs and GoThrough(word, i):
      dictionary["conjugatables"].append([word, i])



def Conjugate():
	for i in range(len(dictionary["subject"])):
		if i < len(dictionary["subject"]):
			sub = dictionary["subject"][i][0]
			#sublocate = dictionary["subject"][i][1]
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
  vowels = ["a", "e", "h", "i", "o", "u", "y", "é", "à", "è", "ù", "â", "ê", "î", "ô", "û", "ë", "ï", "ü"]
  dictindex = ["subject", "conjugatables", "infinitives", "pasttense"]
  strthing = strthing.split(" ")
  finalstring = ""
  for i in range(len(dictionary)):
    for j in dictionary[dictindex[i]]:
      strthing[j[1]] = j[0]
  for i in range(len(strthing)):
    try:
      if strthing[i] != strthing[i-1]:
        finalstring = finalstring + strthing[i] + " "
    except:
      finalstring = finalstring + strthing[i] + " "
  for j in range(len(finalstring)):
    if j + 5 != len(finalstring):
      for i in vowels:
        if finalstring[j:j+4] == "je " + i:
          finalstring = finalstring.replace(finalstring[j:j+4], ("j'" + i))
        if finalstring[j:j+4] == "ne " + i:
          finalstring = finalstring.replace(finalstring[j:j+4], ("n'" + i))
        if finalstring[j:j+4] == "de " + i:
          finalstring = finalstring.replace(finalstring[j:j+4], ("d'" + i))
  
  
  return finalstring


#print(converbs)
strthing = input("enter a sentence to conjugate (verbs at the infinitive) -> ").lower()
sentances = strthing.split(".")
if len(sentances) == 1:
  print(len(sentances), "Sentence Found. Conjugating...")
else:
  print(len(sentances), "Sentences Found. Conjugating...")
for sentance in sentances:
  dictionary = {
	"subject": [],
	"conjugatables": [],
	"infinitives": [],
	"pasttense": []
}
  VerbParse(sentance)
  print(dictionary)
  Conjugate()
  print(dictionary)
  print("Congjugated Sentence: ", Construct(sentance))