# -*- coding: utf-8 -*-
"""
WordListFrame : Widget to display the list of words' dictionnary
"""

# -----------------------
# Importation des modules
# -----------------------
from tkinter import Frame, Label, Scrollbar, Listbox
from tkinter import NS, END, DOTBOX, SINGLE
#from tkinter.constants import *
#from tkinter.messagebox import *
#from my_dico import MyDico

BG_UNSELECTED_COLOR = 'white'
FG_UNSELECTED_COLOR = 'black'
BG_SELECTED_COLOR = 'blue'
FG_SELECTED_COLOR = 'white'


# **************************
# *  Classe WordListFrame  *
# **************************
class WordListFrame(Frame):
    "Classe d'affichage de liste de mots du dictionnaire"

    # ------------ Constructeurs ------------
    def __init__(self, master=None):
        "Constructeur de la classe WordListFrame"
        super().__init__(master)

        #  Attributs ------------
        self.index = 0

        # Contruction du GUI
        self.make_frame()

        # Gérer les évènements
        #self.bind('<Change-Index>',self.onIndexChange,'+')
    #\__init__

    def make_frame(self):
        "Construction de l'interface"
        # --- Header ---
        self.col1_label = Label(self)
        self.col1_label.grid(row=0, column=0)
        self.col2_label = Label(self)
        self.col2_label.grid(row=0, column=1)
        self.col3_label = Label(self)
        self.col3_label.grid(row=0, column=2)

        # ---- Lists ----
        self.y_scroll = Scrollbar(self)
        self.col1_list = Listbox(self,
                                 activestyle=DOTBOX,
                                 selectmode=SINGLE,
                                 yscrollcommand=self.y_scroll.set)
        self.col2_list = Listbox(self,
                                 activestyle=DOTBOX,
                                 selectmode=SINGLE,
                                 yscrollcommand=self.y_scroll.set)
        self.col3_list = Listbox(self,
                                 activestyle=DOTBOX,
                                 selectmode=SINGLE,
                                 yscrollcommand=self.y_scroll.set)
        self.y_scroll.config(command=self.yview)
        self.col1_list.grid(row=1, column=0, sticky=NS)
        self.col2_list.grid(row=1, column=1, sticky=NS)
        self.col3_list.grid(row=1, column=2, sticky=NS)
        self.y_scroll.grid(row=1, column=3, sticky=NS)

        self.col1_list.bind("<<ListboxSelect>>", self.on_select_col1_event)
        self.col2_list.bind("<<ListboxSelect>>", self.on_select_col2_event)
        self.col3_list.bind("<<ListboxSelect>>", self.on_select_col3_event)
    #\make_frame

    def yview(self, args1, arg2, arg3=None, arg4=None):
        """Regroupe les évènements yview pour l'ensemble des listes"""
        self.col1_list.yview(args1, arg2, arg3, arg4)
        self.col2_list.yview(args1, arg2, arg3, arg4)
        self.col3_list.yview(args1, arg2, arg3, arg4)
    #\yview

    def grid(self, **args):
        """Display the frame"""
        super().grid(args)
    #\grid

    # ------------ Méthodes Event ------------
    def on_change_index(self):
        """Evènement de changement de la valeur de l'index"""
        self.on_select()
        self.event_generate('<<change-Index>>')
    #\on_change_index

    def on_select(self):
        """Selectionne une ligne dans la liste"""
        self.col1_list.itemconfig(self.index,
                                  background=BG_SELECTED_COLOR,
                                  foreground=FG_SELECTED_COLOR)
        self.col2_list.itemconfig(self.index,
                                  background=BG_SELECTED_COLOR,
                                  foreground=FG_SELECTED_COLOR)
        self.col3_list.itemconfig(self.index,
                                  background=BG_SELECTED_COLOR,
                                  foreground=FG_SELECTED_COLOR)
    #\on_select_event

    def on_lose_selection(self):
        """Sur la perte de la selection d'un Item"""
        self.col1_list.itemconfig(self.index,
                                  background=BG_UNSELECTED_COLOR,
                                  foreground=FG_UNSELECTED_COLOR)
        self.col2_list.itemconfig(self.index,
                                  background=BG_UNSELECTED_COLOR,
                                  foreground=FG_UNSELECTED_COLOR)
        self.col3_list.itemconfig(self.index,
                                  background=BG_UNSELECTED_COLOR,
                                  foreground=FG_UNSELECTED_COLOR)
    #\on_lose_selection

    def on_select_col1_event(self, event):
        "Selectionne dans la colonne 1"
        idxs = self.col1_list.curselection()
        if len(idxs) == 1:
            if int(idxs[0]) != self.index:
                self.on_lose_selection()
                self.index = int(idxs[0])
                self.on_change_index()
    #\on_select_col1_event

    def on_select_col2_event(self, event):
        "Selectionne dans la colonne 2"
        idxs = self.col2_list.curselection()
        if len(idxs) == 1:
            if int(idxs[0]) != self.index:
                self.on_lose_selection()
                self.index = int(idxs[0])
                self.on_change_index()
    #\on_select_col2_event

    def on_select_col3_event(self, event):
        "Selectionne dans la colonne 3"
        idxs = self.col3_list.curselection()
        if len(idxs) == 1:
            if int(idxs[0]) != self.index:
                self.on_lose_selection()
                self.index = int(idxs[0])
                self.on_change_index()
    #\on_select_col3_event

    # ------------ Méthodes ------------
    def set_title(self, triplet=("", "", "")):
        """Set the title of this frame"""
        self.col1_label["text"] = triplet[0]
        self.col2_label["text"] = triplet[1]
        self.col3_label["text"] = triplet[2]
    #\set_title

    def insert(self, position=END, triplet=("", "", "")):
        "Insert une traduction dans la liste à la postion donnnée"
        if len(triplet) == 3:
            self.col1_list.insert(position, triplet[0])
            self.col2_list.insert(position, triplet[1])
            self.col3_list.insert(position, triplet[2])
    #\insert

    def delete(self, debut, fin=None):
        "Supprime un ou plusieurs item de la liste"
        self.col1_list.delete(debut, fin)
        self.col2_list.delete(debut, fin)
        self.col3_list.delete(debut, fin)
    #\delete



# ==>  autotest -------------------------------------------------------------------
if __name__ == '__main__':
    app = WordListFrame()
    app.grid()

# Fin du fichier WordListFrame
