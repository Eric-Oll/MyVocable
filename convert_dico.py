# -*- coding: utf-8 -*-

"""
This module contains the file convertissor from file :

The file is a CSV-file with semi-comma separator and with header.
The columns are :
 - english word or expression (Mot ou expression anglaise)
 - french word or expression (Mot ou expression française)
 - Information about the mean of the words
 - english to french selecting translation counter
     (Nombre de fois que la traduction a été présentée en anglais)
 - english to franch translating error counter
     (Nombre d'erreur dans la traduction anglais -> Français)
 - french to english selecting translation counter
     (Nombre de fois que la traduction a été présentée en français)
 - french to english translating error counter
     (Nombre d'erreur dans la traduction français -> anglais)

to file :

The file is a CSV-file with semi-comma separator and with header.
The columns are :
 - english word or expression (Mot ou expression anglaise)
 - french word or expression (Mot ou expression française)
 - Information about the mean of the words
 - Categories of the words (=list with comma-separator)
 - english to french selecting translation counter
     (Nombre de fois que la traduction a été présentée en anglais)
 - english to franch translating error counter
     (Nombre d'erreur dans la traduction anglais -> Français)
 - french to english selecting translation counter
     (Nombre de fois que la traduction a été présentée en français)
 - french to english translating error counter
     (Nombre d'erreur dans la traduction français -> anglais)

"""
import argparse
import os


def parse_arguments():
    """Analyse la ligne de commande du programme.
    usage: convert_dico [-h] [-s SOURCE] [-d DESTINATION]
    """
    parser = argparse.ArgumentParser(prog='convert_dico')
    parser.add_argument("-s", "--source",
                        help="Nom du fichier source")
    parser.add_argument("-d", "--destination",
                        help="Nom du fichier destination")
    return parser.parse_args()

def read_source(filename):
    """Reading generator file"""
    with open(filename, 'r') as file:
        line = file.readline()
        while line != '':
            yield line
            try:
                line = file.readline()
            except:
                break


def convert_line(line):
    fields = line.split(";")
    if len(fields) == 7:
        return "{};{};{};;{};{};{};{}".format(*fields)
    else:
        return line

def main():

    args = parse_arguments()
    if not os.path.isfile(args.source):
        return

    if args.destination == '':
        return

    iter_file = read_source(args.source)
    with open(args.destination, 'w') as file:
        for line in iter_file:
            file.write(convert_line(line))


if __name__ == "__main__":
    main()
