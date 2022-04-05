from PIL import Image
import pytesseract
import cv2
import imutils
from imutils.contours import sort_contours
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import emnist
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import mlconjug3
from verbecc import Conjugator

#ia numero un
num_classes = 47
x_train, y_train = emnist.extract_training_samples("balanced")
x_test, y_test = emnist.extract_test_samples("balanced")
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)
# convert class vectors to binary class matrices
#print(y_train, y_test)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
#print('x_train shape:', x_train.shape)
#print(x_train.shape[0], 'train samples')
#print(x_test.shape[0], 'test samples')
batch_size = 128
epochs = 1
ydata = [0]
#ydata = np.array([])

#model = Sequential()
#model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=input_shape))
#model.add(Conv2D(64, (3, 3), activation='relu'))
#model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.25))
#model.add(Flatten())
#model.add(Dense(256, activation='relu'))
#model.add(Dropout(0.5))
#model.add(Dense(num_classes, activation='softmax'))
model = load_model('emnist.h5')
for epochnum in range(0):
  model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(),metrics=['accuracy'])
  hist = model.fit(x_train, y_train,batch_size=batch_size,epochs=epochs,verbose=0,validation_data=(x_test, y_test))
  
  if ydata[0] == 0:
  	print("[" + str(epochnum + 1) + "], " + str(hist.history['accuracy']) + "Fetching First Data")
  else:
  	if ydata < hist.history['accuracy']:
  		print("[" + str(epochnum + 1) + "], " + str(hist.history['accuracy']) + "[Greater Than Previous Accuracy]")
  	if ydata > hist.history['accuracy']:
  		print("[" + str(epochnum + 1) + "], " + str(hist.history['accuracy']) + "[Less Than Previous Accuracy]")
  	if ydata == hist.history['accuracy']:
  		print("[" + str(epochnum + 1) + "], " + str(hist.history['accuracy']) + "What the hell happened here?")
  	pass
  ydata = hist.history['accuracy']
  f = open("ydata.txt", "a")
  f.write(str(hist.history['accuracy']))
  f.write('\n')
  f.close()
  model.save('emnist.h5')
  #np.savetxt("ydata.txt", ydata, delimiter=',',header='Accuracy',fmt='%s', comments='')
print("The model has successfully trained")

print("Saving the model as emnist.h5")

#graphing thing

#xdata = np.linspace(1,epochnum,10)


#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#ax.plot(xdata, ydata)
#plt.show()

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
strthing = pytesseract.image_to_string(Image.open('french thing.png'), lang='fra')
print(strthing)
accent = ["?", " ", ".", "!", ",", "-", "\"", "\n", ";", ":", "'", "ë", "ï", "ü", "à", "è", "ì", "ò", "ù", "â", "ê","î", "ô", "û", "é", "ç"]
formatstring = ""

#sorts through input string to make a new better formatted string
for i in range(len(strthing)):
	if strthing[i-1] == "_" and strthing[i+1] == "_":
		formatstring += "_"
	elif strthing[i].isalpha() or strthing[i] in accent:
		formatstring += strthing[i]
	elif strthing[i] == "’":
		formatstring += "'"
	else:
		formatstring += "_"


print(formatstring)



#makes a videocapture
cv2.namedWindow("vitrine")
videocapture = cv2.VideoCapture(0)


'''print("What image source do you want to use?")
z = input("Camera / File")
if z.upper() == "FILE":
	y = input("What is the file name? (Case sensitive, Include file type in response)")'''

def VerbPlacement(strthing):
	verb = ""
	newstring = ""
	underscore = 0
	for j in strthing:
		if j[0] == "(":
			verb = j[1:].replace(")", " ")

	for i in strthing:
		if i[0] == "_":
			newstring += verb
		else:
			newstring += i

	return newstring




def Conjugate(strthing):
	cg = Conjugator(lang='fr')
	#strthing = input("enter a sentence to conjugate -> ").lower()
	#strthing = "je aller manger mes pommes. tu manger tes pommes, tu manger et avoir tes pommes. il manger ses pommes. on avoir manger ses pommes. elle manger ses pommes. nous manger nos pommes. vous manger vos pommes. ils manger leurs pommes. elles manger leurs pommes"
	conidile = mlconjug3.Conjugator(language='fr')


	verbs = open('verbs.txt').read().splitlines()
	strthing = strthing.replace(".", ",")
	strthing = strthing.lower()
	sent = strthing.split(",")
	cent = VerbPlacement(sent)

	subjects = ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"]
	plursing = ["1s", "2s", "3s", "3s", "3s", "1p", "2p", "3p", "3p"]
	plursing2 = [1, 2, 3, 3, 3, 4, 5, 6, 6]
	passe = ['ai', 'as', 'a', 'avons', 'avez', 'vont', 'suis', 'es', 'est','sommes', 'êtes', 'sont']
	finalstring = ""

	a1 = []
	a2 = []
	l=True
	g=True

	for sentence in cent:
		
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


def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    filereader(filename)

def filereader(filename):
	strthing = pytesseract.image_to_string(Image.open(filename), lang='fra+eng')
	Conjugate(strthing)
def camera(event=None):
	if videocapture.isOpened():
		rvalve,frame = videocapture.read()
	else:
		rvalve = False
	while rvalve:
		cv2.imshow("vitrine", frame)
		rvalve,frame = videocapture.read()
		qui = cv2.waitKey(100)
		#close on x press window
		if cv2.getWindowProperty("vitrine", 0) < 0:
			break
		#close with escape
		if qui == 27:
			break
		#take picture with tab
		if qui == 9:
			cv2.imwrite("amon coding thing.jpeg", frame)
			print("Image saved")
			image = cv2.imread('amon coding thing.jpeg')
			grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(grey, (5,5), 0)
			canny = cv2.Canny(grey, 30, 150)
			contrare = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			contrare = imutils.grab_contours(contrare)
			contrare = sort_contours(contrare, method="left-to-right")[0]
			chars=[]
			for i in contrare:
				(x, y, w, h) = cv2.boundingRect(i)
				if(w>=5 and w<=150) and (h>=15 and h<=120):
					boi = grey[y:y + h, x:x + w]
					thrash = cv2.threshold(boi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
					(tH, tW) = thrash.shape
					if tW > tH:
						thrash = imutils.resize(thrash, width=32)
					else:
						thrash = imutils.resize(thrash, height=32)
					(tH, tW) = thrash.shape
					dX = int(max(0,32 - tW) / 2.0)
					dY = int(max(0,32 - tH) / 2.0)
					padded = cv2.copyMakeBorder(thrash, top=dY, bottom=dY, left=dX, right=dX, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))
					padded = cv2.resize(padded, (32, 32))
					padded = padded.astype("float32") / 255.0
					padded = np.expand_dims(padded, axis=-1)
					chars.append((padded, (x,y,w,h)))
			boxes = [b[1] for b in chars]
			chars = np.array([i[0] for i in chars], dtype="float32")
			#preds = model.predict(chars)
			labelNames = "0123456789"
			labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
			um = accent.copy()
			for a in labelNames:
				um.append(a) 
			'''for (pred, (x, y, w, h)) in zip(preds, boxes):
				i = np.argmax(pred)
				prob = pred[i]
				label = labelNames[i]
				print("[INFO] {} - {:.2f}%".format(label, prob * 100))
				cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.putText(image, label, (x - 10, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
				cv2.imshow("Image", image)
				cv2.waitKey(0)'''
			print(contrare)
			strthing = pytesseract.image_to_string(canny, lang='fra+eng')
			cv2.imwrite("graymon coding thing.jpeg", grey)
			cv2.imwrite("graymon bluring thing.jpeg", blur)
			cv2.imwrite("graymon bluring thinny.jpeg", canny)
			print(strthing)
	#OCR

root = tk.Tk()
root.geometry("400x400")
button1 = tk.Button(root, text='Upload file', command=UploadAction)
button1.pack()
button2 = tk.Button(root, text='OpenCamera', command=camera)
button2.pack()
root.mainloop()

#fix not conjugating to passe compose with line break?
#make it put the verb in parentheses into the underlined area unconjugated