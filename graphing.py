import mlconjug3
from verbecc import Conjugator
cg = Conjugator(lang='fr')
strthing = input("enter a sentence to conjugate -> ").lower()
#strthing = "je aller manger mes pommes. tu manger tes pommes, tu manger et avoir tes pommes. il manger ses pommes. on avoir manger ses pommes. elle manger ses pommes. nous manger nos pommes. vous manger vos pommes. ils manger leurs pommes. elles manger leurs pommes"
conidile = mlconjug3.Conjugator(language='fr')


verbs = open('verbs.txt').read().splitlines()
strthing = strthing.replace(".", ",")
sent = strthing.split(",")

subjects = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
plursing = ["1s", "2s", "3s", "3s", "3s", "1p", "2p", "3p", "3p"]
plursing2 = [1, 2, 3, 3, 3, 4, 5, 6, 6]
passe = ['ai', 'as', 'a', 'avons', 'avez', 'vont', 'suis', 'es', 'est','sommes', 'êtes', 'sont']
finalstring = ""

a1 = []
a2 = []
l=True
g=True
for sentence in sent:
	
	scent = sentence.split(" ")

	for j in subjects:
		if j in scent:
			a1.append(plursing[subjects.index(j)])
			a2.append(plursing2[subjects.index(j)])


#	if len(a1) == 0:
	k=0
	while len(a1) > 1:
		a1.pop(0)
		a2.pop(0)
	for i in scent:
		#futur proche
		if k>0:
			if scent[k-1].lower() == "aller":
				l=False
		#passé-composé
			if (scent[k-1].lower() == "avoir" or scent[k-1].lower() == "être") and i in verbs:
				l=False
				g=False
				converb = cg.conjugate(i)['moods']['indicatif']['passé-composé']
				if len(a1) > 1:
					a1.pop(0)
					a2.pop(0)
				cent = converb[a2[0]].split(" ")
				for c in cent:
					for q in subjects:
						if c == q:
							cent.remove(c)
						if cent[0] in passe:
							cent.remove(cent[0])
				finalstring += str(cent[0])
		if i in verbs and l:
			if len(a1)>0:
				converb = conidile.conjugate(i).conjug_info['Indicatif']['Présent'][a1[0]]
			#converb = cg.conjugate(a1[0])['moods']['indicatif']['présent']
			finalstring += converb
			
		elif i in verbs and g==False:
			pass
		else:
			finalstring += i
		finalstring +=" "
		
		k+=1
		l=True
		g=True

	finalstring = finalstring[:len(finalstring) -1]
	finalstring += ","

finalstring = finalstring[0:len(finalstring)-1] + "."
finalstring = finalstring.replace("je ai", "j'ai")
print(finalstring)