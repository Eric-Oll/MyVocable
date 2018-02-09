# ManageMyDico : Boite de dialogue de gestion du dictionnaire
# -----------------------------------------------------------

_DEBUG_=False

# -----------------------
# Importation des modules
# -----------------------
import tkinter
from tkinter import *
from tkinter.constants import *
from tkinter.messagebox import *
from WordListFrame import *
from MyDico import  *
from MyDicoApp import *


# *************************
# *  Classe ManageMyDico  *
# *************************
class ManageMyDico(Frame):
	# ------------ Attributs de la classe ------------
	Dico = None		# Dictionnaire
	DicoList = None	# Liste des éléments du dictionnaire
	SortOption = None	# Défini le tri du dictionnaire
	
	# ------------ Constructeurs ------------
	def __init__(self, master, dico):
		"Contructeur de la classe ManageMyDico"
		Frame.__init__(self, master)
		
		# Contruction du GUI
		self.makeGUI()
	
		# Initialisation de la liste
		self.Dico = dico
		self.onSort()
	#\__init__
	
	# ------------ Méthodes GUI ------------
	def makeGUI(self):
		"Construction de l'interface GUI"
		
		# Liste des mots
		self.DicoList = WordListFrame(self)
		self.DicoList.grid(row=0, column=0, rowspan=5, sticky='nesw')
		self.DicoList.bind('<<change-Index>>',self.onSelect)
		
		# Option de tri
		self.SortOption=StringVar()
		self.SortOption.set(EN)
		self.SortOptFrame = LabelFrame(self, bd=1, relief="solid", text="Tri")
		self.SortOptFrame.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky=EW)
		self.OptEN = Radiobutton(self.SortOptFrame, 
			text="Anglais", 
			variable=self.SortOption, 
			value=EN,
			command=self.onSort
		)
		self.OptEN.grid(row=0, column=0, sticky=W)
		self.OptFR = Radiobutton(self.SortOptFrame, 
			text="Français", 
			variable=self.SortOption, 
			value=FR,
			command=self.onSort
		)
		self.OptFR.grid(row=0, column=1, sticky=E)
		self.OptEN.select()
		
		
		# Détail des mots / Modif
		self.DetailFrame = LabelFrame(self, bd=1, relief="solid")
		self.DetailFrame.grid(row=1,column=1, padx=5, pady=5, ipadx=5, ipady=5)
		
		self.LabelEN = Label(self.DetailFrame, text="Mot en anglais")
		self.LabelEN.grid(row=0, sticky=W, padx=5, pady=5)
		
		self.EntryEN = Entry(self.DetailFrame)
		self.EntryEN.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
		
		self.LabelFR = Label(self.DetailFrame, text="Mot en français")
		self.LabelFR.grid(row=1, sticky=W, padx=5, pady=5)
		
		self.EntryFR = Entry(self.DetailFrame)
		self.EntryFR.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
		
		self.LabelInfo = Label(self.DetailFrame, text="Info complémentaire")
		self.LabelInfo.grid(row=2, sticky=W, padx=5, pady=5)
		
		self.EntryInfo = Entry(self.DetailFrame, width=20)
		self.EntryInfo.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
		
		# Bouton d'actions
		self.ButtonAdd = Button(self.DetailFrame, text="Ajouter", command=self.onAdd)
		self.ButtonAdd.grid(row=3, column=0, padx=10, pady=5)
		self.ButtonModify = Button(self.DetailFrame, text="Modifier", command=self.onModify)
		self.ButtonModify.grid(row=3, column=1, padx=10, pady=5)
		self.ButtonDelete = Button(self.DetailFrame, text="Supprimer", command=self.onDelete)
		self.ButtonDelete.grid(row=3, column=2, padx=10, pady=5)
		
		self.ButtonQuit = Button(self, text="Sortir", command=self.onQuit)
		self.ButtonQuit.grid(row=2, column=1, padx=5, pady=5, sticky=E)
		self.grid()
	#\makeGUI
	
	# ------------ Méthodes Event ------------
	def onAdd(self):
		# Controle de la saisie
		if self.EntryEN.get() == "":
			# Afficher un message d'erreur
			showwarning(
				"MyDicoApp.ManageMyDico",
				"Le mot anglais doit être renseigné."
			)
			return
		if self.EntryFR.get() == "":
			# Afficher un message d'erreur
			showwarning(
				"MyDicoApp.ManageMyDico",
				"Le mot français doit être renseigné."
			)
			return
		
		# Ajout dans le dictionnaire
		self.Dico.addTranslate(MyTranslate(
			en=self.EntryEN.get(),
			fr=self.EntryFR.get(),
			info=self.EntryInfo.get()
		))
		
		self.EntryEN.delete(0,END)
		self.EntryFR.delete(0,END)
		self.EntryInfo.delete(0,END)
		
		# Ajout dans la liste
		self.updateList()
	#\onAdd
	
	def onModify(self):
			# Controle de la saisie
			if self.EntryEN.get() == "":
				# Afficher un message d'erreur
				showwarning(
					"MyDicoApp.ManageMyDico",
					"Le mot anglais doit être renseigné."
				)
				return
			if self.EntryFR.get() == "":
				# Afficher un message d'erreur
				showwarning(
					"MyDicoApp.ManageMyDico",
					"Le mot français doit être renseigné."
				)
				return
			
			# Mise à jour du dictionnaire
			self.Dico.ListWords[self.DicoList.Index].set(EN,self.EntryEN.get())
			self.Dico.ListWords[self.DicoList.Index].set(FR,self.EntryFR.get())
			self.Dico.ListWords[self.DicoList.Index].set(INFO,self.EntryInfo.get())
			
			self.EntryEN.delete(0,END)
			self.EntryFR.delete(0,END)
			self.EntryInfo.delete(0,END)

			# Ajout dans la liste
			self.updateList()
	#\onModify	
		
	def onDelete(self):
		pass
	#\onDelete
	
	def onSelect(self, event):
		self.EntryEN.delete(0,END)
		self.EntryEN.insert(0,self.Dico.ListWords[self.DicoList.Index].get(EN))
		self.EntryFR.delete(0,END)
		self.EntryFR.insert(0,self.Dico.ListWords[self.DicoList.Index].get(FR))
		self.EntryInfo.delete(0,END)
		self.EntryInfo.insert(0,self.Dico.ListWords[self.DicoList.Index].get(INFO))
	#\onSelect
	
	def onSort(self):
		"Répond à l'évènement du choix du tri"
		if _DEBUG_: print("ManageMyDico.onSort : Appel de l'évènement avec les tri par : %s" % self.SortOption.get())
		self.Dico.sortDico(self.SortOption.get())
		self.updateList()
	#\onSort
	
	def onQuit(self):
		# self.grid_remove()
		self.master.displayFrame(FRAME_DEFAULT)
	#\onQuit
	
	# ------------ Méthodes ------------
	def show(self):
		"Affiche l'écran"
		self.grid()
	#\show
	
	def updateList(self):
		"Met à jour la liste DicoList"
		# Vide la liste existante
		self.DicoList.delete(0,END)
		
		# Recharge la liste des mots
		for translate in self.Dico.ListWords:
			if self.SortOption.get() == EN:
				self.DicoList.setTitle(("Anglais","Français","Info"))
				self.DicoList.insert(END,(translate["EN"],translate["FR"],translate["INFO"]))
			else:
				self.DicoList.setTitle(("Français","Anglais","Info"))
				self.DicoList.insert(END,(translate["FR"],translate["EN"],translate["INFO"]))
	#\updateList

# Fin du fichier ManageMyDico.py