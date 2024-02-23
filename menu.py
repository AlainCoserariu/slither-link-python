###############################################################################
#                                 SlitherLink                                 #
#                               Alain Coserariu                               #
###############################################################################

import fltk
import slitherlink
import utilitaire as util


# -----------------------------------Menu---------------------------------------


def lancer_jeu(indice, etat, largeur_fenetre, hauteur_fenetre):
    """
    Lance le jeu ou affiche un message d'erreur liée à la lecture d'un fichier

    :param indice: tableau d'indice allant de 0 à trois ou ne donnant pas de
    renseignement
    :param etat: dictionnaire comportant l'information de chaque segments non
    vierge
    :param largeur_fenetre: Largeur de la fenêtre
    :param hauteur_fenetre: Hauteur de la fenêtre
    :return: Bool, Bool: représente dans quelle menu on doit se situer
    """
    if indice is not None:
        menu = True
        menu2 = False
        fltk.ferme_fenetre()
        slitherlink.jeu(indice, etat)
        fltk.cree_fenetre(largeur_fenetre, hauteur_fenetre)
        return menu, menu2
    else:
        fltk.rectangle(20, 665 // 5 - 20, 600 - 20,
                       665 // 5 + 20, remplissage="white")
        fltk.texte(600 // 2, 665 // 5,
                   "Cette grille n'est pas conforme !",
                   'red', taille=15, ancrage='center')
        fltk.attend_ev()
        menu = True
        menu2 = False
        return menu, menu2


def dessine_bouton(x: int, y: int, contenu: str, ancrage: str = 'nw',
                   couleur: str = 'white', taille: int = 24,
                   largeur: str = None):
    """
    Dessine un bouton aux coordonnées renseignées.

    :param x: Abscisse du point d'ancrage.
    :param y: Ordonnée du point d'ancrage.
    :param contenu: Texte à insérer dans le bouton.
    :param ancrage: Ancrage du bouton.
    :param couleur: Couleur de remplissage du bouton.
    :param taille: Taille du texte.
    :param largeur: Chaîne de caractère déterminant la largeur du bouton.
    :return tuple: Coordonées du bouton.
    """
    if largeur is None:
        largeur = contenu  # contenue = texte
    longueur, hauteur = fltk.taille_texte(largeur, taille=taille)
    hauteur -= hauteur % 5

    fltk.rectangle(x - (longueur + 2 * 5) // 2,
                   y - (hauteur + 2 * 5) // 2,
                   x + (longueur + 2 * 5) // 2,
                   y + (hauteur + 2 * 5) // 2,
                   remplissage=couleur)
    fltk.texte(x, y, contenu, ancrage='center', taille=taille)
    return x - (longueur + 2 * 5) // 2, y - (hauteur + 2 * 5) // 2, x + (
            longueur + 2 * 5) // 2, y + (hauteur + 2 * 5) // 2


def dessine_menu(reglesMenu: dict, bouttons_menu_un: dict, largeur_fenetre,
                 hauteur_fenetre):
    """
    Dessine le menu principal et modifie les variables de jeu.
    :param bouttons_menu_un:
    :param dict reglesMenu: Variables de jeu.
    :param largeur_fenetre: largeur de la fenêtre
    :param hauteur_fenetre: Hauteut de la fenêtre
    """
    fltk.efface_tout()

    fltk.image(0, 0, "images/fond_menu.png", ancrage='nw')
    fltk.texte(largeur_fenetre // 2, 4,
               "Slitherlink",
               taille=30, couleur="white", ancrage='n')

    bouttons_menu_un["jouer"] = \
        dessine_bouton(largeur_fenetre // 2, 225,
                       "Jouer", ancrage='center',
                       largeur="Afficher les coups disponibles")
    bouttons_menu_un["charger_partie"] = \
        dessine_bouton(largeur_fenetre // 2, 300,
                       "Charger une partie", ancrage='center',
                       largeur="Afficher les coups disponibles")
    bouttons_menu_un["quitter"] = \
        dessine_bouton(largeur_fenetre // 2, 450,
                       "Quitter", ancrage='center')


def gestion_menu2(bouttons_menu_deux, largeur_fenetre, hauteur_fenetre):
    """
    Gére le deuxième menu

    :param bouttons_menu_deux: Dictionnaire contenant les coordonnées de chaque
    sommets de chaque bouttons du deuxième menu
    :param largeur_fenetre: Largeur de la fenetre
    :param hauteur_fenetre: Hauteur de la fenetre
    :return: Bool, Bool : Servent à determiner quelle menu afficher
    """
    x, y = fltk.attend_clic_gauche()

    for boutton in bouttons_menu_deux:
        if int(bouttons_menu_deux[boutton][0]) <= x <= \
                int(bouttons_menu_deux[boutton][2]) and \
                int(bouttons_menu_deux[boutton][1]) <= y \
                <= int(bouttons_menu_deux[boutton][3]):
            # Vérification des coordonnées de clics dans un boutton
            if boutton == "grille1":
                indice, p = util.charger_grille('grille5x5.txt')
                return lancer_jeu(indice, {}, largeur_fenetre,
                                  hauteur_fenetre)
            elif boutton == "grille2":
                indice, p = util.charger_grille('grille7x7.txt')
                return lancer_jeu(indice, {}, largeur_fenetre,
                                  hauteur_fenetre)
            elif boutton == "grille3":
                indice, p = util.charger_grille('grille10x10.txt')
                return lancer_jeu(indice, {}, largeur_fenetre,
                                  hauteur_fenetre)
            elif boutton == "grille4":
                indice, p = util.charger_grille('grille15x15.txt')
                return lancer_jeu(indice, {}, largeur_fenetre,
                                  hauteur_fenetre)
            elif boutton == "precedent":
                return True, False


def dessine_menu_2(reglesMenu2: dict, bouttons: dict, largeur_fenetre,
                   hauteur_fenetre, bouttons_menu_deux):
    fltk.efface_tout()

    fltk.image(0, 0, "images/fond_menu.png", ancrage='nw')
    fltk.texte(largeur_fenetre // 2, 4,
               "Slitherlink",
               taille=30, couleur="white", ancrage='n')

    bouttons_menu_deux["grille1"] = \
        dessine_bouton(largeur_fenetre // 2, 225,
                       "Grille 5x5", ancrage='center')
    bouttons_menu_deux["grille2"] = \
        dessine_bouton(largeur_fenetre // 2, 300,
                       "Grille 7x7", ancrage='center')
    bouttons_menu_deux["grille3"] = \
        dessine_bouton(largeur_fenetre // 2, 375,
                       "Grille 10x10", ancrage='center')
    bouttons_menu_deux["grille4"] = \
        dessine_bouton(largeur_fenetre // 2, 450,
                       "Grille 15x15", ancrage='center')
    bouttons_menu_deux["precedent"] = \
        dessine_bouton(largeur_fenetre // 2, 525, "Precedent",
                       ancrage='center')


def menu():
    """
    Gére le menu

    :return: Void
    """
    bouttons_menu_un = {}
    bouttons_menu_deux = {}

    reglesMenu = {'jouer': True,
                  'sauvegarde': None}  # Indicateur sur le premier menu

    reglesMenu2 = {'jouer': True}  # Indicateurs sur le second menu

    largeur_fenetre = 600
    hauteur_fenetre = 665

    fltk.cree_fenetre(largeur_fenetre, hauteur_fenetre)

    menu = True
    menu2 = False
    while menu:
        dessine_menu(reglesMenu, bouttons_menu_un, largeur_fenetre,
                     hauteur_fenetre)
        x, y = fltk.attend_clic_gauche()

        for boutton in bouttons_menu_un:
            if int(bouttons_menu_un[boutton][0]) <= x <= \
                    int(bouttons_menu_un[boutton][2]) and \
                    int(bouttons_menu_un[boutton][1]) <= y <= \
                    int(bouttons_menu_un[boutton][3]):
                # Vérification des coordonnées de clics dans un boutton
                if boutton == "jouer":
                    menu = False
                    menu2 = True
                elif boutton == "charger_partie":
                    indice, etat = util.charger_grille('sauvegarde.txt')
                    menu, menu2 = lancer_jeu(indice, etat, largeur_fenetre,
                                             hauteur_fenetre)

                elif boutton == "quitter":
                    menu = False
                    menu2 = False
                    fltk.ferme_fenetre()

        while menu2:
            dessine_menu_2(reglesMenu2, bouttons_menu_deux, largeur_fenetre,
                           hauteur_fenetre, bouttons_menu_deux)
            menu, menu2 = gestion_menu2(bouttons_menu_deux, largeur_fenetre,
                                        hauteur_fenetre)
