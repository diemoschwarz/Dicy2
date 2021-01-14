#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

#############################################################################
# Intervals.py 
# Using intervals.
# Jérôme Nika, IRCAM STMS LAB
# copyleft 2016 - 2017
#############################################################################


""" 
Using Intervals
================
Some subclasses of :class:`~Label.Label` enable to define a notion of interval. The tools defined in this module handle such possibilities.
**Tutorial in** :file:`_Tutorials_/Label_and_intervals_tutorial.py`.
"""

from copy import deepcopy, copy
from .PrefixIndexing import *


def prefix_indexing_intervals(sequence, pattern, sequence_to_interval_fun = None, **args):
    """ Index the prefixes of a pattern in a sequence. TODO DIRE QU'IL FAUT DES SEQUENCES DE LABELS AVEC METHODE DELTA DEFINI
    LISTE DES PARAMETRES A TODOIFIER AUSSI
    FAUX NE DOIT NECESSAIREMENT ETRE DES LISTES DE LABELS !!! MAIS SEQUENCE ET PATTERN DOIVENT REPRESENTER DES INTERVALLES --> A CORRIGER.
    SPECIFIER QUELLE DOIT ETRE LA FORME D'UN LABEL D'INTERVAL
    
    :param sequence:
    :type sequence: list(label)
    :param pattern:
    :type pattern: list(label)
    :param equiv: [args] compararison function given as a lambda function, default: TODO IL FAUT METTRE LE NONE ET TOUT EN ARGUMENT
    :type equiv: function
    :param print_info: [args] print the details of the research? 
    :type print_info: int
    :return: BIEN DIRE CE QU'EST LA LISTE DE LISTES prefixes of the pattern in the sequence (key = length, value = list of left positions of prefixes of the pattern of length 'length' in the sequence) **and** length of the longest prefix
    :rtype: tuple ( dict (int -> list), int)
    :seealso: **Tutorial in** :file:`_Tutorials_/Label_and_intervals_tutorial.py`

    :!: **equiv** has to be consistent with the type of the elements in labels.


    :Example:

    >>> "TODO"
    """
    
    interval_sequence = sequence
    interval_pattern = pattern

    if not sequence_to_interval_fun is None:
        interval_sequence = sequence_to_interval_fun(interval_sequence, **args)
        interval_pattern = sequence_to_interval_fun(interval_pattern, **args)

    #print("LOOKING FOR INTERVALS {}".format(interval_pattern))

    prefixes , max_length = prefix_indexing(interval_sequence , interval_pattern, **args)
    for length,list_of_left_pos_in_sequence in prefixes.items():
        deltas = []
        for p in list_of_left_pos_in_sequence:
            # TODO FAIRE UN TRY POUR LA SOUSTRACTION DE LABELS QUI DOIT ETRE UN ENTIER. OU PAS ?
            delta = sequence[p].delta(pattern[0])
            deltas.append(delta)
        prefixes[length] = [[list_of_left_pos_in_sequence[i],deltas[i]] for i in range(0,len(list_of_left_pos_in_sequence))]

    return prefixes, max_length 


def filtered_prefix_indexing_intervals(sequence, pattern, sequence_to_interval_fun = None, **args):
    """ Filtered index of the prefixes of a pattern in a sequence (filtered regarding lengths and positions). TODO DIRE QU'IL FAUT DES SEQUENCES DE LABELS AVEC METHODE DELTA DEFINI
    LISTE DES PARAMETRES A TODOIFIER AUSSI
    FAUX NE DOIT NECESSAIREMENT ETRE DES LISTES DE LABELS !!! MAIS SEQUENCE ET PATTERN DOIVENT REPRESENTER DES INTERVALLES --> A CORRIGER.
    SPECIFIER QUELLE DOIT ETRE LA FORME D'UN LABEL D'INTERVAL
    
    :param sequence:
    :type sequence: list(label)
    :param pattern:
    :type pattern: list(label)
    :param authorized_indexes: [args] list of authorized indexes to filter the results 
    :type authorized_indexes: list (int)
    :param authorized_intervals: [args] list of authorized intervals to filter the results 
    :type authorized_intervals: list
    :param length_interval: [args] interval of length to filter the results.
    :type length_interval: tuple (int, int): absolute lengths** of the prefixes **or** tuple (float, float): fractions of the length of the longest prefix before filtering
    :param equiv: [args] compararison function given as a lambda function, default: TODO
    :type equiv: function
    :param print_info: [args] print the details of the research? 
    :type print_info: int
    :return: prefixes of the pattern in the sequence after filtering (key = length, value = list of left positions of prefixes of the pattern of length 'length' in the sequence) **and** length of the longest prefix
    :rtype: tuple (dict (int -> list), int)
    :seealso: **Tutorial in** :file:`_Tutorials_/Label_and_intervals_tutorial.py`

    :!: **equiv** has to be consistent with the type of the elements in labels.


    :Example:

    >>> "TODO"
    """

    interval_sequence = sequence
    interval_pattern = pattern

    if not sequence_to_interval_fun is None:
        interval_sequence = sequence_to_interval_fun(interval_sequence)
        interval_pattern = sequence_to_interval_fun(interval_pattern)

    if "equiv" in args.keys():
        equiv = args["equiv"]
    else:
        equiv = (lambda x,y : (x[1::] == y[1::]) and (x[0] == y[0] or x[0] is None or y[0] is None))
    if "print_info" in args.keys():
        print_info = args["print_info"]
    else:
        print_info = 0  

    tmp_max_length = 0
    filtered_index_delta_prefixes = {}
    length_interval = [] ###

    prefixes_delta, max_length = prefix_indexing_intervals(sequence, pattern, sequence_to_interval_fun = sequence_to_interval_fun, equiv = equiv, print_info = print_info)

    if "length_interval" in args.keys():
        length_interval = args["length_interval"]
        if type(length_interval[0]) == float or type(length_interval[1]) == float: ###
            length_interval = max(1,round(length_interval[0]*max_length)), min(round(length_interval[1]*max_length), max_length)

    for l in prefixes_delta.keys():
        filtered_positions_deltas  = prefixes_delta[l]

        if (len(length_interval) == 0) or (l <= length_interval[1] and l >= length_interval[0]): ###

            if l > tmp_max_length:
                tmp_max_length = l

            if "authorized_indexes" in args.keys():
                filtered_positions_deltas  = [p for p in filtered_positions_deltas if p[0] in args["authorized_indexes"]]

            if "authorized_intervals" in args.keys():
                filtered_positions_deltas  = [p for p in filtered_positions_deltas if p[1] in args["authorized_intervals"]]

            if len(filtered_positions_deltas) > 0:
                filtered_index_delta_prefixes [l] = filtered_positions_deltas  

    return filtered_index_delta_prefixes , tmp_max_length
