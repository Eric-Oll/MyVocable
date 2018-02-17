# -*- coding: utf-8 -*-


"""
Ce module contient la classe TestsMyTtranslation.
Cette classe a pour objectif de valider la classe MyTranslation
"""
from unittest import TestCase
from my_dico import MyTranslation
from my_dico import EN, FR, INFO, CATEGORIES
from my_dico import EN_COUNT, EN_ERR_COUNT, EN_RATIO
from my_dico import FR_COUNT, FR_ERR_COUNT, FR_RATIO

class TestMyVocable(TestCase):

    def test__init__(self):
        """ Test la création d'un objet MyTranslation"""
        fileline = "No, that's incorrect. In fact,;Non, pas du tout. En réalité, ...;Une info;adverbe,noms;4;3;2;1"

        translation = MyTranslation(fileline)
        self.assertEqual(translation[EN], "No, that's incorrect. In fact,")
        self.assertEqual(translation[FR], "Non, pas du tout. En réalité, ...")
        self.assertEqual(translation[INFO], "Une info")
        self.assertListEqual(translation[CATEGORIES],['adverbe','noms'])
        self.assertEqual(translation[EN_COUNT], 4)
        self.assertEqual(translation[EN_ERR_COUNT], 3)
        self.assertEqual(translation[FR_COUNT], 2)
        self.assertEqual(translation[FR_ERR_COUNT], 1)
        self.assertEqual(translation[EN_RATIO], 1/4)
        self.assertEqual(translation[FR_RATIO], 1/2)

        translation = MyTranslation("Word", "Mot", "Info", ['Categorie'])
        self.assertEqual(translation[EN], "Word")
        self.assertEqual(translation[FR], "Mot")
        self.assertEqual(translation[INFO], "Info")
        self.assertListEqual(translation[CATEGORIES],['Categorie'])


        translation = MyTranslation(en="Word", fr="Mot", info="Info", categories=['Categorie'])
        self.assertEqual(translation[EN], "Word")
        self.assertEqual(translation[FR], "Mot")
        self.assertEqual(translation[INFO], "Info")
        self.assertListEqual(translation[CATEGORIES],['Categorie'])

    def test_get_all(self):
        """Test la sérialisation des informations sous la forme d'une str"""
        fileline = "too;aussi;info;adverbe;4;3;2;1"

        translation = MyTranslation(fileline)
        self.assertEqual(translation.get(),fileline)