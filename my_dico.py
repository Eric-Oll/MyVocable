# -*- coding: utf-8 -*-

"""
This module contains the class definition for the classes :
    - MyTranslate
    - MyDico
    - FormatError(Exception)


This classes implement the dictionnary of MyVocable
They use a file to store informations about the translation

The file is a CSV-file with semi-comma separator and with header.
The columns are :
 - english word or expression (Mot ou expression anglaise)
 - french word or expression (Mot ou expression française)
 - english to french selecting translation counter
     (Nombre de fois que la traduction a été présentée en anglais)
 - english to franch translating error counter
     (Nombre d'erreur dans la traduction anglais -> Français)
 - french to english selecting translation counter
     (Nombre de fois que la traduction a été présentée en français)
 - french to english translating error counter
     (Nombre d'erreur dans la traduction français -> anglais)
"""

# -----------------------
# Importation des modules
# -----------------------
#import string
import random
import logging as log

# --------------------
# Constantes
# --------------------
EN = "EN"
FR = "FR"
INFO = "INFO"
EN_COUNT = "EN_COUNT"
EN_ERR_COUNT = "EN_ERROR"
EN_RATIO = "EN_RATIO"
FR_COUNT = "FR_COUNT"
FR_ERR_COUNT = "FR_ERROR"
FR_RATIO = "FR_RATIO"



# =============================================================================
# Classe MyTranslate
# =============================================================================
class MyTranslate:
    """"Translating item (Item de traduction)"""

    # ------------ Constructeur  & Surcharge opÃ©rateur ------------
    def __init__(self, en="", fr="", info="",
                 en_count=0, en_error=0,
                 fr_count=0, fr_error=0,
                 lineDico=""):
        """Constructeur de la classe MyTranslate"""
        if lineDico != "":
            log.debug("Création de la ligne {}".format(lineDico))
            line = lineDico.split(";")
            log.debug("Nombre de composant de la ligne : {}".format(len(line)))
            if len(line) == 7:
                self.en_word = line[0]
                log.debug("Mot anglais : {}".format(self[EN]))
                self.fr_word = line[1]
                log.debug("Mot franÃ§ais : {}".format(self[FR]))
                self.info_word = line[2]
                log.debug("Information de traduction : {}".format(self[INFO]))
                self.en_count = line[3]
                log.debug("Compteur de proposition de mots anglais : {}".format(self[EN_COUNT]))
                try:
                    self.en_err_count = line[4]
                except Exception:
                    log.error("MyTranslate.__init__ : Problème dans l'écriture \
                              du compteur d'erreur de mots anglais : {} de type {}"
                              .format(line[4], type(line[4])))
                try:
                    self.fr_count = line[5]
                except Exception:
                    log.error("MyTranslate.__init__ : Problème dans l'écriture \
                              du compteur de proposition de mots français : {} de type {}"
                              .format(line[5], type(line[5])))
                try:
                    self.fr_err_count = line[6]
                except Exception:
                    log.error("MyTranslate.__init__ : Problème dans l'écriture \
                              du compteur d'erreur de mots français : {} de type {}"
                              .format(line[6], type(line[6])))
            elif len(line) == 2:
                self.en_word = line[0]
                self.fr_word = line[1]
                self.info_word = info
                self.en_count = en_count
                self.en_err_count = en_error
                self.fr_count = fr_count
                self.fr_err_count = fr_error
            elif len(line) == 3:
                self.en_word = line[0]
                self.fr_word = line[1]
                self.info_word = line[2]
                self.en_count = en_count
                self.en_err_count = en_error
                self.fr_count = fr_count
                self.fr_err_count = fr_error
            else:
                raise FormatError(lineDico, len(line))
        else:
            self.en_word = en
            self.fr_word = fr
            self.info_word = info
            self.en_count = en_count
            self.en_err_count = en_error
            self.fr_count = fr_count
            self.fr_err_count = fr_error

        #Mise Ã  jour des stat
        self.en_ratio_ok = 0
        self.fr_ratio_ok = 0
        self.update_english_stats()
        self.update_french_stats()
    #\__init__

    # =========================================================================
    # Specials methods
    # =========================================================================
    def __str__(self): # Retour la traduction sous la forme CSV
        return self.get()
    #\__str__

    def __getitem__(self, option):
        return self.get(option)
    #\__getitem__

    def __setitem__(self, option, value):
        try:
            self.set(option, value)
        except Exception:
            log.error("MyTranslate.__setitem__ : Erreur sur option '{}' avec \
                      la valeur '{}' de type '{}'"
                      .format(option, value, type(value)))
    #\__setitem__

    # ------------ MÃ©thodes ------------
    def get(self, option=""):
        """"Retour les Ã©lÃ©ments de traduction"""
        if option == "" or option == "ALL":
            return "{};{};{};{};{};{};{}".format(self.en_word, self.fr_word, self.info_word,
                                                 self.en_count, self.en_err_count,
                                                 self.fr_count, self.fr_err_count)
        elif option == EN:
            return self.en_word
        elif option == FR:
            return self.fr_word
        elif option == INFO:
            return self.info_word
        elif option == EN_COUNT:
            return int(self.en_count)
        elif option == EN_ERR_COUNT:
            return int(self.en_err_count)
        elif option == FR_COUNT:
            return int(self.fr_count)
        elif option == FR_ERR_COUNT:
            return int(self.fr_err_count)
        elif option == EN_RATIO:
            return float(self.en_ratio_ok)
        elif option == FR_RATIO:
            return float(self.fr_ratio_ok)
    #\get

    def set(self, option, value):
        "Modifie la valeur d'un Ã©lÃ©ment de la traduction"
        if value == "":
            return
        try:
            if option == EN:
                self.en_word = value
            elif option == FR:
                self.fr_word = value
            elif option == INFO:
                self.info_word = value
            elif option == EN_COUNT:
                self.en_count = int(value)
                self.update_english_stats()
            elif option == EN_ERR_COUNT:
                self.en_err_count = int(value)
                self.update_english_stats()
            elif option == FR_COUNT:
                self.fr_count = int(value)
                self.update_french_stats()
            elif option == FR_ERR_COUNT:
                self.fr_err_count = int(value)
                self.update_french_stats()
            elif option == EN_RATIO:
                self.en_ratio_ok = float(value)
            elif option == FR_RATIO:
                self.fr_ratio_ok = float(value)
        except Exception:
            log.error("MyTranslate.set : Erreur sur option '{}' avec la valeur \
                      '{}' de type '{}'".format(option, value, type(value)))
    #\set

    def update_english_stats(self):
        """Update the stats for english indicators"""
        try:
            if self[EN_COUNT] != 0:
                self[EN_RATIO] = float(self[EN_COUNT]-self[EN_ERR_COUNT])/self[EN_COUNT]
        except Exception:
            log.debug("MyTranslate.update_english_stats : Erreur dans le calcul \
                      du ratio avec EN_COUNT={} et EN_ERR_COUNT={}"
                      .format(self.en_count, self.en_err_count))
    #\update_english_stats

    def update_french_stats(self):
        """Update the stats for french indicators"""
        try:
            if int(self[FR_COUNT]) != 0:
                self[FR_RATIO] = float(self[FR_COUNT]-self[FR_ERR_COUNT])/self[FR_COUNT]
        except Exception:
            log.debug("MyTranslate.updateStatsFr : Erreur dans le calcul du ratio \
                      avec FR_COUNT={} et FR_ERR_COUNT={}"
                      .format(self.fr_count, self.fr_err_count))
    #\update_french_stats

    def ratio_value(self, langue=EN):
        """Return the error level.
        It uses by the sort_dico, itself uses by shot_word, to select a word"""
        if langue == EN:
            return self[EN_COUNT]-2*self[EN_ERR_COUNT]
        if langue == FR:
            return self[FR_COUNT]-2*self[FR_ERR_COUNT]
    #\ratio_value

# =============================================================================
# Classe MyDico
# =============================================================================
class MyDico:
    "Dictionnaire de traduction"
    # ------------ Constructeurs ------------
    def __init__(self, fichier=""):
        "Constructeur de la classe MyDico"
        self.filename = fichier
        self.words = []
    #\__init__

#    def count(self):
    def __len__(self):
        """Return the size of the dictionnary"""
        return len(self.words)
    #\count

    # ------------ MÃ©thodes ------------
    def load_dico(self, fichier=""):
        """Chargement du dictionnaire"""
        if fichier != "": # si on spécifie un dictionnaire à charger
            self.filename = fichier

        # Ouverture du dictionnaire
        try:
            file = open(self.filename, "r", encoding='utf8')
        except Exception:
            log.error("Le dictionnaire '{}' n'existe pas ou ne peut pas Ãªtre ouvert."
                      .format(self.filename))

        #Réinitialisation du dictionnaire
        self.words = []

        # Lecture du dictionnaire
        nb_ignore = 0
        lineread = file.readline()
        while lineread != "":
            try:
                translate = MyTranslate(lineDico=lineread.replace("\n", ""))
                self.words.append(translate)
            except FormatError as err:
                nb_ignore += 1
                log.error("Ligne en erreur : {} ; nb d'arguments = {}"
                          .format(err.error_line, err.items_count))

            lineread = file.readline()
        file.close()
    #\load_dico

    def save_dico(self, fichier=""):
        """Save the dictionnary into a file"""
        if fichier != "": # si on spÃ©cifie un nom de fichier pour la sauvegarde
            self.filename = fichier

        # Ouverture du dictionnaire
        try:
            file = open(self.filename, "w", encoding='utf8')
        except Exception:
            log.error("Le dictionnaire '{}' n'est pas accessible en Ã©criture."
                      .format(self.filename))

        try:
            for word in self.words:
                log.debug("Ecriture de : {}".format(word))
                print(word, file=file)
                #f.writeline(word.get())
        except Exception:
            log.error("Erreur dans la sauvegarde du dictionnaire '{}'.".format(self.filename))
        finally:
            file.close()
    #\save_dico

    def add_translate(self, translate):
        "Ajoute une traduction au dictionnaire"
        self.words.append(translate)
    #\add_translate

#OPT : Réduire les différent cas de type de tri par un seul cas générique
    def sort_dico(self, sortby=EN):
        "Trie le dictionnaire"
        if sortby == EN:
            try:
                self.words.sort(key=lambda translate: translate[EN])
            except BaseException as err:
                log.error("MyDico.sortDico : Erreur sur le tri en anglais :{}".format(err))
        elif sortby == FR:
            try:
                self.words.sort(key=lambda translate: translate[FR])
            except Exception:
                log.error("MyDico.sortDico : Erreur sur le tri en franÃ§ais.")
        elif sortby == EN_RATIO:
            try:
                self.words.sort(key=lambda translate: translate.en_ratio_ok)
            except Exception:
                log.error("MyDico.sortDico : Erreur sur le tri en franÃ§ais.")
        elif sortby == FR_RATIO:
            try:
                self.words.sort(key=lambda translate: translate.ratioValue(FR))
                # self.words.sort(key=lambda translate: translate.fr_ratio_ok)
            except Exception:
                log.error("MyDico.sortDico : Erreur sur le tri en franÃ§ais.")
    #\sort_dico

    def shot_word(self, langue=EN):
        "Selectionne une traduction"
        # langue = EN -> basÃ© sur les stat EN
        # langue = FR -> basÃ© sur les stat FR

        if langue == EN:
            self.sort_dico(EN_RATIO)
        if langue == FR:
            self.sort_dico(FR_RATIO)

        # On fait varier la borne sup. (rendre moins accessible les rÃ©ussite)
        borne_sup = random.randint(1, len(self))

        # On tire au hazard un Ã©lÃ©ment sur le segment restant
        return random.choice(self.words[0:borne_sup])
    #\shot_word


# =============================================================================
# Classes d'exception
# =============================================================================
class FormatError(Exception):
    """Error type about the format of dictionnary file"""
    def __init__(self, error_line, items_count):
        self.error_line = error_line
        self.items_count = items_count

# ==>  autotest -------------------------------------------------------------------
if __name__ == '__main__':
    #import sys
    #sys.path.append("C:\\Users\\eollivie\Documents\\Application\\BankPerfect8\\Scripts\\MyScriptBP")

    dico = MyDico("C:\\Users\\eollivie\\Documents\\Labo\\Pyhton\\MyVocable\\dico.csv")
    dico.load_dico()
    print(len(dico.words))
    for word in dico.words:
        print(word)
    # dico.saveDico()

# Fin du fichier my_dico.py
