# -*- coding: utf-8 -*-

"""
This module contains the 'ManageMyDico' Frame
(ManageMyDico : Boite de dialogue de gestion du dictionnaire)
"""
# -----------------------
# Importation des modules
# -----------------------
from tkinter import Frame, Label, LabelFrame, Entry, Button, Radiobutton, StringVar
from tkinter import W, E, EW, NSEW, END
#from tkinter.constants import *
from tkinter.messagebox import showwarning
import logging as log

from word_list_frame import WordListFrame
from my_dico import MyTranslate, EN, FR, INFO

from my_vocable_constantes import FRAME_DEFAULT

# =============================================================================
# Classe ManageMyDico
# =============================================================================
class ManageMyDico(Frame):
    """'ManageMyDiso' is Frame to manage the translation of the dictionnary."""
    # ------------ Constructeurs ------------
    def __init__(self, master, dico):
        "Contructeur de la classe ManageMyDico"
        Frame.__init__(self, master)

        self.word_list_frame = None    # Liste des éléments du dictionnaire
        self.sort_option = None    # Défini le tri du dictionnaire

        # Contruction du GUI
        self.create_frame()

        # Initialisation de la liste
        self.dico = dico
        self.on_sort_event()
    #\__init__

    # ------------ Méthodes GUI ------------
    def create_frame(self):
        "Construction de l'interface GUI"

        # Liste des mots
        self.word_list_frame = WordListFrame(self)
        self.word_list_frame.grid(row=0, column=0, rowspan=5, sticky=NSEW)
        self.word_list_frame.bind('<<change-Index>>', self.on_select_event)

        # Option de tri
        self.sort_option = StringVar()
        self.sort_option.set(EN)
        self.sort_option_frame = LabelFrame(self, bd=1, relief="solid", text="Tri")
        self.sort_option_frame.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky=EW)
        self.en_option = Radiobutton(self.sort_option_frame,
                                     text="Anglais",
                                     variable=self.sort_option,
                                     value=EN,
                                     command=self.on_sort_event)
        self.en_option.grid(row=0, column=0, sticky=W)
        self.fr_option = Radiobutton(self.sort_option_frame,
                                     text="Français",
                                     variable=self.sort_option,
                                     value=FR,
                                     command=self.on_sort_event)
        self.fr_option.grid(row=0, column=1, sticky=E)
        self.en_option.select()


        # Détail des mots / Modif
        self.detail_frame = LabelFrame(self, bd=1, relief="solid")
        self.detail_frame.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        self.en_label = Label(self.detail_frame, text="Mot en anglais")
        self.en_label.grid(row=0, sticky=W, padx=5, pady=5)

        self.en_entry = Entry(self.detail_frame)
        self.en_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.fr_label = Label(self.detail_frame, text="Mot en français")
        self.fr_label.grid(row=1, sticky=W, padx=5, pady=5)

        self.fr_entry = Entry(self.detail_frame)
        self.fr_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.info_label = Label(self.detail_frame, text="Info complémentaire")
        self.info_label.grid(row=2, sticky=W, padx=5, pady=5)

        self.info_entry = Entry(self.detail_frame, width=20)
        self.info_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        # Bouton d'actions
        self.add_button = Button(self.detail_frame, text="Ajouter",
                                 command=self.on_add_event)
        self.add_button.grid(row=3, column=0, padx=10, pady=5)
        self.modify_button = Button(self.detail_frame, text="Modifier",
                                    command=self.on_modify_event)
        self.modify_button.grid(row=3, column=1, padx=10, pady=5)
        self.delete_button = Button(self.detail_frame, text="Supprimer",
                                    command=self.on_delete_event)
        self.delete_button.grid(row=3, column=2, padx=10, pady=5)

        self.quit_button = Button(self, text="Sortir",
                                  command=self.on_quit_event)
        self.quit_button.grid(row=2, column=1, padx=5, pady=5, sticky=E)

        self.grid()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>", self.on_resize_event)

    #\create_frame

    # ------------ Méthodes Event ------------
    def on_add_event(self):
        """Method used when the add_button is activated."""
        # Controle de la saisie
        if self.en_entry.get() == "":
            # Afficher un message d'erreur
            showwarning(
                "MyDicoApp.ManageMyDico",
                "Le mot anglais doit être renseigné."
            )
            return
        if self.fr_entry.get() == "":
            # Afficher un message d'erreur
            showwarning(
                "MyDicoApp.ManageMyDico",
                "Le mot français doit être renseigné."
            )
            return

        # Ajout dans le dictionnaire
        self.dico.addTranslate(MyTranslate(
            en=self.en_entry.get(),
            fr=self.fr_entry.get(),
            info=self.info_entry.get()
        ))

        self.en_entry.delete(0, END)
        self.fr_entry.delete(0, END)
        self.info_entry.delete(0, END)

        # Ajout dans la liste
        self.update_list()
    #\on_add_event

    def on_modify_event(self):
        """Method used when the modify_button is activated."""
        # Controle de la saisie
        if self.en_entry.get() == "":
            # Afficher un message d'erreur
            showwarning(
                "MyDicoApp.ManageMyDico",
                "Le mot anglais doit être renseigné."
            )
            return
        if self.fr_entry.get() == "":
            # Afficher un message d'erreur
            showwarning(
                "MyDicoApp.ManageMyDico",
                "Le mot français doit être renseigné."
            )
            return

        # Mise à jour du dictionnaire
        self.dico.words[self.word_list_frame.index].set(EN, self.en_entry.get())
        self.dico.words[self.word_list_frame.index].set(FR, self.fr_entry.get())
        self.dico.words[self.word_list_frame.index].set(INFO, self.info_entry.get())

        self.en_entry.delete(0, END)
        self.fr_entry.delete(0, END)
        self.info_entry.delete(0, END)

        # Ajout dans la liste
        self.update_list()
    #\on_modify_event

    def on_delete_event(self):
        """Method used when the delete_button is activated."""
        pass
    #TODO : Faire la méthode on_delete_event
    #\on_delete_event

    def on_select_event(self, event):
        """Method used when a new line is selected on word_list_frame"""
        self.en_entry.delete(0, END)
        self.en_entry.insert(0, self.dico.words[self.word_list_frame.index].get(EN))
        self.fr_entry.delete(0, END)
        self.fr_entry.insert(0, self.dico.words[self.word_list_frame.index].get(FR))
        self.info_entry.delete(0, END)
        self.info_entry.insert(0, self.dico.words[self.word_list_frame.index].get(INFO))
    #\on_select_event

    def on_sort_event(self):
        "Répond à l'évènement du choix du tri"
        log.debug("ManageMyDico.onSort : Appel de l'évènement avec les tri par : {}"
                  .format(self.sort_option.get()))
        self.dico.sort_dico(self.sort_option.get())
        self.update_list()
    #\on_sort_event

    def on_resize_event(self, event):
        """Method used when the frame shape resize"""
        self.width = event.width
        self.height = event.height
        log.debug("New size 'ManageMyDico' : {}x{}".format(self.width, self.height))

    def on_quit_event(self):
        """Method used when the quit_button is activated."""
        # self.grid_remove()
        self.master.display_frame(FRAME_DEFAULT)
    #\on_quit_event

    # ------------ Méthodes ------------
    def show(self):
        "Affiche l'écran"
        self.grid()
    #\show

    def update_list(self):
        "Met à jour la liste word_list_frame"
        # Vide la liste existante
        self.word_list_frame.delete(0, END)

        # Recharge la liste des mots
        for translate in self.dico.words:
            if self.sort_option.get() == EN:
                self.word_list_frame.set_title(("Anglais", "Français", "Info"))
                self.word_list_frame.insert(END,
                                            (translate["EN"], translate["FR"], translate["INFO"]))
            else:
                self.word_list_frame.set_title(("Français", "Anglais", "Info"))
                self.word_list_frame.insert(END,
                                            (translate["FR"], translate["EN"], translate["INFO"]))
    #\update_list

# Fin du fichier manage_my_dico.py
