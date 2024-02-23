###############################################################################
#                                  SlitherLink                                #
#                                Alain Coserariu                              #
###############################################################################


# -----------------------------Fonctions diverses------------------------------


def charger_grille(nom_fichier):
    """
    Charge une grille depuis un fichier texte

    :param nom_fichier: nom du fichier contenant la grille
    :return: (indice, etat)
    indice :tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    etat :dictionnaire comportant l'information de chaque segments non
    vierge
    None : Si la grille indice n'est pas conforme
    """
    with open("grilles/" + nom_fichier, 'r') as grille:
        lignes = grille.readlines()
        indice = []
        etat = {}

        for ligne in lignes:
            ligne_indice = []
            if ligne[0] != "e":  # Si on doit écrire dans le dictionnaire
                for caractere in ligne:
                    if caractere == '_':
                        ligne_indice.append(None)
                    elif caractere in ['0', '1', '2', '3']:
                        ligne_indice.append(int(caractere))
                    elif caractere != "\n":
                        return None
                indice.append(ligne_indice)
            else:
                segment = ((int(ligne[1]), int(ligne[2])),
                           (int(ligne[3]), int(ligne[4])))
                if ligne[5] == '-':
                    etat[segment] = -int(ligne[6])
                else:
                    etat[segment] = int(ligne[5])

        if indice == [[]]:
            return None, None

        for k in indice:
            if len(k) != len(indice[0]):
                return None, None

        return indice, etat


def sauvegarder_grille(indice, etat):
    """
    Sauvegarde une grille dans un fichier texte pour reprendre une partie plus
    tard (même après fermeture du programme)

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :return: Void
    """

    with open('grilles/sauvegarde.txt', 'w') as fichier:
        for y in range(len(indice)):
            for x in range(len(indice[0])):
                if indice[y][x] is None:
                    fichier.write("_")
                elif indice[y][x] in [0, 1, 2, 3]:
                    fichier.write(str(indice[y][x]))
                if x == len(indice[0]) - 1:
                    fichier.write("\n")

        for clef in etat:
            fichier.write("e" + str(clef[0][0]) + str(clef[0][1]) +
                          str(clef[1][0]) + str(clef[1][1]) + str(etat[clef]) +
                          "\n")


def element_dictionnaire(dictionnaire, element):
    """
    Cherche la première clef qui correspond à element dans dictionnaire

    :param dictionnaire: Dictionnaire dans lequelle on effectue la recherche
    :param element: Elément qui correpond à une clef
    :return: clef
             None : Si il n'y as pas de clef qui correspondent à un élément

    >>> element_dictionnaire({"lundi": 1, "mardi": 2, "mercredi": 3}, 2)
    'mardi'

    >>> element_dictionnaire({"lundi": 1, "mardi": 2, "mercredi": 3}, 7) \
    is None
    True
    """
    valeur_dictionnaire = []
    clef_dictionnaire = []
    for k in dictionnaire:
        valeur_dictionnaire.append(dictionnaire[k])
        clef_dictionnaire.append(k)

    increment = 0
    while increment < len(valeur_dictionnaire) - 1 and \
            valeur_dictionnaire[increment] != element:
        increment += 1

    if valeur_dictionnaire[increment] == element:
        return clef_dictionnaire[increment]
    else:
        return None


def ordonner_sommet(segment):
    """
    Classe par ordre croissant les deux couples de coordonnées de segment

    :param segment: couple de coordonnées entre deux sommets
    :return: segment

    >>> ordonner_sommet(((1, 1), (1, 0)))
    ((1, 0), (1, 1))

    >>> ordonner_sommet(((1, 0), (0, 1)))
    ((1, 0), (0, 1))
    """
    sommet_un = segment[0]
    sommet_deux = segment[1]

    if sommet_un[1] > sommet_deux[1]:
        return sommet_deux, sommet_un
    elif sommet_un[1] == sommet_deux[1]:
        if sommet_un[0] > sommet_deux[0]:
            return sommet_deux, sommet_un
    return sommet_un, sommet_deux


# ------------------Fonctions d'informations de la grille----------------------


def compteur_segments_etat(etat):
    """
    Compte le nombre de segments placées dans le dictionnaire etat

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :return: nombre de segment placées

    >>> compteur_segments_etat({})
    0

    >>> compteur_segments_etat({((0, 0), (0, 1)): 1})
    1
    """
    compteur_segment_etat = 0
    for k in etat:
        if etat[k] == 1:
            compteur_segment_etat += 1
    return compteur_segment_etat


def est_trace(etat, segment):
    """
    Verifie si le segment avec une information "tracé" est dans le dictionnaire
    etat

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: Bool : true si segment est dans etat et qu'il est "placé"

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> est_trace(etat, ((1, 0), (1, 1)))
    True

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> est_trace(etat, ((1, 1), (1, 0)))
    True

    >>> etat = {((1, 0), (1, 1)) : 2}
    >>> est_trace(etat, ((1, 1), (1, 0)))
    False

    >>> etat = {}
    >>> est_trace(etat, ((1, 1), (1, 0)))
    False
    """
    segment = ordonner_sommet(segment)
    if segment in etat and etat[segment] == 1:
        return True
    return False


def est_interdit(etat, segment):
    """
    Verifie si le segment avec une information "interdit" est dans le
    dictionnaire etat

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: Bool : true si segment est dans etat et qu'il est "interdit"

    >>> etat = {((1, 0), (1, 1)) : -1}
    >>> est_interdit(etat, ((1, 0), (1, 1)))
    True

    >>> etat = {((1, 0), (1, 1)) : -1}
    >>> est_interdit(etat, ((1, 1), (1, 0)))
    True

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> est_interdit(etat, ((1, 1), (1, 0)))
    False

    >>> etat = {}
    >>> est_interdit(etat, ((1, 1), (1, 0)))
    False
    """
    segment = ordonner_sommet(segment)
    if segment in etat and etat[segment] == -1:
        return True
    return False


def est_vierge(etat, segment):
    """
    Vérifie si un segment est dans le dictionnaire etat

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: Bool : true si segment n'est pas dans etat

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> est_vierge(etat, ((1, 0), (1, 1)))
    False

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> est_vierge(etat, ((1, 1), (1, 0)))
    False

    >>> etat = {}
    >>> est_vierge(etat, ((1, 0), (1, 1)))
    True

    >>> etat = {((1, 0), (1, 1)) : 2}
    >>> est_vierge(etat, ((1, 0), (1, 1)))
    False
    """
    segment = ordonner_sommet(segment)
    if segment in etat:
        return False
    return True


def statut_case(indice, etat, case):
    """
    Vérifie les informations d'une case : -indice satisfait
                                          -encore possible de satisfaire
                                          l'indice
                                          -trop de segments/croix autour de
                                          l'indice
                                          -pas d'indice

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param case: coordonnées dans le tableau indice référent à une case
    :return: None : si l'indice ne donne aucun renseignement
             -1 : si il y a trop de segments autour de l'indice
             0 : si l'indice est satifait
             1 : si il n'y a pas assez de segments pour satisfaire l'indice

    >>> indice = [\
    [1, None],\
    [None, 1]\
    ]
    >>> etat = {((0, 0), (0, 1)) : 1, \
                ((1, 1), (2, 1)) : 1, \
                ((1, 1), (1, 2)) : 1}
    >>> statut_case(indice, etat, (0, 0))
    0

    >>> statut_case(indice, etat, (1, 1))
    -1

    >>> statut_case(indice, etat, (0, 1)) is None
    True
    """
    x = case[0]
    y = case[1]
    if indice[y][x] is None:
        return None
    else:
        liste_segments = [((x, y), (x + 1, y)),
                          ((x + 1, y), (x + 1, y + 1)),
                          ((x + 1, y + 1), (x, y + 1)),
                          ((x, y + 1), (x, y))]
        compteur_segments = 0
        compteur_croix = 0
        for k in liste_segments:
            if est_trace(etat, k):
                compteur_segments += 1
            elif est_interdit(etat, k):
                compteur_croix += 1

        if compteur_segments > indice[y][x] or \
                compteur_croix > 4 - indice[y][x]:
            return -1
        elif compteur_segments == indice[y][x]:
            return 0
        else:
            return 1


def segments_traces(etat, sommet):
    """
    Renvoie la liste des segments tracés adjacents à un sommet

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param sommet: couple de coordonnées représentent un point de la grille
    :return: liste des segments tracés adjacent au sommets

    >>> etat = {\
    ((1, 0), (1, 1)) : 1,\
    ((0, 1), (1, 1)) : 2,\
    ((1, 1), (1, 2)) : 1,\
    ((1, 1), (2, 1)) : 1}
    >>> segments_traces(etat, (1, 1))
    [((1, 1), (2, 1)), ((1, 1), (1, 2)), ((1, 0), (1, 1))]

    >>> etat = {\
    ((1, 0), (1, 1)) : 1,\
    ((1, 1), (1, 2)) : 1,\
    ((1, 1), (2, 1)) : 1}
    >>> segments_traces(etat, (1, 1))
    [((1, 1), (2, 1)), ((1, 1), (1, 2)), ((1, 0), (1, 1))]
    """
    liste_segment_traces = []
    x = sommet[0]
    y = sommet[1]
    liste_segments = [((x, y), (x + 1, y)),
                      ((x, y), (x, y + 1)),
                      ((x - 1, y), (x, y)),
                      ((x, y - 1), (x, y))]

    for k in liste_segments:
        if k in etat and etat[k] == 1:
            liste_segment_traces.append(k)

    return liste_segment_traces


def segments_interdits(etat, sommet):
    """
    Renvoie la liste des segments interdits adjacents à un sommet

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param sommet: couple de coordonnées représentent un point de la grille
    :return: liste des segments tracés adjacent au sommets

    >>> etat = {\
    ((1, 0), (1, 1)) : 1,\
    ((0, 1), (1, 1)) : 2,\
    ((1, 1), (1, 2)) : 1,\
    ((1, 1), (2, 1)) : 1}
    >>> segments_interdits(etat, (1, 1))
    [((0, 1), (1, 1))]

    >>> etat = {\
    ((1, 0), (1, 1)) : 2,\
    ((1, 1), (1, 2)) : 1,\
    ((1, 1), (2, 1)) : 2}
    >>> segments_interdits(etat, (1, 1))
    [((1, 1), (2, 1)), ((1, 0), (1, 1))]
    """
    liste_segment_traces = []
    x = sommet[0]
    y = sommet[1]
    liste_segments = [((x, y), (x + 1, y)),
                      ((x, y), (x, y + 1)),
                      ((x - 1, y), (x, y)),
                      ((x, y - 1), (x, y))]

    for k in liste_segments:
        if k in etat and etat[k] == 2:
            liste_segment_traces.append(k)

    return liste_segment_traces


def segments_vierges(etat, sommet):
    """
    Renvoie la liste des segments vierges adjacent à un sommet

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param sommet: couple de coordonnées représentent un point de la grille
    :return: liste des segments tracés adjacent au sommets

    >>> etat = {\
    ((1, 0), (1, 1)) : 1,\
    ((0, 1), (1, 1)) : 2,\
    ((1, 1), (1, 2)) : 1,\
    ((1, 1), (2, 1)) : 1}
    >>> segments_vierges(etat, (1, 1))
    []

    >>> etat = {\
    ((1, 0), (1, 1)) : 2,\
    ((1, 1), (1, 2)) : 1,\
    ((1, 1), (2, 1)) : 2}
    >>> segments_vierges(etat, (1, 1))
    [((0, 1), (1, 1))]
    """
    liste_segment_traces = []
    x = sommet[0]
    y = sommet[1]
    liste_segments = [((x, y), (x + 1, y)),
                      ((x, y), (x, y + 1)),
                      ((x - 1, y), (x, y)),
                      ((x, y - 1), (x, y))]

    for k in liste_segments:
        if k not in etat:
            liste_segment_traces.append(k)

    return liste_segment_traces


def cases_adjacent_segment(segment, indice):
    """
    Détermine les cases adjacentes à un segment

    :param segment: couple de coordonnées entre deux sommets
    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :return: list: liste des cases adjacentes à un segment

    >>> indice = [\
    [None, None, None, None, None],\
    [2, 2, None, None, 3],\
    [2, 1, None, 0, 3],\
    [None, None, 2, 0, None],\
    [2, 2, 2, 2, None],\
    ]
    >>> cases_adjacent_segment(((1, 1), (1, 2)), indice)
    [(1, 1), (0, 1)]

    >>> cases_adjacent_segment(((1, 2), (1, 1)), indice)
    [(1, 1), (0, 1)]

    >>> cases_adjacent_segment(((2, 1), (1, 1)), indice)
    [(1, 1), (1, 0)]

    >>> cases_adjacent_segment(((0, 0), (0, 1)), indice)
    [(0, 0)]

    >>> cases_adjacent_segment(((5, 4), (5, 5)), indice)
    [(4, 4)]

    >>> indice = [\
    [1, None],\
    [None, 1],\
    ]
    >>> cases_adjacent_segment(((1, 2), (2, 2)), indice)
    [(1, 1)]
    """
    segment = ordonner_sommet(segment)
    cases_adjacent = [(segment[0][0], segment[0][1])]
    if segment[0][0] < segment[1][0]:
        cases_adjacent.append((segment[0][0], segment[0][1] - 1))
    elif segment[0][1] < segment[1][1]:
        cases_adjacent.append((segment[0][0] - 1, segment[0][1]))

    cases_adjacent_verifie = []
    for case in cases_adjacent:
        if 0 <= case[0] < len(indice[0]) and 0 <= case[1] < len(indice):
            cases_adjacent_verifie.append(case)

    return cases_adjacent_verifie


# ------------Fonctions de complétion des segments de la grille----------------


def tracer_segment(etat, segment):
    """
    Ajoute dans le dictionnaire etat l'information de placement d'un segment
    par le joueur

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: None

    >>> etat = {}
    >>> tracer_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {((1, 0), (1, 1)): 1}

    >>> etat = {}
    >>> tracer_segment(etat, ((1, 1), (1, 0)))
    >>> print(etat)
    {((1, 0), (1, 1)): 1}

    >>> etat = {((1, 0), (1, 1)) : -1}
    >>> tracer_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {((1, 0), (1, 1)): 1}

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> tracer_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {}

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> tracer_segment(etat, ((1, 1), (1, 0)))
    >>> print(etat)
    {}
    """
    segment = ordonner_sommet(segment)
    if est_vierge(etat, segment) or est_interdit(etat, segment):
        etat[segment] = 1
    else:
        effacer_segment(etat, segment)


def interdire_segment(etat, segment):
    """
    Ajoute dans le dictionnaire etat l'information de placement d'une croix
    par le joueur

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: None

    >>> etat = {}
    >>> interdire_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {((1, 0), (1, 1)): 2}

    >>> etat = {}
    >>> interdire_segment(etat, ((1, 1), (1, 0)))
    >>> print(etat)
    {((1, 0), (1, 1)): 2}

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> interdire_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {((1, 0), (1, 1)): 2}

    >>> etat = {((1, 0), (1, 1)) : 2}
    >>> interdire_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {}

    >>> etat = {((1, 0), (1, 1)) : 2}
    >>> interdire_segment(etat, ((1, 1), (1, 0)))
    >>> print(etat)
    {}
    """
    segment = ordonner_sommet(segment)
    if est_trace(etat, segment) or est_vierge(etat, segment):
        etat[segment] = 2
    else:
        effacer_segment(etat, segment)


def effacer_segment(etat, segment):
    """
    Efface du dictionnaire etat l'information concernant un segment

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: None

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> effacer_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {}

    >>> etat = {((1, 0), (1, 1)) : 1}
    >>> effacer_segment(etat, ((1, 1), (1, 0)))
    >>> print(etat)
    {}

    >>> etat = {((1, 0), (1, 1)) : 2}
    >>> effacer_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {}

    >>> etat = {}
    >>> effacer_segment(etat, ((1, 0), (1, 1)))
    >>> print(etat)
    {}
    """
    segment = ordonner_sommet(segment)
    if segment in etat:
        del (etat[segment])


# ---------------------Fonctions de condition de victoire----------------------


def indice_satisfait(indice, etat):
    """
    Vérifie si tous les indices sont bien respectés

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :return: bool : True si tous les indices sont respectés

    >>> indice = [\
    [1, None],\
    [None, 1],\
    ]
    >>> etat = {((0, 0), (0, 1)) : 1, ((1, 1), (2, 1)) : 1}
    >>> indice_satisfait(indice, etat)
    True

    >>> indice = [\
    [2, None],\
    [None, 1]\
    ]
    >>> etat = {((0, 0), (0, 1)) : 1, ((1, 1), (2, 1)) : 1}
    >>> indice_satisfait(indice, etat)
    False

    >>> indice = [\
    [1, None],\
    [None, 1]\
    ]
    >>> etat = {((0, 0), (0, 1)) : 1, ((1, 1), (2, 1)) : 1, \
    ((0, 0), (1, 0)) : 1}
    >>> indice_satisfait(indice, etat)
    False
    """
    for y in range(len(indice)):
        for x in range(len(indice[y])):
            if statut_case(indice, etat, (x, y)) is not None and \
                    statut_case(indice, etat, (x, y)) != 0:
                return False
    return True


def boucle(etat, segment):
    """
    Vérifie que le segment est dans une boucle

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: nombre de segment dans la boucle
             None : si le segment n'est pas dans une boucle
    """
    compteur_segment = 1

    depart = segment[0]
    if len(segments_traces(etat, depart)) != 2:
        return None

    precedent = depart
    courent = segment[1]
    while courent != depart:
        liste_segment_traces = segments_traces(etat, courent)
        if len(liste_segment_traces) != 2:
            return None

        for segment in liste_segment_traces:
            for sommet in segment:
                if sommet != courent and sommet != precedent:
                    nouveau_sommet = sommet

        precedent = courent
        courent = nouveau_sommet

        compteur_segment += 1

    return compteur_segment


def boucle_unique(etat, segment):
    """
    Vérifie que dans l'état du jeu il y a bien une seule et unique boucle en
    partant d'un segment

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: int : nombre de segments si le jeu est une boucle unique
             None : si le jeu n'est pas une boucle unique

    >>> etat = {\
    ((0, 0), (1, 0)) : 1,\
    ((1, 0), (1, 1)) : 1,\
    ((0, 1), (1, 1)) : 1,\
    ((0, 0), (0, 1)) : 1\
    }
    >>> boucle_unique(etat, ((0, 0), (1, 0)))
    4

    >>> etat = {\
    ((0, 0), (1, 0)) : 1,\
    ((1, 0), (1, 1)) : 1,\
    ((0, 1), (1, 1)) : 1\
    }
    >>> boucle_unique(etat, ((0, 0), (1, 0))) is None
    True

    >>> etat = {\
    ((0, 0), (1, 0)) : 1,\
    ((1, 0), (1, 1)) : 1,\
    ((0, 1), (1, 1)) : 1,\
    ((0, 0), (0, 1)) : 1,\
    ((3, 0), (3, 1)) : 1\
    }
    >>> boucle_unique(etat, ((0, 0), (1, 0))) is None
    True
    """
    compteur_segment = boucle(etat, segment)

    if compteur_segment != compteur_segments_etat(etat):
        return None

    return compteur_segment


def affichage_victoire_console(indice, etat, segment):
    """
    À chaque coup joué, affiche un message sur la console indiquant le statut
    de chacune des deux conditions de victoires

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param segment: couple de coordonnées entre deux sommets
    :return: Void
    """
    print("Indice satisfait : ", indice_satisfait(indice, etat))
    print("Segment formant une boucle unique : ", boucle_unique(etat, segment))
