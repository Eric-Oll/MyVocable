# MyDicoApp : Application d'apprentissage du vocabulaire Anglais - Français
# -------------------------------------------------------------------------
_DEBUG_=True

# -----------------------
# Importation des modules
# -----------------------
import configparser
import tkinter
from tkinter import *
from tkinter.filedialog import *

from MyDico import  *
from ManageMyDico import *
from MyDicoTraining import *

# **************
# * CONSTANTES *
# **************
APP_TITLE = "MyDicoApp"
INI_FILE = "MyDicoApp.INI"
WIDTH_DEFAULT = 500
HEIGHT_DEFAULT = 300

# -- Frame List --
FRAME_DEFAULT = 'DefaultFrame'
FRAME_MANAGEDICO = 'ManageDico'
FRAME_TRAININGEN = 'TrainingEN'
FRAME_TRAININGFR = 'TrainingFR'

# **********************
# *  Classe MyDicoApp  *
# **********************
class MyDicoApp(Tk):
	"Application principale du Dico"
	# ------------ Attributs de la classe ------------
	AppConfig = None	# Configuration de l'application
	Dico=None			# Dictionnaire de traduction
	DefaultFrame=None	# Ecran par défautt
	ManageDico=None		# Ecran de gestion du dictionnaire
	TrainingEN = None	# Ecran d'entrainement en anglais
	TrainingFR = None	# Ecran d'entrainement en Français
	
	# ------------ Constructeur  & Surcharge opérateur ------------
	def __init__(self, master=None):
		"Constructeur de MyDicoApp"
		Tk.__init__(self)
		self.master=master
		self.grid()
		
		# Lecture des données de configuration
		self.AppConfig = configparser.ConfigParser()
		try:
			self.AppConfig.read(INI_FILE)
		except:
			if _DEBUG_: print("MyDicoApp.__init__ : Fichier de config inconnu (%s)" % INI_FILE)
			
		# Contruction du GUI
		self.title(APP_TITLE)
		self.makeMenu()
		self.makeDefaultFrame()
		
		# Instanciation et chargement du dictionnaire
		self.Dico = MyDico()
		fileStr=self.AppConfig['APP']['DefaultDico']
		try:
			self.Dico.loadDico(fileStr)
			self.title("{} - {}".format(APP_TITLE, fileStr))
		except:
			if _DEBUG_: print("MyDicoApp.__init__ : Dictionnaire inconnu (%s)" % fileStr)
				
	#\__init__
	
	# ------------ Méthodes GUI ------------
	def makeDefaultFrame(self):
		"Crée une Frame par défaut pour l'application"
		self.DefaultFrame=Frame(self)
		self.DefaultFrame.grid()

		cnv = Canvas(self.DefaultFrame
			, width = WIDTH_DEFAULT
			, height = HEIGHT_DEFAULT
			#, bg="white"
		)
		cnv.grid(row=1, column=0, sticky=W, pady=20)
		
		try:
			self.imgFR_EN=PhotoImage(file=self.AppConfig['APP']['DefaultImage'])
			cnv.create_image(WIDTH_DEFAULT/2,HEIGHT_DEFAULT/2, image=self.imgFR_EN)
		except:
			if _DEBUG_: print("MyDicoApp.makeDefaultFrame : Erreur de chargement de l'image : %s" % self.AppConfig['APP']['DefaultImage'])

	# \makeDefaultFrame	
	
	def makeMenu(self):
		self.MenuBar = Menu(self)
		# Menu Fichier
		self.FileMenu = Menu(self.MenuBar,tearoff=0)
		self.FileMenu.add_command(label="Charger le dico", command=self.onLoad)
		self.FileMenu.add_command(label="Sauver le dico", command=self.onSave)
		self.FileMenu.add_separator()
		self.FileMenu.add_command(label="Quitter", command=self.onQuit)
		self.MenuBar.add_cascade(label="Fichier",menu=self.FileMenu)
		
		# Menu Trainning
		self.TrainingMenu = Menu(self.MenuBar, tearoff=0)
		self.TrainingMenu.add_command(label="Entrainnement En -> Fr",command=self.onTrainingEN)
		self.TrainingMenu.add_command(label="Entrainnement Fr -> En", command=self.onTrainingFR)
		self.TrainingMenu.add_separator()
		self.TrainingMenu.add_command(label="Statistiques", command=self.onReport)
		self.MenuBar.add_cascade(label="Entrainement",menu=self.TrainingMenu)
		
		# Menu Dictionnaire
		self.DicoMenu = Menu(self.MenuBar, tearoff=0)
		self.DicoMenu.add_command(label="Ajouter des mots...", command=self.onAddDico)
		self.DicoMenu.add_command(label="Rechercher", command=self.onSearchDico)
		self.MenuBar.add_cascade(label="Dictionnaire",menu=self.DicoMenu)
		
		# Affichage du menu
		self.config(menu=self.MenuBar)
	# \makeMenu
		
	# ------------ Méthodes Event ------------
	def onQuit(self):
		self.onSave()
		self.quit()
	#\onQuit
	
	def onLoad(self):
		fileDlg=LoadFileDialog(self ,title="Ouvrir un dictionnaire")
		fileStr=fileDlg.go()
		if fileStr !=None:
			print(fileStr)
			self.Dico.loadDico(fileStr)
			self.title("%s - %s" % (APP_TITLE, fileStr))	
	#\onLoad
	
	def onSave(self):
		if self.Dico.FileName != "":
			self.Dico.saveDico()
	#\onSave
	
	def onTrainingEN(self):
		self.displayFrame(FRAME_TRAININGEN)
		# if self.TrainingEN == None:
			# self.TrainingEN = MyDicoTraining(self, self.Dico, EN_TO_FR)
		# else:
			# self.TrainingEN.show()
		# self.DefaultFrame.grid_remove()
	#\onTrainingEN
	
	def onTrainingFR(self):
		self.displayFrame(FRAME_TRAININGFR)
		# if self.TrainingFR == None:
			# self.TrainingFR = MyDicoTraining(self, self.Dico, FR_TO_EN)
		# else:
			# self.TrainingFR.show()
		# self.DefaultFrame.grid_remove()
	#\onTrainingFR
	
	def onReport(self):
		pass
	#\onReport
	
	def onAddDico(self):
		self.displayFrame(FRAME_MANAGEDICO)
		# if self.ManageDico == None:
			# self.ManageDico=ManageMyDico(self, self.Dico)
		# else:
			# self.ManageDico.show()
		# self.DefaultFrame.grid_remove()
	#\onAddDiso
	
	def onSearchDico(self):
		pass
	#\onSearchDico
	
	def displayFrame(self, frame=FRAME_DEFAULT):
		"Affiche la Frame sélectionné"
		
		# Frame par défaut
		if frame==FRAME_DEFAULT: 
			self.DefaultFrame.grid()
		else:
			self.DefaultFrame.grid_remove()
			
		# Gestion du dictionnaire
		if frame ==FRAME_MANAGEDICO:
			if self.ManageDico == None:
				self.ManageDico=ManageMyDico(self, self.Dico)
			else:
				self.ManageDico.show()
		else: 
			if self.ManageDico != None: self.ManageDico.grid_remove()
			
		# Entrainement en Anglais
		if frame ==FRAME_TRAININGEN:
			if self.TrainingEN == None:
				self.TrainingEN = MyDicoTraining(self, self.Dico, EN_TO_FR)
			else:
				self.TrainingEN.show()
		else: 
			if self.TrainingEN != None: self.TrainingEN.grid_remove()
		
		
		# Entrainement en français
		if frame ==FRAME_TRAININGFR:
			if self.TrainingFR == None:
				self.TrainingFR = MyDicoTraining(self, self.Dico, FR_TO_EN)
			else:
				self.TrainingFR.show()
		else: 
			if self.TrainingFR != None: self.TrainingFR.grid_remove()
			
	#\onCloseFrame
	
# ==>  autotest -------------------------------------------------------------------
if __name__ == '__main__' :
	app=MyDicoApp()
	app.mainloop()
	
# Fin du fichier MyDicoApp.py