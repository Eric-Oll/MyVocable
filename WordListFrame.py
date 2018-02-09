# WordListFrame : Widget pour afficher la liste des mots du dictionnaire
# ----------------------------------------------------------------------

_DEBUG_=True

# -----------------------
# Importation des modules
# -----------------------
import tkinter
from tkinter import *
from tkinter.constants import *
from tkinter.messagebox import *
from MyDico import  *

BG_UNSELECTED_COLOR='white'
FG_UNSELECTED_COLOR='black'
BG_SELECTED_COLOR='blue'
FG_SELECTED_COLOR='white'


# **************************
# *  Classe WordListFrame  *
# **************************
class WordListFrame(Frame):
	"Classe d'affichage de liste de mots du dictionnaire"
	# ------------ Attributs de la classe ------------
	Col1Label=None	# Entete de la colonne 1
	Col2Label=None	# Entete de la colonne 2
	Col3Label=None	# Entete de la colonne 3
	Col1List=None	# Liste de la colonne 1
	Col2List=None	# Liste de la colonne 2
	Col3List=None	# Liste de la colonne 3
	YScroll=None	# Scrollbar des listes
	Index=0
	
	# ------------ Constructeurs ------------
	def __init__(self,master=None):
		"Constructeur de la classe WordListFrame"
		super().__init__(master)

		# Contruction du GUI
		self.makeGUI()
		
		# Gérer les évènements
		#self.bind('<Change-Index>',self.onIndexChange,'+')
		
		#\__init__
		
	def makeGUI(self):
		"Construction de l'interface"
		# --- Entete ---
		self.Col1Label = Label(self)
		self.Col1Label.grid(row=0,column=0)
		self.Col2Label = Label(self)
		self.Col2Label.grid(row=0,column=1)
		self.Col3Label = Label(self)
		self.Col3Label.grid(row=0,column=2)
		
		# ---- List ----
		self.YScroll = Scrollbar(self)
		self.Col1List=Listbox(self,
			activestyle=DOTBOX,
			selectmode=SINGLE,
			yscrollcommand=self.YScroll.set
			#, width=20
		)
		self.Col2List=Listbox(self,
			activestyle=DOTBOX,
			selectmode=SINGLE,
			yscrollcommand=self.YScroll.set
			#, width=20
		)
		self.Col3List=Listbox(self,
			activestyle=DOTBOX,
			selectmode=SINGLE,
			yscrollcommand=self.YScroll.set
			#, width=20
		)
		self.YScroll.config(command=self.yview)
		self.Col1List.grid(row=1, column=0, sticky=NS)
		self.Col2List.grid(row=1, column=1, sticky=NS)
		self.Col3List.grid(row=1, column=2, sticky=NS)	
		self.YScroll.grid(row=1, column=3, sticky=NS)
		
		self.Col1List.bind("<<ListboxSelect>>", self.onSelectCol1)
		self.Col2List.bind("<<ListboxSelect>>", self.onSelectCol2)
		self.Col3List.bind("<<ListboxSelect>>", self.onSelectCol3)

	#\makeGUI	
	
	def yview(self, args1, arg2, arg3=None, arg4=None):
		"Regroupe les évènements yview pour l'ensemble des listes"
		self.Col1List.yview(args1, arg2, arg3, arg4)
		self.Col2List.yview(args1, arg2, arg3, arg4)
		self.Col3List.yview(args1, arg2, arg3, arg4)
	#\yview	

	
	def grid(self, **args):
		super().grid(args)
	#\
	
	# ------------ Méthodes Event ------------
	def onChangeIndex(self):
		"Evènement de changement de la valeur de l'index"
		self.onSelect()
		self.event_generate('<<change-Index>>')
	#\onIndexChange
	
	def onSelect(self):
		"Selectionne une ligne dans la liste"
		self.Col1List.itemconfig(self.Index,background=BG_SELECTED_COLOR, foreground=FG_SELECTED_COLOR)
		self.Col2List.itemconfig(self.Index,background=BG_SELECTED_COLOR, foreground=FG_SELECTED_COLOR)
		self.Col3List.itemconfig(self.Index,background=BG_SELECTED_COLOR, foreground=FG_SELECTED_COLOR)		
	#\onSelect	
	
	def onLoseSelection(self):
		"Sur la perte de la selection d'un Item"
		self.Col1List.itemconfig(self.Index,background=BG_UNSELECTED_COLOR, foreground=FG_UNSELECTED_COLOR)
		self.Col2List.itemconfig(self.Index,background=BG_UNSELECTED_COLOR, foreground=FG_UNSELECTED_COLOR)
		self.Col3List.itemconfig(self.Index,background=BG_UNSELECTED_COLOR, foreground=FG_UNSELECTED_COLOR)		
	#\onLoseSelection
	
	def onSelectCol1(self, event):
		"Selectionne dans la colonne 1"
		idxs = self.Col1List.curselection()
		if len(idxs) == 1:
			if int(idxs[0])!= self.Index:
				self.onLoseSelection()
				self.Index=int(idxs[0])
				self.onChangeIndex()
	#\onSelectCol1

	def onSelectCol2(self, event):
		"Selectionne dans la colonne 2"
		idxs = self.Col2List.curselection()
		if len(idxs) == 1:
			if int(idxs[0])!= self.Index:
				self.onLoseSelection()
				self.Index=int(idxs[0])
				self.onChangeIndex()
	#\onSelectCol2

	def onSelectCol3(self, event):
		"Selectionne dans la colonne 3"
		idxs = self.Col3List.curselection()
		if len(idxs) == 1:
			if int(idxs[0])!= self.Index:
				self.onLoseSelection()
				self.Index=int(idxs[0])
				self.onChangeIndex()
	#\onSelectCol3
	
	# ------------ Méthodes ------------
	def setTitle(self, triplet=("","","")):
		self.Col1Label["text"]=triplet[0]
		self.Col2Label["text"]=triplet[1]
		self.Col3Label["text"]=triplet[2]
	#\setTitle
	
	def insert(self, position=END, triplet=("","","")):
		"Insert une traduction dans la liste à la postion donnnée"
		if len(triplet) == 3:
			self.Col1List.insert(position,triplet[0])
			self.Col2List.insert(position,triplet[1])
			self.Col3List.insert(position,triplet[2])
	#\insert
	
	def delete(self, debut, fin=None):
		"Supprime un ou plusieurs item de la liste"
		self.Col1List.delete(debut, fin)
		self.Col2List.delete(debut, fin)
		self.Col3List.delete(debut, fin)
	#\delete

	
	
# ==>  autotest -------------------------------------------------------------------
if __name__ == '__main__' :
	app=WordListFrame()
	app.grid()
	
# Fin du fichier WordListFrame	