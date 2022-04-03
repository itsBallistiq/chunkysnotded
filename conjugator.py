from verbecc import Conjugator
cg = Conjugator(lang='fr')
subjects = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
plursing2 = [1, 2, 3, 3, 3, 4, 5, 6, 6]
verbs = open('verbs.txt').read().splitlines()
def SentanceConstruct(words, conjugated, subject, unconjugated, infinitifetpasse):
	finalsentance = ""
	for word in words:
		if len(conjugated) > 2:

			if word == unconjugated:
				finalsentance = finalsentance + conjugated[1]
			elif word == infinitifetpasse:
				finalsentance = finalsentance + conjugated[2]
			else:
				finalsentance = finalsentance + word
			finalsentance = finalsentance + " "
			return finalsentance
		#checks for j'ai or j'
		'''else:
			print(word, unconjugated)
			if word == unconjugated:
				finalsentance = finalsentance + conjugated[0]
			elif word == infinitifetpasse:
				finalsentance = finalsentance + conjugated[1]
			elif word == subject:
				pass
			else:
				finalsentance = finalsentance + word
			finalsentance = finalsentance + " "
	return finalsentance[1:len(finalsentance)]'''


def Present(subject, verb):
	subjectverb = []
	print(verb)
	converbs = cg.conjugate(verb)['moods']['indicatif']['présent']
	print(converbs)
	for converb in converbs:
		if subject in converb:
			converb = converb.split(" ")
			subjectverb.append(converb[0])
			subjectverb.append(converb[1])
			print(subjectverb)
			return subjectverb
		if subject == "je" and "j'" in converb:
			subjectverb.append(converb[0])

			return subjectverb



def Future(subject, verb):
	subjectallerverb = []
	converbs = cg.conjugate("aller")['moods']['indicatif']['présent']
	for converb in converbs:
		if subject in converb:
			converb = converb.split(" ")
			subjectallerverb.append(converb[0])
			subjectallerverb.append(converb[1])
			subjectallerverb.append(verb)
			return subjectallerverb

def Preference():
	pass

def Past(subject, avoirouetre, verb):
	subjectavoirouetreverb = []
	passe = ['ai', 'as', 'a', 'avons', 'avez', 'vont', 'suis', 'es', 'est','sommes', 'êtes', 'sont']
	converbs = cg.conjugate(verb)['moods']['indicatif']['passé-composé']
	for converb in converbs:
		if subject in converb:
			converb = converb.split(" ")
			subjectavoirouetreverb.append(converb[0])
			subjectavoirouetreverb.append(converb[1])
			subjectavoirouetreverb.append(converb[2])
			return subjectavoirouetreverb
		if subject == "je" and "j'" in converb:
			converb = converb.split(" ")
			subjectavoirouetreverb.append(converb[0])
			subjectavoirouetreverb.append(converb[1])
			return subjectavoirouetreverb
def ConSentance(strthing):
	
	#strthing = "je aller manger mes pommes et manger tes pommes, tu manger et avoir tes pommes. il manger ses pommes. on avoir manger ses pommes. elle manger ses pommes. nous manger nos pommes. vous manger vos pommes. ils manger leurs pommes. elles manger leurs pommes"
	strthing = strthing.replace(".", ",")
	strthing = strthing.lower()
	sentances = strthing.split(",")
	for sentance in sentances:
		words = sentance.split(" ")
		currentsub = ""
		allerfound = False
		for i in range(len(words)):
			word = words[i]
			if word == "aller":
				allerfound = True
			if word in subjects:
				currentsub = word
			if i < len(words)-1 and allerfound and word in verbs and word != "aller":
				converb = Future(currentsub, word)
				constructedsentance = SentanceConstruct(words, converb, currentsub, "aller", word)
				print(constructedsentance)
			if i < len(words)-1 and (word == "avoir" or word == "être") and words[i+1] in verbs:
				converb = Past(currentsub, word, words[i+1])
				constructedsentance = SentanceConstruct(words, converb, currentsub, word, words[i+1])
				print(constructedsentance)
			elif word in verbs:
				converb = Present(currentsub, word)
				print(converb)
				constructedsentance = SentanceConstruct(words, converb, currentsub, word, "")
				print(constructedsentance)
ConSentance(strthing = input("enter a sentence to conjugate -> ").lower())