###############################################################################
#                                SlitherLink                                  #
#                              Alain Coserariu                                #
###############################################################################

import utilitaire
import fltk
import slitherlink


def afficher_resultat(taille_fenetre_x, taille_fenetre_y):
    """
    Affiche un texte à l'écran pour signaler si le solveur à trouver une
    solution ou non

    :param taille_fenetre_x: Largeur de la fenêtre de jeu
    :param taille_fenetre_y: Hauteur de la fenêtre de jeu
    :return: Void
    """
    fltk.rectangle(20, taille_fenetre_y // 3 - 25, taille_fenetre_x - 20,
                   taille_fenetre_y // 3 + 25,
                   remplissage="white")
    fltk.texte(taille_fenetre_x // 2, taille_fenetre_y // 3,
               "Il n'y a pas de solution depuis votre "
               "avancé", 'red', 'center', taille=18)
    fltk.attend_ev()


def placer_theorie(etat, sommet, liste_sommet, segment_courent):
    """
    Place un coup théorique dans etat avec les croix que cela implique

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param sommet: Sommet depuis lequel le solveur cherche la suite de la
    solution
    :param liste_sommet: Liste des sommets qui peuvent être pris pour continuer
    la recherche de solution
    :param segment_courent: Segment théorique sur lequel travail le solveur
    :return: void
    """
    etat[segment_courent] = 1
    for k in liste_sommet:
        if len(utilitaire.segments_traces(etat, sommet)) >= 2 and \
                utilitaire.ordonner_sommet((sommet, k)) not in etat \
                and utilitaire.ordonner_sommet((sommet, k)) != \
                segment_courent:
            etat[utilitaire.ordonner_sommet((sommet, k))] = -1


def sommet_adjacent(sommet, etat, indice):
    """
    Cherche les sommets adjacents utile à la recherche d'une solution depuis un
    sommet de départ

    :param sommet: couple de coordonnées représentent un point de la grille
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :return: List : Liste de tous les sommets adjacents utile à la recherche

    >>> etat = {}
    >>> indice = [\
    [None, 1], \
    [1, None]]
    >>> sommet_adjacent((1, 1), etat, indice)
    [(0, 1), (2, 1), (1, 0), (1, 2)]

    >>> etat = {((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1}
    >>> sommet_adjacent((1, 0), etat, indice)
    [(2, 0), (1, 1)]
    """
    liste_sommet_temporaire = [(sommet[0] - 1, sommet[1]),
                               (sommet[0] + 1, sommet[1]),
                               (sommet[0], sommet[1] - 1),
                               (sommet[0], sommet[1] + 1)]
    liste_sommet = []
    for sommet_liste_sommet in liste_sommet_temporaire:
        segment_temporaire = utilitaire.ordonner_sommet((sommet,
                                                         sommet_liste_sommet))
        if 0 <= sommet_liste_sommet[0] <= len(indice[0]) and \
                0 <= sommet_liste_sommet[1] <= len(indice) and \
                segment_temporaire not in etat:
            liste_sommet.append(sommet_liste_sommet)
    return liste_sommet


def effacer_segment(indice, etat):
    """
    Cherche si il faut effacer le segment théorique ou si il est valide

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :return: Bool: True si il faut effacer le segment
    """
    for y in range(len(indice)):
        for x in range(len(indice[0])):
            if utilitaire.statut_case(indice, etat, (x, y)) == -1:
                return True


def trouver_premier_sommet(indice, sommet_faux):
    """
    Trouve un premier sommet intéressant pour commencé à résoudre la grille.
    Par exemple un sommet autour d'un 3 est forcément intéressant cor
    obligatoirement relié à un segment qui fait partie de la solution.

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param sommet_faux: Liste des sommets qui ne font pas partie de la solution
    :return: sommet

    >>> indice = [\
    [None, None, None, None, None],\
    [2, 2, None, None, 3],\
    [2, 1, None, 0, 3],\
    [None, None, 2, 0, None],\
    [2, 2, 2, 2, None],\
    ]
    >>> trouver_premier_sommet(indice, [])
    (4, 1)
    """
    for i in range(3, 0, -1):
        for y in range(len(indice)):
            for x in range(len(indice[y])):
                if indice[y][x] == i:
                    liste_sommet_case = [(x, y),
                                         (x + 1, y),
                                         (x, y + 1),
                                         (x + 1, y + 1)]
                    for sommet in liste_sommet_case:
                        if sommet not in sommet_faux:
                            return sommet


def solveur(etat, indice, sommet, taille_case, marge, solveur_graphique):
    """
    Représente dans le dictionnaire état tous les segments "tracés" qui
    forment la solution.

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param sommet: couple de coordonnées représentent un point de la grille
    :param taille_case: Taille de chaque case
    :param marge: Marge au bord de l'écran qui permet de garder chaque éléments
    du jeu dans la fenêtre
    :param solveur_graphique: Bool : Affiche une recherche graphique ou non
    :return: Bool : True si il existe une solution
                    False si il n'y pas de solution

    >>> indice = [\
    [3, None],\
    [None, 3]]
    >>> solveur({}, indice, trouver_premier_sommet(indice, []), 0, 0, False)
    True
    """
    if solveur_graphique:
        slitherlink.afficher(indice, taille_case, etat, marge)

    segments_adjacent = utilitaire.segments_traces(etat, sommet)
    if len(segments_adjacent) > 2:
        return False

    elif len(segments_adjacent) == 2:
        return utilitaire.boucle_unique(etat, segments_adjacent[0]) and \
               utilitaire.indice_satisfait(indice, etat)

    elif len(segments_adjacent) < 2:
        liste_sommet = sommet_adjacent(sommet, etat, indice)

        for sommet_deux in liste_sommet:
            segment_courent = utilitaire.ordonner_sommet((sommet, sommet_deux))

            placer_theorie(etat, sommet, liste_sommet, segment_courent)

            if not effacer_segment(indice, etat) and \
                    solveur(etat, indice, sommet_deux, taille_case, marge,
                            solveur_graphique):
                return True
            else:
                for k in liste_sommet:
                    if utilitaire.ordonner_sommet((sommet, k)) in etat:
                        del etat[utilitaire.ordonner_sommet((sommet, k))]

    return False


def executer_solveur(etat, indice, taille_case, marge, solveur_graphique,
                     taille_fenetre_x, taille_fenetre_y):
    """
    Execute le solveur dans la boulce principale du jeu

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param taille_case: Taille de chaque case
    :param marge: Marge au bord de l'écran qui permet de garder chaque éléments
    du jeu dans la fenêtre
    :param solveur_graphique: Bool : Affiche une recherche graphique ou non
    :param taille_fenetre_x: Largeur de la fenêtre de jeu
    :param taille_fenetre_y: Hauteur de la fenêtre de jeu
    :return: None : si il n'y a pas de solution à la grille
    """
    solution = False
    sommet_faux = []
    while not solution:
        premier_sommet = None

        # Si la grille est commancé :
        if utilitaire.compteur_segments_etat(etat) > 0:

            for segment in etat:
                if etat[segment] == 1:
                    if len(utilitaire.segments_traces(etat, segment[0])) < 2:
                        premier_sommet = segment[0]
                    elif len(utilitaire.segments_traces(etat, segment[1])) < 2:
                        premier_sommet = segment[1]
            if premier_sommet is None:
                afficher_resultat(taille_fenetre_x, taille_fenetre_y)
                return None

        else:
            premier_sommet = trouver_premier_sommet(indice, sommet_faux)

        solution = solveur(etat, indice, premier_sommet, taille_case,
                           marge, solveur_graphique)
        if not solution:
            if utilitaire.compteur_segments_etat(etat) > 0 or \
                    len(sommet_faux) == \
                    utilitaire.compteur_segments_etat(etat):
                afficher_resultat(taille_fenetre_x, taille_fenetre_y)
                return None

            sommet_faux.append(premier_sommet)

        else:
            solution = True
