# Affiche le ratio de selection pour un dictionnaire



from MyDico import  *

dico = MyDico()
dico.loadDico('dico.csv')
dico.sortDico(FR_RATIO)
for item in dico.ListWords:
	print("EN='{}' (Count'={}, Err={}),\t\t FR='{}' (Count={}, Err={})\t\t => ratio = {}".format(
		item[EN], item[EN_COUNT], item[EN_ERR_COUNT],
		item[FR], item[FR_COUNT], item[FR_ERR_COUNT],
		item.ratioValue(FR)
	))
