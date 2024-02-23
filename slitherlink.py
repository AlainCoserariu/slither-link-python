###############################################################################
#                                   SlitherLink                               #
#                                 Alain Coserariu                             #
###############################################################################

import fltk
import solveur
import utilitaire as util
import menu


# ----------------------------Fonction d'affichage-----------------------------


def afficher_points_grille(indice, taille_case, marge):
    """
    Affiche chaque point de la grille

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param taille_case: Taille de chaque case
    :param marge: Marge au bord de l'écran qui permet de garder chaque éléments
    du jeu dans la fenêtre
    :return: Void
    """
    for y in range(len(indice) + 1):
        for x in range(len(indice[0]) + 1):
            fltk.cercle(x * taille_case + marge / 2,
                        y * taille_case + marge / 2,
                        3, "black", "black")


def afficher_indices(indice, taille_case, marge, etat):
    """
    Affiche les indices sur la grille.
    Affiche un indice en rouge s'il y a trop de segments autour
    Affiche un indice en noir s'il n'y a pas assez de segments autour
    Affiche un indice en vert s'il est satisfait

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param taille_case: Taille de chaque case
    :param marge: Marge au bord de l'écran qui permet de garder chaque éléments
    du jeu dans la fenêtre
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :return: Void
    """
    for y in range(len(indice)):
        for x in range(len(indice[0])):

            numero = indice[y][x]
            if numero is None:
                numero = ""
            else:
                numero = str(numero)

            if util.statut_case(indice, etat, (x, y)) == -1:
                fltk.texte(x * taille_case + taille_case / 2 + marge / 2,
                           y * taille_case + taille_case / 2 + marge / 2,
                           numero, "red", "center")
            elif util.statut_case(indice, etat, (x, y)) == 1:
                fltk.texte(x * taille_case + taille_case / 2 + marge / 2,
                           y * taille_case + taille_case / 2 + marge / 2,
                           numero, "black", "center")
            else:
                fltk.texte(x * taille_case + taille_case / 2 + marge / 2,
                           y * taille_case + taille_case / 2 + marge / 2,
                           numero, "green", "center")


def afficher_segment(etat, taille_case, marge):
    """
    Affiche chaque segment ou croix présent dans le dictionnaire etat

    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge (1: segment tracée / -1: croix)
    :param taille_case: Taille de chaque case
    :param marge: Marge au bord de l'écran qui permet de garder chaque éléments
    du jeu dans la fenêtre
    :return: Void
    """
    for segment in etat:
        if etat[segment] == 1:
            fltk.ligne(taille_case * segment[0][0] + marge / 2,
                       taille_case * segment[0][1] + marge / 2,
                       taille_case * segment[1][0] + marge / 2,
                       taille_case * segment[1][1] + marge / 2,
                       'black', 5)
        else:
            fltk.ligne((taille_case * segment[0][0] + marge / 2 + taille_case *
                        segment[1][0] + marge / 2) / 2 - 7,
                       (taille_case * segment[0][1] + marge / 2 + taille_case *
                        segment[1][1] + marge / 2) / 2 - 7,
                       (taille_case * segment[0][0] + marge / 2 + taille_case *
                        segment[1][0] + marge / 2) / 2 + 7,
                       (taille_case * segment[0][1] + marge / 2 + taille_case *
                        segment[1][1] + marge / 2) / 2 + 7,
                       'red', 5)
            fltk.ligne((taille_case * segment[0][0] + marge / 2 + taille_case *
                        segment[1][0] + marge / 2) / 2 + 7,
                       (taille_case * segment[0][1] + marge / 2 + taille_case *
                        segment[1][1] + marge / 2) / 2 - 7,
                       (taille_case * segment[0][0] + marge / 2 + taille_case *
                        segment[1][0] + marge / 2) / 2 - 7,
                       (taille_case * segment[0][1] + marge / 2 + taille_case *
                        segment[1][1] + marge / 2) / 2 + 7,
                       'red', 5)


def afficher(indice, taille_case, etat, marge):
    """
    Affiche chaque élément du jeu à chaque événement joueur (tel que le
    placement d'une croix ou celui d'un segment)

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param taille_case: Taille de chaque case
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param marge: Marge au bord de l'écran qui permet de garder chaque éléments
    du jeu dans la fenêtre
    :return: Void
    """
    fltk.efface_tout()

    afficher_points_grille(indice, taille_case, marge)
    afficher_segment(etat, taille_case, marge)
    afficher_indices(indice, taille_case, marge, etat)

    fltk.mise_a_jour()


# ------------------------Fonction relative a la grille------------------------


def placer_element(type_evenement, segment, indice, etat):
    """
    Met à jour le dictionnaire état après un clics de souris sur un segment

    :param type_evenement: Evenement fltk
    :param segment: couple de coordonnées entre deux sommets
    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :return:
    """
    if type_evenement == "ClicGauche":
        if segment in etat and etat[segment] == 1:
            del etat[segment]
        else:
            etat[segment] = 1
            util.affichage_victoire_console(
                indice, etat, util.element_dictionnaire(etat, 1))
    else:
        if segment in etat and etat[segment] == -1:
            del etat[segment]
        else:
            etat[segment] = -1


def detecter_clic(coordonnees_click, taille_case, etat, marge, clic, indice,
                  type_evenement):
    """
    Place un element (segment ou croix) dans le dictionnaire état

    :param coordonnees_click: Tuple : Coordonnées d'un click donnée par fltk
    :param taille_case: Taille de chaque case
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param marge: Marge au bord de l'écran qui permet de garder chaque éléments
    du jeu dans la fenêtre
    :param clic: str: 'droit' ou 'gauche' pour signaler si il faut placer un
    segment ou une croix
    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param type_evenement: Evenement fltk
    :return: Void
    """
    for y in range(len(indice) + 1):
        for x in range(len(indice[0]) + 1):

            # Largeur de détéction des clics proches des segments
            marge_inferieur_x = x - 5 / taille_case + marge / 2 / taille_case
            marge_superieur_x = x + 5 / taille_case + marge / 2 / taille_case

            marge_inferieur_y = y - 5 / taille_case + marge / 2 / taille_case
            marge_superieur_y = y + 5 / taille_case + marge / 2 / taille_case

            if marge_inferieur_x <= coordonnees_click[0] / taille_case <= \
                    marge_superieur_x and y + 5 / taille_case + marge / 2 / \
                    taille_case < coordonnees_click[1] / taille_case < \
                    y + 1 - 5 / taille_case + marge / 2 / taille_case:

                segment = util.ordonner_sommet(((x, y), (x, y + 1)))
                placer_element(type_evenement, segment, indice, etat)
            elif marge_inferieur_y <= coordonnees_click[1] / taille_case <= \
                    marge_superieur_y and \
                    x + 5 / taille_case + marge / 2 / taille_case < \
                    coordonnees_click[0] / taille_case < \
                    x + 1 - 5 / taille_case + marge / 2 / taille_case:

                segment = util.ordonner_sommet(((x, y), (x + 1, y)))
                placer_element(type_evenement, segment, indice, etat)


# ------------------------------Boucle principale------------------------------


def jeu(indice, etat):
    """
    Gère la boucle principale du jeu

    :return: Void
    """

    marge = 20  # Espace vide sur le bord de l'écrans pour bien afficher le jeu
    taille_case = 100
    print(indice)
    taille_fenetre_x = taille_case * len(indice[0]) + marge
    taille_fenetre_y = taille_case * len(indice) + marge
    while taille_fenetre_x > 950 or taille_fenetre_y > 950:
        taille_case -= 1
        taille_fenetre_x = taille_case * len(indice[0]) + marge
        taille_fenetre_y = taille_case * len(indice) + marge

    fltk.cree_fenetre(taille_fenetre_x, taille_fenetre_y)
    afficher(indice, taille_case, etat, marge)

    jeu = True
    while jeu:
        # Afficher la grille de jeu
        afficher(indice, taille_case, etat, marge)

        # detecter le click
        evenement = fltk.donne_ev()
        type_evenement = fltk.type_ev(evenement)

        if type_evenement == "ClicDroit" or type_evenement == "ClicGauche":
            coordonnees_click = (fltk.abscisse(evenement),
                                 fltk.ordonnee(evenement))
            # Placer/retirer le marqueur (segment ou interdit)
            detecter_clic(coordonnees_click, taille_case, etat, marge,
                          type_evenement, indice, type_evenement)

        elif type_evenement == 'Touche' and fltk.touche(evenement) == "s":
            solveur.executer_solveur(etat, indice, taille_case, marge, False,
                                     taille_fenetre_x, taille_fenetre_y)
        elif type_evenement == 'Touche' and fltk.touche(evenement) == "g":
            solveur.executer_solveur(etat, indice, taille_case, marge, True,
                                     taille_fenetre_x, taille_fenetre_y)
        elif type_evenement == 'Touche' and fltk.touche(evenement) == "e":
            etat = {}
        elif type_evenement == 'Touche' and fltk.touche(evenement) == "v":
            util.sauvegarder_grille(indice, etat)

        fltk.mise_a_jour()

        if type_evenement == 'Touche' and fltk.touche(evenement) == "m":
            jeu = False
            fltk.ferme_fenetre()

        # Gestion victoire
        if util.indice_satisfait(indice, etat) and util.boucle_unique(
                etat, util.element_dictionnaire(etat, 1)):
            afficher(indice, taille_case, etat, marge)
            fltk.attend_ev()
            fltk.rectangle(20, taille_fenetre_y // 3 - 25,
                           taille_fenetre_x - 20,
                           taille_fenetre_y // 3 + 25,
                           remplissage="white")
            fltk.texte(taille_fenetre_x // 2,
                       taille_fenetre_y // 3,
                       "La grille a été résolue !",
                       'green', 'center', taille=18)
            fltk.attend_ev()
            fltk.ferme_fenetre()
            jeu = False


if __name__ == '__main__':
    menu.menu()
