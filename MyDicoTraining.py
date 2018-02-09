# MyDicoTraining : Boite de dialogue d'entrainement
# -----------------------------------------------------------

_DEBUG_=True

# -----------------------
# Importation des modules
# -----------------------
import tkinter
from tkinter import *
from tkinter.font import *
from tkinter.constants import *
from tkinter.messagebox import *
from MyDico import  *
from MyDicoApp import *

# -----------
# Constantes
# -----------
EN_TO_FR = 'En_To_Fr'
FR_TO_EN = 'Fr_To_En'
FRAME_DEFAULT = 'DefaultFrame'

CHECKOK_MSG = 'Juste'
CHECKOK_COLOR = 'green'
CHECKKO_MSG = 'Erreur'
CHECKKO_COLOR = 'red'


# ***************************
# *  Classe MyDicoTraining  *
# ***************************
class MyDicoTraining(Frame):
	# ------------ Attributs de la classe ------------
	Dico = None			# Dictionnaire
	Mode = None			# Méthode d'entrainement : En vers Fr, ou Fr vers En
	CurrentTranslate = None	# Traduction courante
	
	WordAskLbl = None	# Mot-Question
	InfoLbl = None		# Info complémentaire
	WordAns = None		# Mot-Réponse
	StatLblFrame = None	# Zone de statistique
	StatNbLbl = None	# Nombre de proposition
	StatNbOkLbl = None	# Nombre de réponse Ok
	StatNbKoLbl = None	# Nombre de réponse Ko
	StatReussite = None	# Pourcentage de réussite
	CheckBtn = None		# Bouton de controle de la réponse
	CloseBtn = None		# Bouton de sortie
	ResultFrame = None	# Zone de résultat
	ResultLbl = None	# Résultat
	ResultAskLbl = None	# Résultat : mot proposé
	ResultSaisieLbl = None # Résultat : Réponse faite
	ResultAnsLbl = None # Résultat : Réponse 
	RésulStatLbl = None # Résultat : Taux de réussite
	
	# ------------ Constructeurs ------------
	def __init__(self,master, dico, mode = EN_TO_FR):
		"Contructeur de la classe MyDicoTraining"
		Frame.__init__(self, master)
		
		# Référence au dictionnaire
		self.Mode=mode
		self.Dico = dico
		
		# Contruction du GUI
		self.makeGUI()
		
		# Selection d'un premier mot
		self.askWord()
	#\ __init__	
	
	# ------------ Méthodes GUI ------------
	def makeGUI(self):
		"Construction de l'interface GUI"
		
		# Titre de la fenêtre
		self.titleLbl = Label(self)
		self.titleLbl.grid(row=0, column=0, columnspan=3, padx=5, pady=10)
		
		# Mot proposé
		self.WordAskLbl_ = Label(self)
		self.WordAskLbl_.grid(row=1, column=0, sticky=E, padx=5, pady=5)
		self.WordAskLbl = Label(self, font='Time 14 bold', fg='blue', bd=4)
		self.WordAskLbl.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
		
		# Information
		self.InfoLbl_ = Label(self, text="Info. complémentaire : ")
		self.InfoLbl_.grid(row=2, column=0, sticky=E, padx=5, pady=5)
		self.InfoLbl = Label(self, fg='gray')
		self.InfoLbl.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
		
		# Réponse
		self.WordAns_ = Label(self)
		self.WordAns_.grid(row=3, column=0, sticky=E, padx=5, pady=5)
		self.WordAns = Entry(self)
		self.WordAns.grid(row=3, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
		self.WordAns.bind('<KeyPress-Return>',self.onCheck)
		
		# Zone statistique
		self.StatLblFrame = LabelFrame(self, bd=1, relief='solid')
		self.StatLblFrame.grid(row=4, column=0, rowspan=2, columnspan=2)
		self.StatNbLbl_ = Label(self.StatLblFrame, text="Nombre de tirage : ")
		self.StatNbLbl_.grid(row=0, column=0, sticky=E)
		self.StatNbLbl = Label(self.StatLblFrame)
		self.StatNbLbl.grid(row=0, column=1, sticky=W)
		self.StatNbOkLbl_ = Label(self.StatLblFrame, text="Nombre de Ok : ")
		self.StatNbOkLbl_.grid(row=1, column=0, sticky=E)
		self.StatNbOkLbl = Label(self.StatLblFrame)
		self.StatNbOkLbl.grid(row=1, column=1, sticky=W)
		self.StatNbKoLbl_ = Label(self.StatLblFrame, text="Nombre de Ko : ")
		self.StatNbKoLbl_.grid(row=2, column=0, sticky=E)
		self.StatNbKoLbl = Label(self.StatLblFrame)
		self.StatNbKoLbl.grid(row=2, column=1, sticky=W)
		self.StatReussite_ = Label(self.StatLblFrame, text="% de réussite : ")
		self.StatReussite_.grid(row=3, column=0, sticky=E)
		self.StatReussite = Label(self.StatLblFrame)
		self.StatReussite.grid(row=3, column=1, sticky=W)
		
		# Boutons ...
		# ... Controle de la réponse
		self.CheckBtn = Button(self
			, text="Vérifier la réponse"
			, command=self.onCheck
		)
		self.CheckBtn.grid(row=4, column=2, sticky=NE, padx=5, pady=5)
		
		# ... Fermer la fenetre
		self.CloseBtn = Button(self
			, text="Sortir"
			, command=self.onClose
		)
		self.CloseBtn.grid(row=5, column=2, sticky=SE, padx=5, pady=5)
		
		# ... Solution
		self.ResultFrame = LabelFrame(self, bd=1, relief='solid', text=" Résultat ")
		self.ResultFrame.grid(row=6, column=0, columnspan=3, stick=EW, padx=5, pady=10, ipadx=5, ipady=5)
		self.ResultLbl = Label(self.ResultFrame, justify=LEFT, font='Time 16 bold')
		self.ResultLbl.grid(row=0, column=0, columnspan=2, stick=EW)
		self.ResultAskLbl_ = Label(self.ResultFrame, text="Mot proposé : ")
		self.ResultAskLbl_.grid(row=1,column=0, sticky=E)
		self.ResultAskLbl = Label(self.ResultFrame, fg='blue')
		self.ResultAskLbl.grid(row=1, column=1, sticky=EW)
		self.ResultSaisiseLbl_ = Label(self.ResultFrame, text="Mots saisies : ")
		self.ResultSaisiseLbl_.grid(row=2, column=0, sticky=E) 
		self.ResultSaisiseLbl = Label(self.ResultFrame)
		self.ResultSaisiseLbl.grid(row=2, column=1, sticky=EW)
		self.ResultAnsLbl_ = Label(self.ResultFrame, text="Réponse : ")
		self.ResultAnsLbl_.grid(row=3,column=0, sticky=E)
		self.ResultAnsLbl = Label(self.ResultFrame, fg='green', font='12')
		self.ResultAnsLbl.grid(row=3, column=1, sticky=EW)
		self.RésulStatLbl_ = Label(self.ResultFrame, text="Taux de réussite : ")
		self.RésulStatLbl_.grid(row=4,column=0, sticky=E)
		self.RésulStatLbl = Label(self.ResultFrame)
		self.RésulStatLbl.grid(row=4, column=1, sticky=EW)

		
		# Mise à jour des libellés en fonction du mode d'entrainement
		if self.Mode == EN_TO_FR : 
			self.titleLbl["text"]="Entrainement de l'anglais vers le français"
			self.WordAskLbl_["text"]="Mot en anglais : "
			self.WordAns_["text"] = "Mot en français : "
		elif self.Mode == FR_TO_EN:
			self.titleLbl["text"]="Entrainement du français vers l'anglais"
			self.WordAskLbl_["text"]="Mot en français : "
			self.WordAns_["text"] = "Mot en anglais : "
		else:
			if _DEBUG_ : print("MyDicoTraining.makeGUI : Mode d'entrainement non défini.")
		
		self.grid()
		
	#\ makeGUI
			
	# ------------ Méthodes Event ------------
	def onCheck(self, event=None):
		"Controle la réponse"
				
		if self.Mode == EN_TO_FR:
			self.CurrentTranslate.set(EN_COUNT,int(self.CurrentTranslate.get(EN_COUNT))+1)
			if self.WordAns.get() != self.CurrentTranslate[FR]:
				self.CurrentTranslate.set(EN_ERR_COUNT,int(self.CurrentTranslate[EN_ERR_COUNT])+1)
				self.ResultLbl['text']=CHECKKO_MSG
				self.ResultLbl['fg']=CHECKKO_COLOR
			else:
				self.ResultLbl['text']=CHECKOK_MSG
				self.ResultLbl['fg']=CHECKOK_COLOR
			

			self.ResultAnsLbl['text'] = self.CurrentTranslate[FR]
			self.RésulStatLbl['text'] = "{:6.2f} %".format(self.CurrentTranslate[EN_RATIO]*100)
		else:
			self.CurrentTranslate.set(FR_COUNT,int(self.CurrentTranslate.get(FR_COUNT))+1)
			if self.WordAns.get() != self.CurrentTranslate.get(EN):
				self.CurrentTranslate.set(FR_ERR_COUNT,int(self.CurrentTranslate.get(FR_ERR_COUNT))+1)
				self.ResultLbl['text']=CHECKKO_MSG
				self.ResultLbl['fg']=CHECKKO_COLOR
			else:
				self.ResultLbl['text']=CHECKOK_MSG
				self.ResultLbl['fg']=CHECKOK_COLOR
			
			self.ResultAnsLbl['text'] = self.CurrentTranslate[EN]
			self.RésulStatLbl['text'] = "{:6.2f} %".format(self.CurrentTranslate[FR_RATIO]*100)
		
		self.ResultSaisiseLbl['text'] = self.WordAns.get()
		self.ResultAskLbl['text'] = self.WordAskLbl['text']
		
		self.askWord()		
	#\ onCheck
	
	def onClose(self):
		"Ferme la fenêtre"
		self.master.displayFrame(FRAME_DEFAULT)

		# self.grid_remove()
		# self.master.onCloseFrame()
	#\ onClose
	
	# ------------ Méthodes ------------
	def show(self):
		"Affiche l'écran"
		self.grid()
	#\show
	
	def askWord(self):
		"Initialise une question"
		if self.Mode == EN_TO_FR :
			# Selction d'une traduction
			self.CurrentTranslate=self.Dico.shotWord(EN)
			#Affiche de la traduction choisie
			self.WordAskLbl["text"]=self.CurrentTranslate[EN]
			self.InfoLbl["text"]=self.CurrentTranslate[INFO]
			self.StatNbLbl["text"]=str(self.CurrentTranslate[EN_COUNT])
			self.StatNbOkLbl["text"]=str(self.CurrentTranslate[EN_COUNT]-self.CurrentTranslate[EN_ERR_COUNT])
			self.StatNbKoLbl["text"]=str(self.CurrentTranslate[EN_ERR_COUNT])
			self.StatReussite["text"]="{:6.2f} %".format(self.CurrentTranslate[EN_RATIO]*100)
		else:
			# Selction d'une traduction
			self.CurrentTranslate=self.Dico.shotWord(FR)
			#Affiche de la traduction choisie
			self.WordAskLbl["text"]=self.CurrentTranslate.get(FR)
			self.InfoLbl["text"]=self.CurrentTranslate.get(INFO)
			self.StatNbLbl["text"]=str(self.CurrentTranslate.get(FR_COUNT))
			self.StatNbOkLbl["text"]=str(int(self.CurrentTranslate.get(FR_COUNT))-int(self.CurrentTranslate.get(FR_ERR_COUNT)))
			self.StatNbKoLbl["text"]=str(self.CurrentTranslate.get(FR_ERR_COUNT))
			self.StatReussite["text"]="{:6.2f} %".format(self.CurrentTranslate[FR_RATIO]*100)
		
		self.WordAns.delete(0,END)
		self.WordAns.focus_set()
	#\askWord	

# Fin du fichier MyDicoTraining.py