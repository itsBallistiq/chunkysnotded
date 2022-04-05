from verbecc import Conjugator
cg = Conjugator(lang='fr')
subjects = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
plursing2 = [1, 2, 3, 3, 3, 4, 5, 6, 6]
verbs = open("verbs.txt", "r", encoding="utf8").read().splitlines()
preference = open("preference.txt", "r", encoding="utf8").read().splitlines()
passe = ['ai', 'as', 'a', 'avons', 'avez', 'vont', 'suis', 'es', 'est','sommes', 'êtes', 'sont']

def SentanceConstruct(words, conjugated, subject, unconjugated, infinitifetpasse):
	finalsentance = ""
	for word in words:
		if word == unconjugated:
			finalsentance = finalsentance + conjugated[1]
		elif word == infinitifetpasse:
			finalsentance = finalsentance + conjugated[2]
		else:
			finalsentance = finalsentance + word
		finalsentance = finalsentance + " "
	return finalsentance


def IsFeminine(subject):
	if subject == "elle":
		subject = "il"
		return subject, 1
	if subject == "elles":
		subject = "ils"
		return subject, 2
	return subject, 0


def Present(subject, verb):
	subjectverb = []
	converbs = cg.conjugate(verb)['moods']['indicatif']['présent']
	fem = IsFeminine(subject)[1]
	subject = IsFeminine(subject)[0]
	for converb in converbs:
		if subject in converb:
			converb = converb.split(" ")
			if fem == 1:
				subjectverb.append("elle")
			elif fem == 2:
				subjectverb.append("elles")
			else:
				subjectverb.append(converb[0])
			subjectverb.append(converb[1])
			subjectverb.append("")
			return subjectverb
		if subject == "je" and "j'" in converb:
			subjectverb.append(converb[0])
			subjectverb.append("")
			subjectverb.append("")

			return subjectverb



def Future(subject, verb):
	subjectallerverb = []
	converbs = cg.conjugate("aller")['moods']['indicatif']['présent']
	fem = IsFeminine(subject)[1]
	subject = IsFeminine(subject)[0]
	for converb in converbs:
		if subject in converb:
			converb = converb.split(" ")
			if fem == 1:
				subjectallerverb.append("elle")
			elif fem == 2:
				subjectallerverb.append("elles")
			else:
				subjectallerverb.append(converb[0])
			subjectallerverb.append(converb[1])
			subjectallerverb.append(verb)
			return subjectallerverb


def Preference(subject, verb):
	subjectallerverb = []
	converbs = cg.conjugate(verb)['moods']['indicatif']['présent']
	fem = IsFeminine(subject)[1]
	subject = IsFeminine(subject)[0]
	for converb in converbs:
		if subject in converb:
			converb = converb.split(" ")
			if fem == 1:
				subjectallerverb.append("elle")
			elif fem == 2:
				subjectallerverb.append("elles")
			else:
				subjectallerverb.append(converb[0])
			subjectallerverb.append(converb[1])
			subjectallerverb.append(verb)
			return subjectallerverb


def Past(subject, avoirouetre, verb, words, index):
	subjectavoirouetreverb = []
	converbs = cg.conjugate(verb)['moods']['indicatif']['passé-composé']
	fem = IsFeminine(subject)[1]
	subject = IsFeminine(subject)[0]
	for converb in converbs:
		if subject in converb:
			converb = converb.split(" ")
			if fem == 1:
				subjectavoirouetreverb.append("elle")
			elif fem == 2:
				subjectavoirouetreverb.append("elles")
			else:
				subjectavoirouetreverb.append(converb[0])
			subjectavoirouetreverb.append(converb[1])
			subjectavoirouetreverb.append(converb[2])
			words[index+1] = converb[1]
			words[index+2] = converb[2]
			return subjectavoirouetreverb, words
		if subject == "je" and "j'" in converb:
			converb = converb.split(" ")
			subjectavoirouetreverb.append(converb[0])
			subjectavoirouetreverb.append(converb[1])
			subjectavoirouetreverb.append("")
			words[index] = converb[0]
			words.pop(index+1)
			words[index+1] = converb[1]
			return subjectavoirouetreverb, words



def ConSentance(strthing):
	strthing = strthing.replace(".", ",")
	strthing = strthing.lower()
	sentances = strthing.split(",")
	subjectstack = []
	finalstring = ""
	for sentance in sentances:
		words = sentance.split(" ")
		while "" in words:
			words.remove("")
		currentsub = ""
		currentsublocated = 0
		allerfound = False
		for i in range(len(words)):
			if i < len(words):
				word = words[i]
			if word == "aller":
				allerfound = True
			if word in subjects:
				currentsub = word
				subjectstack.append(currentsub)
				if len(subjectstack) > 1:
					subjectstack.pop(0)
					currentsub = subjectstack[0] # <--------- redundant but better safe than sorry
				currentsublocated = i
			if i < len(words)-1 and allerfound and word in verbs and word != "aller":
				converb = Future(currentsub, word)
				finalstring = finalstring +  SentanceConstruct(words, converb, currentsub, "aller", word) + "\n"
			elif i < len(words)-1 and (word == "avoir" or word == "être") and words[i+1] in verbs:
				converb = Past(currentsub, word, words[i+1], words, currentsublocated)
				finalstring = finalstring +  SentanceConstruct(converb[1], converb[0], currentsub, word, "") + "\n"
			elif word in preference:
				converb = Preference(currentsub, word)
				finalstring = finalstring +  SentanceConstruct(words, converb, currentsub, word, "") + "\n"
			elif word in verbs and (word[i-1] not in passe):
				converb = Present(currentsub, word)
				finalstring = finalstring + SentanceConstruct(words, converb, currentsub, word, "") + "\n"
	print(finalstring)
				
ConSentance(strthing = input("enter a sentence to conjugate -> ").lower())
#fix multiple verbs going through different conjugations in a weird way (try entering "je avoir manger une pomme et aller manger une pomme, tu manger une pomme")
#add negative (is it better to recognize the negative pieces or is it better to deconstruct the sentance? If we deconstruct the sentance we will have to be careful about multiple negatives in one sentance)
#add more "preference" verbs (more verbs where the verb will be after and will be at the infinitive)
#make it so that "preference" verbs with multiple words (like arriver à) can work with keeping the next verb at the infinitive
#add a way to grab unique subjects
#maybe we should grab subjects first because it might also just give us a way to grab the verb too or something and that could be helpful except very maddening because it would mean that we would have to rework this entire system AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

