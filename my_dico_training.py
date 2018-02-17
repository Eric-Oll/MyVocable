# -*- coding: utf-8 -*-

"""
MyDicoTraining : Training Frame
"""
# -----------------------
# Importation des modules
# -----------------------
from tkinter import Frame, Label, Entry, Button, LabelFrame, StringVar
from tkinter import E, W, EW, SE, NE, LEFT, END
from tkinter.ttk import Combobox
#from tkinter.font import *
#from tkinter.constants import *
#from tkinter.messagebox import *
import logging as log

from my_dico import FR, FR_COUNT, FR_ERR_COUNT, FR_RATIO
from my_dico import EN, EN_COUNT, EN_ERR_COUNT, EN_RATIO
from my_dico import INFO

# -----------
# Constantes
# -----------
from my_vocable_constantes import FRAME_DEFAULT
from my_vocable_constantes import EN_TO_FR
from my_vocable_constantes import FR_TO_EN

CHECKOK_MSG = 'Juste'
CHECKOK_COLOR = 'green'
CHECKKO_MSG = 'Erreur'
CHECKKO_COLOR = 'red'


# ***************************
# *  Classe MyDicoTraining  *
# ***************************
class MyDicoTraining(Frame):
    """
    This frame implement the training.
    The parameters 'mode' define how to train :
        - english to french
        - french to english
    """
    # ------------ Constructeurs ------------
    def __init__(self, master, dico, mode=EN_TO_FR):
        "Contructeur de la classe MyDicoTraining"
        Frame.__init__(self, master)

        # Référence au dictionnaire
        self.mode = mode
        self.dico = dico
        self.current_category = StringVar()
        self.current_translation = None

        # Contruction du GUI
        self.make_frame()

        # Selection d'un premier mot
        self.next_translation()
    #\ __init__

    # ------------ Méthodes GUI ------------
    def make_frame(self):
        "Construction de l'interface GUI"

        # Titre de la fenêtre
        self.title_label = Label(self, font='Time 14 bold')
        self.title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=10)

        # Sélection des catégories
        self.category_label = Label(self, text="Apprentissage sur : ")
        self.category_label.grid(row=1, column=0)
        list_values = ['ALL']
        list_values.extend(self.dico.categories)
        self.category_combo = Combobox(self, state='readonly',
                                       textvariable=self.current_category,
                                       values=sorted(list_values))
        self.current_category.set("ALL")
        self.category_combo.grid(row=1, column=1)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_change)

        # Mot proposé
        self.word_asked_label = Label(self)
        self.word_asked_label.grid(row=2, column=0, sticky=E, padx=5, pady=5)
        self.word_asked = Label(self, font='Time 14 bold', fg='blue', bd=4)
        self.word_asked.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        # Information
        self.info_label = Label(self, text="Info. complémentaire : ")
        self.info_label.grid(row=3, column=0, sticky=E, padx=5, pady=5)
        self.info = Label(self, fg='gray')
        self.info.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # Réponse
        self.response_label = Label(self)
        self.response_label.grid(row=4, column=0, sticky=E, padx=5, pady=5)
        self.response = Entry(self)
        self.response.grid(row=4, column=1, columnspan=2, sticky=EW, padx=5, pady=5)
        self.response.bind('<KeyPress-Return>', self.on_check_event)

        # Zone statistique
        self.stat_labelframe = LabelFrame(self, bd=1, relief='solid')
        self.stat_labelframe.grid(row=5, column=0, rowspan=2, columnspan=2)
        self.counter_stat_label = Label(self.stat_labelframe, text="Nombre de tirage : ")
        self.counter_stat_label.grid(row=0, column=0, sticky=E)
        self.counter_stat = Label(self.stat_labelframe)
        self.counter_stat.grid(row=0, column=1, sticky=W)
        self.ok_stat_label = Label(self.stat_labelframe, text="Nombre de Ok : ")
        self.ok_stat_label.grid(row=1, column=0, sticky=E)
        self.ok_stat = Label(self.stat_labelframe)
        self.ok_stat.grid(row=1, column=1, sticky=W)
        self.ko_stat_label = Label(self.stat_labelframe, text="Nombre de Ko : ")
        self.ko_stat_label.grid(row=2, column=0, sticky=E)
        self.ko_stat = Label(self.stat_labelframe)
        self.ko_stat.grid(row=2, column=1, sticky=W)
        self.ratio_ok_stat_label = Label(self.stat_labelframe, text="% de réussite : ")
        self.ratio_ok_stat_label.grid(row=3, column=0, sticky=E)
        self.ratio_ok_stat = Label(self.stat_labelframe)
        self.ratio_ok_stat.grid(row=3, column=1, sticky=W)

        # Boutons ...
        # ... Controle de la réponse
        self.check_button = Button(self, text="Vérifier la réponse", command=self.on_check_event)
        self.check_button.grid(row=5, column=2, sticky=NE, padx=5, pady=5)

        # ... Fermer la fenetre
        self.quit_button = Button(self, text="Sortir", command=self.on_quit_event)
        self.quit_button.grid(row=6, column=2, sticky=SE, padx=5, pady=5)

        # ... Solution
        self.result_frame = LabelFrame(self, bd=1, relief='solid', text=" Résultat ")
        self.result_frame.grid(row=7, column=0, columnspan=3, stick=EW,
                               padx=5, pady=10, ipadx=5, ipady=5)
        self.result_label = Label(self.result_frame, justify=LEFT, font='Time 16 bold')
        self.result_label.grid(row=0, column=0, columnspan=2, stick=EW)
        self.asked_result_label = Label(self.result_frame, text="Mot proposé : ")
        self.asked_result_label.grid(row=1, column=0, sticky=E)
        self.asked_result = Label(self.result_frame, fg='blue')
        self.asked_result.grid(row=1, column=1, sticky=EW)
        self.written_result_label = Label(self.result_frame, text="Mots saisies : ")
        self.written_result_label.grid(row=2, column=0, sticky=E)
        self.written_result = Label(self.result_frame)
        self.written_result.grid(row=2, column=1, sticky=EW)
        self.answered_result_label = Label(self.result_frame, text="Réponse : ")
        self.answered_result_label.grid(row=3, column=0, sticky=E)
        self.answered_result = Label(self.result_frame, fg='green', font='12')
        self.answered_result.grid(row=3, column=1, sticky=EW)
        self.stat_result_label = Label(self.result_frame, text="Taux de réussite : ")
        self.stat_result_label.grid(row=4, column=0, sticky=E)
        self.stat_result = Label(self.result_frame)
        self.stat_result.grid(row=4, column=1, sticky=EW)


        # Mise à jour des libellés en fonction du mode d'entrainement
        if self.mode == EN_TO_FR:
            self.title_label["text"] = "Entrainement de l'anglais vers le français"
            self.word_asked_label["text"] = "Mot en anglais : "
            self.response_label["text"] = "Mot en français : "
        elif self.mode == FR_TO_EN:
            self.title_label["text"] = "Entrainement du français vers l'anglais"
            self.word_asked_label["text"] = "Mot en français : "
            self.response_label["text"] = "Mot en anglais : "
        else:
            log.error("MyDicoTraining.make_frame : Mode d'entrainement non défini.")

        self.grid()
        self.rowconfigure(6, weight=1)
        self.columnconfigure(2, weight=1)
        self.bind("<Configure>", self.on_resize_event)
    #\make_frame

    def init_category_combo(self):
        """Setup the category list"""
        import pdb; pdb.set_trace()
        self.category_combo.delete(0, END)
        self.category_combo.insert(END, "ALL")
        for category in sorted(self.dico.categories):
            self.category_combo.insert(END, category)
        self.category_combo.set("ALL")



    # ------------ Méthodes Event ------------
    def on_check_event(self, event=None):
        "Controle la réponse"

        if self.mode == EN_TO_FR:
            self.current_translation.set(EN_COUNT, int(self.current_translation.get(EN_COUNT))+1)
            if self.response.get() != self.current_translation[FR]:
                self.current_translation.set(EN_ERR_COUNT,
                                             int(self.current_translation[EN_ERR_COUNT])+1)
                self.result_label['text'] = CHECKKO_MSG
                self.result_label['fg'] = CHECKKO_COLOR
            else:
                self.result_label['text'] = CHECKOK_MSG
                self.result_label['fg'] = CHECKOK_COLOR


            self.answered_result['text'] = self.current_translation[FR]
            self.stat_result['text'] = "{:6.2f} %".format(self.current_translation[EN_RATIO]*100)
        else:
            self.current_translation.set(FR_COUNT, int(self.current_translation.get(FR_COUNT))+1)
            if self.response.get() != self.current_translation.get(EN):
                self.current_translation.set(FR_ERR_COUNT,
                                             int(self.current_translation.get(FR_ERR_COUNT))+1)
                self.result_label['text'] = CHECKKO_MSG
                self.result_label['fg'] = CHECKKO_COLOR
            else:
                self.result_label['text'] = CHECKOK_MSG
                self.result_label['fg'] = CHECKOK_COLOR

            self.answered_result['text'] = self.current_translation[EN]
            self.stat_result['text'] = "{:6.2f} %".format(self.current_translation[FR_RATIO]*100)

        self.written_result['text'] = self.response.get()
        self.asked_result['text'] = self.word_asked['text']

        self.next_translation()
    #\ on_check_event

    def on_category_change(self, event):
        """Actions when de category change"""
        self.next_translation()

    def on_quit_event(self):
        "Ferme la fenêtre"
        self.master.display_frame(FRAME_DEFAULT)
    #\ on_quit_event

    def on_resize_event(self, event):
        """Method used when the windows shape resize"""
        self.width = event.width
        self.height = event.height


    # ------------ Méthodes ------------
    def show(self):
        "Affiche l'écran"
        self.grid()
#        self.init_category_combo()
    #\show

    def next_translation(self):
        "Initialise une question"
        if self.mode == EN_TO_FR:
            # Selction d'une traduction
            self.current_translation = self.dico.shot_word(EN, category=self.category_combo.get())
            #Affiche de la traduction choisie
            self.word_asked["text"] = self.current_translation[EN]
            self.info["text"] = self.current_translation[INFO]
            self.counter_stat["text"] = str(self.current_translation[EN_COUNT])
            self.ok_stat["text"] = str(self.current_translation[EN_COUNT]\
                        -self.current_translation[EN_ERR_COUNT])
            self.ko_stat["text"] = str(self.current_translation[EN_ERR_COUNT])
            self.ratio_ok_stat["text"] = "{:6.2f} %".format(self.current_translation[EN_RATIO]*100)
        else:
            # Selction d'une traduction
            self.current_translation = self.dico.shot_word(FR, category=self.category_combo.get())
            #Affiche de la traduction choisie
            self.word_asked["text"] = self.current_translation.get(FR)
            self.info["text"] = self.current_translation.get(INFO)
            self.counter_stat["text"] = str(self.current_translation.get(FR_COUNT))
            self.ok_stat["text"] = str(int(self.current_translation.get(FR_COUNT))\
                        -int(self.current_translation.get(FR_ERR_COUNT)))
            self.ko_stat["text"] = str(self.current_translation.get(FR_ERR_COUNT))
            self.ratio_ok_stat["text"] = "{:6.2f} %".format(self.current_translation[FR_RATIO]*100)

        self.response.delete(0, END)
        self.response.focus_set()
    #\next_translation

# Fin du fichier my_dico_training.py
