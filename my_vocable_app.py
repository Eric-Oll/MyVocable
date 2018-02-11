# -*- coding: utf-8 -*-

"""
MyVocableApp : Application d'apprentissage du vocabulaire Anglais - Français
-----------------------------------------------------------------------------
This module contains the main class of this application : 'MyVocableApp'.

This module can be running directly with the standard command :
    > python my_vocable_app.py
"""

# -----------------------
# Importation des modules
# -----------------------
import configparser
from tkinter import Tk, Frame, Menu, Canvas, PhotoImage
from tkinter import W, NSEW
from tkinter.filedialog import LoadFileDialog
import logging as log

from my_dico import  MyDico
from manage_my_dico import ManageMyDico
from my_dico_training import MyDicoTraining, FR_TO_EN, EN_TO_FR

from my_vocable_constantes import APP_TITLE, INI_FILE, WIDTH_DEFAULT, HEIGHT_DEFAULT
from my_vocable_constantes import FRAME_DEFAULT, FRAME_MANAGEDICO, FRAME_TRAININGEN, FRAME_TRAININGFR

# **********************
# *  Classe MyDicoApp  *
# **********************
class MyVocableApp(Tk):
    "Application principale du Dico"

    # ------------ Constructeur  & Surcharge opérateur ------------
    def __init__(self, master=None):
        "Constructeur de MyDicoApp"
        Tk.__init__(self)
        self.master = master

        # Attributs de la classe ------------
        self.config_file = None    # Configuration de l'application
        self.dico = None            # Dictionnaire de traduction
        self.default_frame = None    # Ecran par défautt
        self.manage_dico_frame = None        # Ecran de gestion du dictionnaire
        self.training_en = None    # Ecran d'entrainement en anglais
        self.training_fr = None    # Ecran d'entrainement en Français
        self.grid()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        # Lecture des données de configuration
        self.config_file = configparser.ConfigParser()
        try:
            self.config_file.read(INI_FILE)
        except:
            log.debug("MyVocableApp.__init__ : Fichier de config inconnu ({})"
                      .format(INI_FILE))

        # Contruction du GUI
        self.title(APP_TITLE)
        self.make_menu()
        self.make_default_frame()

        # Instanciation et chargement du dictionnaire
        self.dico = MyDico()
        dico_filename = self.config_file['APP']['DefaultDico']
        try:
            self.dico.load_dico(dico_filename)
            self.title("{} - {}".format(APP_TITLE, dico_filename))
        except:
            log.error("MyVocableApp.__init__ : Dictionnaire inconnu ({})"
                      .format(dico_filename))

    #\__init__

    # ------------ Méthodes GUI ------------
    def make_default_frame(self):
        """Create a default frame for the application"""
        self.default_frame = Frame(self)
        self.default_frame.grid()

        cnv = Canvas(self.default_frame,
                     width=WIDTH_DEFAULT,
                     height=HEIGHT_DEFAULT)
        cnv.grid(row=1, column=0, sticky=W, pady=20)

        try:
            self.img_fr_en = PhotoImage(file=self.config_file['APP']['DefaultImage'])
            cnv.create_image(WIDTH_DEFAULT/2, HEIGHT_DEFAULT/2, image=self.img_fr_en)
        except Exception:
            log.error("MyVocableApp.makeDefaultFrame : Erreur de chargement de l'image : {}"
                      .format(self.config_file['APP']['DefaultImage']))

    # \make_default_frame

    def make_menu(self):
        """Create de menu of the application"""
        self.menu_bar = Menu(self)
        # Menu Fichier
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Charger le dico", command=self.on_load_event)
        self.file_menu.add_command(label="Sauver le dico", command=self.on_save_event)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quitter", command=self.on_quit_event)
        self.menu_bar.add_cascade(label="Fichier", menu=self.file_menu)

        # Menu Trainning
        self.training_menu = Menu(self.menu_bar, tearoff=0)
        self.training_menu.add_command(label="Entrainnement En -> Fr",
                                       command=self.on_english_training_event)
        self.training_menu.add_command(label="Entrainnement Fr -> En",
                                       command=self.on_french_training_event)
        self.training_menu.add_separator()
        self.training_menu.add_command(label="Statistiques", command=self.on_report_event)
        self.menu_bar.add_cascade(label="Entrainement", menu=self.training_menu)

        # Menu Dictionnaire
        self.dico_menu = Menu(self.menu_bar, tearoff=0)
        self.dico_menu.add_command(label="Ajouter des mots...", command=self.on_manage_dico_event)
        self.dico_menu.add_command(label="Rechercher", command=self.on_search_dico_event)
        self.menu_bar.add_cascade(label="Dictionnaire", menu=self.dico_menu)

        # Affichage du menu
        self.config(menu=self.menu_bar)
    # \make_menu

    # ------------ Méthodes Event ------------
    def on_quit_event(self):
        """Method used when the 'quit' menu item is activate"""
        self.on_save_event()
        self.quit()
    #\on_quit_event

    def on_load_event(self):
        """Method used when the 'load' menu item is activate"""
        file_dialog = LoadFileDialog(self, title="Ouvrir un dictionnaire")
        dico_filename = file_dialog.go()
        if dico_filename != None:
            print(dico_filename)
            self.dico.load_dico(dico_filename)
            self.title("{} - {}".format(APP_TITLE, dico_filename))
    #\on_load_event

    def on_save_event(self):
        """Method used when the 'save' menu item is activate"""
        if self.dico.filename != "":
            self.dico.save_dico()
    #\on_save_event

    def on_english_training_event(self):
        """Method used when the 'English Training' menu item is activate"""
        self.display_frame(FRAME_TRAININGEN)
    #\on_english_training_event

    def on_french_training_event(self):
        """Method used when the 'French Training' menu item is activate"""
        self.display_frame(FRAME_TRAININGFR)
    #\on_french_training_event

    def on_report_event(self):
        """Method used when the 'Reporting' menu item is activate"""
        pass
    #\on_report_event

    def on_manage_dico_event(self):
        """Method used when the 'Word adding' menu item is activate"""
        self.display_frame(FRAME_MANAGEDICO)
    #\on_manage_dico_event

    def on_search_dico_event(self):
        """Method used when the 'Search' menu item is activate"""
        pass
    #\on_search_dico_event

    def display_frame(self, frame=FRAME_DEFAULT):
        """Display the selected frame"""

        # Frame par défaut
        if frame == FRAME_DEFAULT:
            self.default_frame.grid()
        else:
            self.default_frame.grid_remove()

        # Gestion du dictionnaire
        if frame == FRAME_MANAGEDICO:
            if self.manage_dico_frame is None:
                self.manage_dico_frame = ManageMyDico(self, self.dico)
                self.manage_dico_frame.grid(row=0, column=0, sticky=NSEW)
            else:
                self.manage_dico_frame.show()
        else:
            if self.manage_dico_frame is not None:
                self.manage_dico_frame.grid_remove()

        # Entrainement en Anglais
        if frame == FRAME_TRAININGEN:
            if self.training_en is None:
                self.training_en = MyDicoTraining(self, self.dico, EN_TO_FR)
                self.training_en.grid(row=0, column=0, sticky=NSEW)
            else:
                self.training_en.show()
        else:
            if self.training_en is not None:
                self.training_en.grid_remove()

        # Entrainement en français
        if frame == FRAME_TRAININGFR:
            if self.training_fr is None:
                self.training_fr = MyDicoTraining(self, self.dico, FR_TO_EN)
                self.training_fr.grid(row=0, column=0, sticky=NSEW)
            else:
                self.training_fr.show()
        else:
            if self.training_fr is not None:
                self.training_fr.grid_remove()

    #\display_frame

# ==>  autotest -------------------------------------------------------------------
if __name__ == '__main__':
    app = MyVocableApp()
    app.mainloop()

# Fin du fichier my_vocable_app.py
