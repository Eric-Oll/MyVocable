# -*- coding: utf-8 -*-

"""
This module contains the 'ManageMyDico' Frame
(ManageMyDico : Boite de dialogue de gestion du dictionnaire)
"""
# -----------------------
# Importation des modules
# -----------------------
from tkinter import Frame, Label, LabelFrame, Entry, Button
from tkinter import Radiobutton, StringVar, Listbox, Scrollbar
from tkinter import W, E, EW, NS, NSEW, END, ACTIVE
#from tkinter.constants import *
from tkinter.messagebox import showwarning
import logging as log

from word_list_frame import WordListFrame
from my_dico import MyTranslation, EN, FR, INFO, CATEGORIES

from my_vocable_constantes import FRAME_DEFAULT

# TODO : Ajouter la gestion des categories

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
        self.detail_frame.grid(row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky=NSEW)
        self.detail_frame.rowconfigure(3, weight=1)
        self.detail_frame.columnconfigure(1, weight=1)

        # ... English
        self.en_label = Label(self.detail_frame, text="Mot en anglais")
        self.en_label.grid(row=0, sticky=W, padx=5, pady=5)
        self.en_entry = Entry(self.detail_frame)
        self.en_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=EW)

        # ... French
        self.fr_label = Label(self.detail_frame, text="Mot en français")
        self.fr_label.grid(row=1, sticky=W, padx=5, pady=5)
        self.fr_entry = Entry(self.detail_frame)
        self.fr_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=EW)

        # ... Info
        self.info_label = Label(self.detail_frame, text="Info complémentaire")
        self.info_label.grid(row=2, sticky=W, padx=5, pady=5)
        self.info_entry = Entry(self.detail_frame, width=20)
        self.info_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=EW)

        # ... Categories
        self.categories_group = LabelFrame(self.detail_frame, bd=1, relief="solid", text="Catégories")
        self.categories_group.grid(row=3, columnspan=3, padx=5, pady=5, sticky=NSEW)

        self.y_select_categ_scroll = Scrollbar(self.categories_group)
        self.selected_categories = Listbox(self.categories_group,
                                           yscrollcommand=self.y_select_categ_scroll.set)
        self.y_select_categ_scroll.config(command=self.selected_categories.yview)
        self.selected_categories.grid(row=0, column=0, rowspan=5, padx=5, pady=5, sticky=NSEW)
        self.y_select_categ_scroll.grid(row=0, column=1, rowspan=5, padx=5, pady=5, sticky=NS)

        self.add_categ_button = Button(self.categories_group, text="<<",
                                       command=self.on_add_categ_event)
        self.add_categ_button.grid(row=1, column=2, padx=5, pady=5 )

        self.del_categ_button = Button(self.categories_group, text=">>",
                                       command=self.on_del_categ_event)
        self.del_categ_button.grid(row=2, column=2, padx=5, pady=5)

        self.y_avail_categ_scroll = Scrollbar(self.categories_group)
        self.available_categories = Listbox(self.categories_group,
                                            yscrollcommand=self.y_avail_categ_scroll.set)
        self.y_avail_categ_scroll.config(command=self.available_categories.yview)
        self.available_categories.grid(row=0, column=3, rowspan=4, padx=5, pady=5, sticky=NSEW)
        self.y_avail_categ_scroll.grid(row=0, column=4, rowspan=4, padx=5, pady=5, sticky=NS)

        self.new_category_entry = Entry(self.categories_group)
        self.new_category_entry.grid(row=4, column=3, rowspan=4, padx=5, pady=5, sticky=EW)
        self.new_category_button = Button(self.categories_group, text="+",
                                          command=self.on_new_categ_event)
        self.new_category_entry.bind('<KeyPress-Return>', self.on_new_categ_event)
        self.new_category_button.grid(row=4, column=4)

        self.categories_group.rowconfigure(0, weight=1)
        self.categories_group.rowconfigure(3, weight=1)
        self.categories_group.columnconfigure(0, weight=1)
        self.categories_group.columnconfigure(3, weight=1)

        # Bouton d'actions
        self.add_button = Button(self.detail_frame, text="Ajouter",
                                 command=self.on_add_event)
        self.add_button.grid(row=4, column=0, padx=10, pady=5)
        self.modify_button = Button(self.detail_frame, text="Modifier",
                                    command=self.on_modify_event)
        self.modify_button.grid(row=4, column=1, padx=10, pady=5)
        self.delete_button = Button(self.detail_frame, text="Supprimer",
                                    command=self.on_delete_event)
        self.delete_button.grid(row=4, column=2, padx=10, pady=5)

        self.quit_button = Button(self, text="Sortir",
                                  command=self.on_quit_event)
        self.quit_button.grid(row=2, column=1, padx=5, pady=5, sticky=E)

        self.grid()
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
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
        self.dico.add_translation(MyTranslation(
            en=self.en_entry.get(),
            fr=self.fr_entry.get(),
            info=self.info_entry.get()
        )) # TODO : Ajouter les categories auxquelles sont liées la traduction

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
        self.dico.words[self.word_list_frame.index][EN] = self.en_entry.get()
        self.dico.words[self.word_list_frame.index][FR] = self.fr_entry.get()
        self.dico.words[self.word_list_frame.index][INFO] = self.info_entry.get()
        self.dico.words[self.word_list_frame.index][CATEGORIES] = \
            [category for category in self.selected_categories.get(0,END)]

        self.en_entry.delete(0, END)
        self.fr_entry.delete(0, END)
        self.info_entry.delete(0, END)
        self.selected_categories.delete(0,END)

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
        # Update selected categories
        self.selected_categories.delete(0, END)
        category_used = self.dico.words[self.word_list_frame.index][CATEGORIES]
        for category in sorted(category_used):
            self.selected_categories.insert(END, category)
        # Update available catagories
        self.available_categories.delete(0,END)
        for category in sorted(self.dico.categories):
            if category not in category_used:
                self.available_categories.insert(END, category)
    #\on_select_event

    def on_add_categ_event(self):
        """Method executed when the add_categ_button is pressed"""
        try:
            index =  self.available_categories.index(ACTIVE)
        except:
            return
        if index>=0:
            self.selected_categories.insert(END, self.available_categories.selection_get())
            self.available_categories.delete(index)
            self.available_categories.selection_set(self.available_categories.index(ACTIVE))

    def on_del_categ_event(self):
        """Method executed when the del_categ_button is pressed"""
        try:
            index =  self.selected_categories.index(ACTIVE)
        except:
            return
        if index>=0:
            self.available_categories.insert(END, self.selected_categories.selection_get())
            self.selected_categories.delete(index)
            self.selected_categories.selection_set(self.selected_categories.index(ACTIVE))

    def on_new_categ_event(self, event=None):
        """Method executed when the new_categ_button is pressed"""
        new_categ = self.new_category_entry.get()
        if new_categ != "" and new_categ not in self.dico.categories:
            self.available_categories.insert(END,new_categ)
            self.dico.add_category(new_categ)
            self.new_category_entry.delete(0, END)

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

        # Update header if the list
        if self.sort_option.get() == EN:
            self.word_list_frame.set_title(("Anglais", "Français", "Info"))
        else:
            self.word_list_frame.set_title(("Français", "Anglais", "Info"))

        # Recharge la liste des mots
        self.dico.sort_dico(self.sort_option.get())
        for translation in self.dico.words:
            if self.sort_option.get() == EN:
                self.word_list_frame.insert(END,
                                            (translation[EN], translation[FR], translation[INFO]))
            else:
                self.word_list_frame.insert(END,
                                            (translation[FR], translation[EN], translation[INFO]))
    #\update_list

# Fin du fichier manage_my_dico.py
