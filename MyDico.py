# Classes permettant de gérer le dictionnaire de traduction
# ---------------------------------------------------------
_DEBUG_=False
_DEBUG_VERBOSE_=False

# Structure d'un fichier : Fichier de type CSV avec séparateur point-virgule (;) et sans entête
# - Mot ou expression anglaise
# - Mot ou expression française
# - Nombre de fois que la traduction a été présentée en anglais
# - Nombre d'erreur dans la traduction anglais -> Français
# - Nombre de fois que la traduction a été présentée en français
# - Nombre d'erreur dans la traduction français -> anglais

# -----------------------
# Importation des modules
# -----------------------
import string
import random

try:
	import cPickle
except:
	import pickle

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

	
# --------------------
# Classes d'exception
# --------------------	
class FormatError(Exception):
		"Type d'erreur pour un problème de format de fichier"
		def __init__(self, lineErr, nbItem):
			self.LineErr=lineErr
			self.NbItem=nbItem
			
	
# ************************
# *  Classe MyTranslate  *
# ************************
class MyTranslate:
	"Item de traduction"
	# ------------ Attributs de la classe ------------
	EnWord=""	# Mot/Expression en anglais
	FrWord=""	# Mot/Expression en français
	InfoWord=""	# Donne une information sur le contexte
	EnNbRead=0	# Nombre de présentation du mot en anglais
	EnRatioOk=0.0	# Ratio de réussite pour le mot anglais
	EnNbErr=0	# Nombre d'erreur de traduction à partir du mot en anglais
	FrNbRead=0	# Nombre de présentation du mot en français
	FrNbErr=0	# Nombre d'erreur de traduction à partir du mot en français
	FrRatioOk=0.0	# Ratio de réussite pour le mot français
	
	# ------------ Constructeur  & Surcharge opérateur ------------
	def __init__(self, en="", fr="", info="", enCount=0, enError=0, frCount=0, frError=0, lineDico=""):
		"Constructeur de la classe MyTranslate"
		if lineDico !="":
			if _DEBUG_ : print("Création de la ligne {}".format(lineDico))
			line=lineDico.split(";")
			if _DEBUG_ : print("Nombre de composant de la ligne : {}".format(len(line)))
			if len(line) == 7:
				self[EN]=line[0]
				if _DEBUG_ : print("Mot anglais : {}".format(self[EN]))
				self[FR]=line[1]
				if _DEBUG_ : print("Mot français : {}".format(self[FR]))
				self[INFO]=line[2]
				if _DEBUG_ : print("Information de traduction : {}".format(self[INFO]))
				self[EN_COUNT]=line[3]
				if _DEBUG_ : print("Compteur de proposition de mots anglais : {}".format(self[EN_COUNT]))
				try: self[EN_ERR_COUNT]=line[4]
				except: print("MyTranslate.__init__ : Problème dans l'écriture du compteur d'erreur de mots anglais : {} de type {}".format(line[4],type(line[4])))
				try: self[FR_COUNT]=line[5]
				except: print("MyTranslate.__init__ : Problème dans l'écriture du compteur de proposition de mots français : {} de type {}".format(line[5],type(line[5])))
				try: self[FR_ERR_COUNT]=line[6]
				except: print("MyTranslate.__init__ : Problème dans l'écriture du compteur d'erreur de mots français : {} de type {}".format(line[6],type(line[6])))
			elif len(line) == 2:
				self.EnWord=line[0]
				self.FrWord=line[1]
				self.InfoWord=info
				self.EnNbRead=enCount
				self.EnNbErr=enError	
				self.FrNbRead=frCount
				self.FrNbErr=frError
			elif len(line) == 3:
				self.EnWord=line[0]
				self.FrWord=line[1]
				self.InfoWord=line[2]
				self.EnNbRead=enCount
				self.EnNbErr=enError	
				self.FrNbRead=frCount
				self.FrNbErr=frError
			else:
				raise FormatError(lineDico,len(line))
		else:
			self.EnWord=en
			self.FrWord=fr
			self.InfoWord=info
			self.EnNbRead=enCount	
			self.EnNbErr=enError	
			self.FrNbRead=frCount
			self.FrNbErr=frError
			
		#Mise à jour des stat
		# self.updateEnRatio()
		# self.updateFnRatio()
	#\__init__
	
	def __str__(self): # Retour la traduction sous la forme CSV
		return self.get()
	#\__str__
	
	def __getitem__(self, option):
		if _DEBUG_VERBOSE_: print("MyTranslate.__getitem__ : option = {} / Return = '{}' de type {}.".format(option,self.get(option),type(self.get(option))))
		return self.get(option)
	#\__getitem__
	
	def __setitem__(self, option, value):
		try:
			if _DEBUG_VERBOSE_: print("MyTranslate.__setitem__ : option = {} / value = '{}' / type of value = {}.".format(option, value, type(value)))
			self.set(option, value)
		except:
			print("MyTranslate.__setitem__ : Erreur sur option '{}' avec la valeur '{}' de type '{}'".format(option, valeur, type(valeur)))		
	#\__setitem__
	
	# ------------ Méthodes ------------
	def get(self, option=""):
		"Retour les éléments de traduction"
		if option == "" or option == "ALL" :
			return "{};{};{};{};{};{};{}".format(self.EnWord, self.FrWord, self.InfoWord, self.EnNbRead, self.EnNbErr, self.FrNbRead, self.FrNbErr)
		elif option == EN: return self.EnWord
		elif option == FR: return self.FrWord
		elif option == INFO: return self.InfoWord
		elif option == EN_COUNT: return int(self.EnNbRead)
		elif option == EN_ERR_COUNT: return int(self.EnNbErr)
		elif option == FR_COUNT: return int(self.FrNbRead)
		elif option == FR_ERR_COUNT: return int(self.FrNbErr)
		elif option == EN_RATIO : return float(self.EnRatioOk)
		elif option == FR_RATIO: return float(self.FrRatioOk)
	#\get

	def set(self, option, value):
		"Modifie la valeur d'un élément de la traduction"
		if value == "": return
		try:
			if _DEBUG_VERBOSE_: print("MyTranslate.set : option = {} / value = '{}' / type of value = {}.".format(option, value, type(value)))
			if option == EN: self.EnWord=value
			elif option == FR: self.FrWord=value
			elif option == INFO: self.InfoWord=value
			elif option == EN_COUNT:
				self.EnNbRead=int(value)
				self.updateStatsEn()
			elif option == EN_ERR_COUNT: 
				self.EnNbErr=int(value)
				self.updateStatsEn()
			elif option == FR_COUNT: 
				self.FrNbRead=int(value)
				self.updateStatsFr()
			elif option == FR_ERR_COUNT: 
				self.FrNbErr=int(value)
				self.updateStatsFr()
			elif option == EN_RATIO:
				self.EnRatioOk=float(value)
			elif option == FR_RATIO:
				self.FrRatioOk=float(value)
		except: 
			print("MyTranslate.set : Erreur sur option '{}' avec la valeur '{}' de type '{}'".format(option, valeur, type(valeur)))
	#\set
	
	def updateStatsEn(self):
		try:
			if self[EN_COUNT] !=0: self.EnRatioOk=float(int(self.EnNbRead)-int(self.EnNbErr))/int(self.EnNbRead)
		except:
			if _DEBUG_: print("MyTranslate.updateStatsEn : Erreur dans le calcul du ratio avec EN_COUNT={} et EN_ERR_COUNT={}".format(self.EnNbRead, self.EnNbErr))
	#\updateStatsEn
	
	def updateStatsFr(self):
		try:
			if int(self[FR_COUNT]) !=0: self[FR_RATIO]= float(self[FR_COUNT]-self[FR_ERR_COUNT])/self[FR_COUNT]
		except:
			if _DEBUG_: print("MyTranslate.updateStatsFr : Erreur dans le calcul du ratio avec FR_COUNT={} et FR_ERR_COUNT={}".format(self.FrNbRead, self.FrNbErr))
	#\updateStatsFr
	
	def ratioValue(self, langue=EN):
		if langue==EN: return self[EN_COUNT]-2*self[EN_ERR_COUNT]
		if langue==FR: return self[FR_COUNT]-2*self[FR_ERR_COUNT]
	#\ratioValue

# *******************
# *  Classe MyDico  *
# *******************
class MyDico:
	"Dictionnaire de traduction"
	# ------------ Attributs de la classe ------------
	FileName=""		# Nom (+chemin) du fichier dictionnaire
	ListWords=[]	# Liste des traductions
	
	# ------------ Constructeurs ------------
	def __init__(self, fichier=""):
		"Constructeur de la classe MyDico"
		self.FileName=fichier
	#\__init__
	
	def __contains__(self):
		return self.ListWords
	#\__contains__
	
	# ------------ Méthodes ------------
	def loadDico(self, fichier=""):
		"Chargement du dictionnaire"
		# Controle si on spécifie un dictionnaire à charger
		if fichier != "" :
			self.FileName=fichier
			
		# Ouverture du dictionnaire
		try:
			f=open(self.FileName,"r", encoding='utf8')
		except:
			print("Le dictionnaire '%s' n'existe pas ou ne peut pas être ouvert." % self.FileName)
		
		#Réinitialisation du dictionnaire
		self.ListWords=[]
		
		# Lecture du dictionnaire
		nbIgnore=0
		lineread=f.readline()
		while lineread != "" :
			try:
				translate=MyTranslate(lineDico=lineread.replace("\n",""))
				self.ListWords.append(translate)
			except FormatError as err:
				nbIgnore=nbIgnore+1	
				print("Ligne en erreur : %s ; nb d'arguments = %s" %(err.LineErr, err.NbItem))
				
			lineread=f.readline()
		f.close()
	#\loadDico
	
	def saveDico(self, fichier=""):
		"Sauvegarde du dictionnaire"
		# Controle si on spécifie un nom de fichier pour la sauvegarde
		if fichier != "" :
			self.FileName=fichier
		
		# Ouverture du dictionnaire
		try:
			f=open(self.FileName,"w", encoding='utf8')
		except:
			print("Le dictionnaire '%s' n'est pas accessible en écriture." % self.FileName)	
		
		try:
			for word in self.ListWords:
				print("Ecriture de : %s" % word)
				print(word, file=f)
				#f.writeline(word.get())
		except:
			print("Erreur dans la sauvegarde du dictionnaire '%s'." % self.FileName)
		finally:
			f.close()
	#\saveDico
	
	def addTranslate(self, translate):
		"Ajoute une traduction au dictionnaire"
		self.ListWords.append(translate)
	#\addTranslate
	
	def sortDico(self, sortby=EN):
		"Trie le dictionnaire"
		if sortby == EN:
			try:
				self.ListWords.sort(key=lambda translate: translate.EnWord)
			except BaseException as err:
				if _DEBUG_: 
					print("MyDico.sortDico : Erreur sur le tri en anglais.")
					print(err.message)
		elif sortby == FR:
			try:
				self.ListWords.sort(key=lambda translate: translate.FrWord)
			except:
				if _DEBUG_: print("MyDico.sortDico : Erreur sur le tri en français.")
		elif sortby == EN_RATIO:
			try:
				self.ListWords.sort(key=lambda translate: translate.EnRatioOk)
			except:
				if _DEBUG_: print("MyDico.sortDico : Erreur sur le tri en français.")
		elif sortby == FR_RATIO:
			try:
				self.ListWords.sort(key=lambda translate: translate.ratioValue(FR))
				# self.ListWords.sort(key=lambda translate: translate.FrRatioOk)
			except:
				if _DEBUG_: print("MyDico.sortDico : Erreur sur le tri en français.")
	#\sortDico
	
		
	def count(self):
		"Retourne le nombre de mot du dictionnaire"
		if _DEBUG_: print("MyDico.count : Nombre d'éléments du dictionnaire = %s." % len(self.ListWords))
		return len(self.ListWords)
	#\count


	def shotWord(self, langue=EN):
		"Selectionne une traduction"
		# langue = EN -> basé sur les stat EN
		# langue = FR -> basé sur les stat FR
		
		if langue == EN: self.sortDico(EN_RATIO)
		if langue == FR: self.sortDico(FR_RATIO)
		
		# On fait varier la borne sup. (rendre moins accessible les réussite)
		borne_sup=random.randint(1, self.count())
		
		# On tire au hazard un élément sur le segment restant
		return random.choice(self.ListWords[0:borne_sup])
		# selectedItem=[]
		# refItem=self.ListWords[0]
		# for item in self.ListWords:
			# if refItem.ratioValue(langue) == item.ratioValue(langue):
				# selectedItem.append(item)
			# else: break
		
		# return random.choice(selectedItem)
	#\shotWord
	
# ==>  autotest -------------------------------------------------------------------
if __name__ == '__main__' :
	#import sys
	#sys.path.append("C:\\Users\\eollivie\Documents\\Application\\BankPerfect8\\Scripts\\MyScriptBP")

	dico = MyDico("C:\\Users\\eollivie\\Documents\\Labo\\Pyhton\\MyVocable\\dico.csv")
	dico.loadDico()
	print(len(dico.ListWords))
	for word in dico.ListWords:
		print(word)
	# dico.saveDico()
	
# Fin du fichier MyDico.py	