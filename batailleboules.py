# La Bataille des Boules --- Version 3.5
# COUTELLIER Loélia, HOUANGKEO Émeline, CONSANI Maryam

# ==========================Imports==========================
from time import sleep, time
from random import randint
from math import sqrt
from upemtk import *
import os
import json
from datetime import datetime

# ==========================Variables globales==========================
# Taille de la fenêtre
largeur = 1200
hauteur = 800

# Taille de l'aire de jeu
largeur_aire = 800
hauteur_aire = 800

# Variantes
var_sab = False
var_sco = False
var_tai = False
var_dyn = False
var_ter = False
var_obs = False
liste_variantes = [var_sab, var_sco, var_tai, var_dyn, var_ter, var_obs]

# Couleurs
lst_couleurs = ['salmon', 'tan1', 'khaki', 'MediumPurple1',
                'SkyBlue2', 'PaleGreen1']  # liste des couleurs disponibles
lst_couleurs_joueurs = []  # liste des couleurs des joueurs

# Jeu
nb_tour = 30  # nombre de tours à jouer
rayon = 100  # rayon des boules de base
budget = 400  # budget de départ
liste_obstacles = []  # liste des obstacles
lst_coord_tour_joueur = [((largeur * (1025 / 1200)), (hauteur * (150 / 800))), ((largeur * (
    1100 / 1200)), (hauteur * (150 / 800)))]  # Coordonnees pour affichage du tour des joueurs
joueur_actif = ['J1', 'J2']  # Affichage du tour des joueurs
# Coordonnees pour affichage du nombre de tours restants
coord_nb_tour = ((largeur * (1100 / 1200)), (hauteur * (550 / 800)))
dico_valeurs = dict()  # dictionnaire des valeurs de configuration

# Chargement de partie
charger = False  # Variable pour savoir si on charge une partie
dico_chargement = dict()  # dictionnaire des données chargées
nom_save = ''  # nom du fichier de sauvegarde

# Taille police
big_chungus = int((largeur * hauteur) * (40 / (1200 * 800)))
loelia = int((largeur * hauteur) * (35 / (1200 * 800)))
bbb = int((largeur * hauteur) * (30 / (1200 * 800)))
bigbig = int((largeur * hauteur) * (28 / (1200 * 800)))
defaut = int((largeur * hauteur) * (24 / (1200 * 800)))
very_big = int((largeur * hauteur) * (20 / (1200 * 800)))
big = int((largeur * hauteur) * (18 / (1200 * 800)))
biggie = int((largeur * hauteur) * (16 / (1200 * 800)))
mid = int((largeur * hauteur) * (15 / (1200 * 800)))
titi = int((largeur * hauteur) * (13 / (1200 * 800)))
smoll = int((largeur * hauteur) * (12 / (1200 * 800)))

# Vérifier si les paramètres sont bons
si_para = 0

# Vérifier si terminaison a déjà été enclenché
si_ter = 0

# Incrément de la variante dynamique
increment = 5

# Temps pour chaque tour de la variante sablier
temps_tour = 5


# ==========================Fonctions==========================
# RECUPERATION DES PARAMETRES DE CONFIGURATION
def recuperation_parametres():
    """Renvoie un dictionnaire contenant les paramètres de configuration"""
    global dico_valeurs
    with open(os.path.join(os.path.dirname(__file__), 'configuration.txt'), 'r') as config:
        lignes = [next(config)[:-1] for _ in range(9)]
        dico_valeurs = {ligne.split('=')[0]: int(
            ligne.split('=')[1]) for ligne in lignes}


def affectation_parametres():
    """Affecte les paramètres de configuration aux variables globales
    Appelle erreur_parametres()"""
    global largeur
    global hauteur
    global largeur_aire
    global hauteur_aire
    global nb_tour
    global rayon
    global budget
    global lst_coord_tour_joueur
    global coord_nb_tour
    global increment
    global temps_tour
    largeur = dico_valeurs['largeur']
    hauteur = dico_valeurs['hauteur']
    largeur_aire = dico_valeurs['largeur_aire']
    hauteur_aire = dico_valeurs['hauteur_aire']
    nb_tour = dico_valeurs['nb_tour']
    rayon = dico_valeurs['rayon']
    budget = dico_valeurs['budget']
    increment = dico_valeurs['increment']
    temps_tour = dico_valeurs['temps_tour']
    lst_coord_tour_joueur = [((largeur * (1025 / 1200)), (hauteur * (150 / 800))),
                             ((largeur * (1100 / 1200)), (hauteur * (150 / 800)))]
    coord_nb_tour = ((largeur * (1100 / 1200)), (hauteur * (550 / 800)))
    erreur_parametres()


def erreur_parametres():
    """Vérifie que les paramètres de configuration sont corrects
    Appelle interface_parametres() si un problème est détecté"""
    lst_problemes = []
    if largeur_aire > (2 / 3) * largeur:
        lst_problemes.append('Aire trop large par rapport à la fenêtre')
    if hauteur_aire > hauteur:
        lst_problemes.append('Aire trop haute par rapport à la fenêtre')
    if largeur_aire < rayon * 2:
        lst_problemes.append('Aire trop petite par rapport au rayon')
    if hauteur_aire < rayon * 2:
        lst_problemes.append('Aire trop petite par rapport au rayon')
    if rayon < 1:
        lst_problemes.append('Le rayon ne peut pas être inférieur à 1')
    if nb_tour < 1:
        lst_problemes.append(
            'Le nombre de tours ne peut pas être inférieur à 1')
    if budget < 1:
        lst_problemes.append('Le budget ne peut pas être inférieur à 1')
    if nb_tour % 2 == 1:
        lst_problemes.append('Le nombre de tours doit être pair')
    if temps_tour < 1:
        lst_problemes.append(
            'Le temps pour un tour ne peut pas être inférieur à 1')

    if len(lst_problemes) > 0:
        interface_parametres(lst_problemes)


def interface_parametres(lst_problemes):
    """Affiche une interface d'erreur si les paramètres de configuration sont incorrects
    Prend en paramètre une liste contenant les raisons de l'erreur"""
    global si_para
    si_para = 1
    cree_fenetre(800, 800)
    affiche = '\n'.join(lst_problemes)
    rectangle(0, 0, 800, 800, remplissage="grey25")
    texte(400, 200, "Le jeu n'a pas pu être lancé...", police="Arial",
          taille=very_big, couleur="Antique White", ancrage='center')
    texte(400, 250, "Veuillez choisir de nouveaux paramètres !", police="Arial",
          taille=very_big, couleur="Antique White", ancrage='center')
    texte(400, 300, "Raisons : ", police="Arial", taille=very_big,
          couleur="Antique White", ancrage='center')
    texte(400, 400, str(affiche), ancrage='center',
          police="Arial", taille=very_big, couleur='Antique White')
    mise_a_jour()
    sleep(8)
    ferme_fenetre()


# MENU PRINCIPAL
def affichage_menu_principal():
    """Affiche une partie du menu principal
    Renvoie la liste des cases à cocher (sous forme de rectangles) pour les variantes"""
    rectangle(0, 0, largeur, hauteur, remplissage='grey25', tag='menu')

    texte(largeur / 2, (hauteur * (50 / 800)), "Bienvenue dans la", ancrage='center',
          tag='menu', police="Arial", taille=very_big, couleur='AntiqueWhite')

    ligne(0, (hauteur * (90 / 800)), largeur,
          (hauteur * (90 / 800)), tag='menu')
    texte(largeur / 2, (hauteur * (125 / 800)), "Bataille des Boules", taille=big_chungus,
          ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')
    ligne(0, (hauteur * (160 / 800)), largeur,
          (hauteur * (160 / 800)), tag='menu')

    # Définit le rayon et les coordonnées des 5 boules de chaque côté du nom du jeu
    r = (largeur * (30 / 1200))
    y = (hauteur * (125 / 800))
    x = (largeur * (10 / 1200)) + r

    # Boules à gauche du nom du jeu dont les couleurs sont alternées en fonction de leur position
    for i in range(5):
        if i % 2 == 0:
            cercle(x, y, r, remplissage="SkyBlue3", tag='menu')
        else:
            cercle(x, y, r, remplissage="salmon", tag='menu')
        x += 2 * r

    # Boules à droite du nom du jeu dont les couleurs sont alternées en fonction de leur position
    x = largeur - ((largeur * (10 / 1200)) + r)
    for i in range(5):
        if i % 2 == 0:
            cercle(x, y, r, remplissage="salmon", tag='menu')
        else:
            cercle(x, y, r, remplissage="SkyBlue3", tag='menu')
        x -= 2 * r

    # Définition des règles du jeu
    texte((largeur * (30 / 1200)), (hauteur * (200 / 800)), "Règles du jeu : ",
          taille=big, ancrage='w', tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (200 / 800)),
          "Chaque utilisateur joue avec une couleur. Le but du jeu est d'occuper la plus grande aire",
          taille=mid, ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (220 / 800)),
          "coloriée avec sa couleur. Les joueurs contrôlent la souris chacun à leur tour, pour un",
          taille=mid, ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (240 / 800)),
          "nombre de " +
          str(nb_tour // 2) +
          " tours chacun. Les intérieurs de deux boules de couleurs différentes ne",
          taille=mid, ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (260 / 800)),
          "peuvent pas s'intersecter. Si un joueur clique dans l'intérieur d'une boule de l'adversaire,",
          taille=mid, ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (280 / 800)), "il la transforme en deux boules de même couleur plus petites.",
          taille=mid, ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (320 / 800)),
          "Pour changer les paramètres de jeu, modifiez le fichier configuration.txt",
          taille=smoll, ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')

    # Création du bouton permettant de jouer au jeu
    rectangle((largeur * (200 / 1200)), (hauteur * (350 / 800)), (largeur * (400 / 1200)),
              (hauteur * (450 / 800)), tag='menu', couleur='black', remplissage='PaleGreen3')
    texte(largeur / 4, hauteur / 2, "JOUER", ancrage='center', tag='menu',
          police="Arial", taille=very_big, couleur='black')

    # Création du bouton permettant de charger une sauvegarde
    rectangle((largeur * (500 / 1200)), (hauteur * (350 / 800)), (largeur * (700 / 1200)),
              (hauteur * (450 / 800)), tag='menu', couleur='black', remplissage='sky blue')
    texte(largeur / 2, hauteur / 2, "CHARGER", ancrage='center',
          tag='menu', police="Arial", taille=very_big, couleur='black')

    # Création du bouton permettant de quitter le jeu/la fenêtre
    rectangle((largeur * (800 / 1200)), (hauteur * (350 / 800)), (largeur * (1000 / 1200)),
              (hauteur * (450 / 800)), tag='menu', couleur='black', remplissage='salmon')
    texte((largeur * (900 / 1200)), hauteur / 2, "QUITTER", ancrage='center',
          tag='menu', police="Arial", taille=very_big, couleur='black')

    # Affichage du menu "variantes" au centre de la fenêtre
    ligne((largeur * (30 / 1200)), (hauteur * (495 / 800)), (largeur * (430 / 1200)),
          (hauteur * (495 / 800)), epaisseur=2, tag='menu')
    ligne((largeur * (30 / 1200)), (hauteur * (498 / 800)), (largeur * (430 / 1200)),
          (hauteur * (498 / 800)), epaisseur=2, tag='menu')
    texte(largeur / 2, (hauteur * (490 / 800)), "VARIANTES", taille=bigbig,
          ancrage='center', tag='menu', police="Arial", couleur='AntiqueWhite')
    ligne((largeur * (770 / 1200)), (hauteur * (495 / 800)),
          (largeur * (1170 / 1200)), (hauteur * (495 / 800)), epaisseur=2, tag='menu')
    ligne((largeur * (770 / 1200)), (hauteur * (498 / 800)),
          (largeur * (1170 / 1200)), (hauteur * (498 / 800)), epaisseur=2, tag='menu')

    # Définition de la variante "Sablier", de ses règles ainsi que de son paramètre de sélection pour pouvoir jouer avec
    recsab = rectangle((largeur * (30 / 1200)), (hauteur * (530 / 800)), (largeur *
                                                                          (70 / 1200)), (hauteur * (570 / 800)),
                       tag='menu', remplissage='salmon')
    texte((largeur * (100 / 1200)), (hauteur * (550 / 800)), "SABLIER", ancrage='w',
          tag='menu', police="Arial", couleur='AntiqueWhite', taille=defaut)
    texte((largeur * (200 / 1200)), (hauteur * (590 / 800)),
          "Chaque joueur a " + str(temps_tour) + "s pour jouer à chaque",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte((largeur * (200 / 1200)), (hauteur * (605 / 800)), "tour ; s'il ne réagit pas à temps, il perd son tour.",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')

    # Définition de la variante "Scores", de ses règles ainsi que de son paramètre de sélection pour pouvoir jouer avec
    recsco = rectangle((largeur * (430 / 1200)), (hauteur * (530 / 800)), (largeur *
                                                                           (470 / 1200)), (hauteur * (570 / 800)),
                       tag='menu', remplissage='salmon')
    texte((largeur * (500 / 1200)), (hauteur * (550 / 800)), "SCORES", ancrage='w',
          tag='menu', police="Arial", couleur='AntiqueWhite', taille=defaut)
    texte(largeur / 2, (hauteur * (590 / 800)), "Un joueur peut vérifier quelle aire ses boules totalisent",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (605 / 800)), "à chaque instant en appuyant sur la touche 's'.",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')

    # Définition de la variante "Taille Boules", de ses règles ainsi que de son paramètre de sélection pour pouvoir jouer avec
    rectai = rectangle((largeur * (830 / 1200)), (hauteur * (530 / 800)), (largeur *
                                                                           (870 / 1200)), (hauteur * (570 / 800)),
                       tag='menu', remplissage='salmon')
    texte((largeur * (900 / 1200)), (hauteur * (550 / 800)), "TAILLE BOULES", ancrage='w',
          tag='menu', police="Arial", couleur='AntiqueWhite', taille=defaut)
    texte((largeur * (1000 / 1200)), (hauteur * (590 / 800)),
          "À chaque tour, le joueur choisi le rayon de la boule qu'il",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte((largeur * (1000 / 1200)), (hauteur * (605 / 800)),
          "veut introduire. Il commence avec un certain budget fixé",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte((largeur * (1000 / 1200)), (hauteur * (620 / 800)),
          "à " + str(budget) + ", et pour chaque boule posée, son budget",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte((largeur * (1000 / 1200)), (hauteur * (635 / 800)), "diminue du rayon de la boule qu'il pose.",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')

    # Définition de la variante "Dynamique", de ses règles ainsi que de son paramètre de sélection pour pouvoir jouer avec
    recdyn = rectangle((largeur * (30 / 1200)), (hauteur * (660 / 800)), (largeur *
                                                                          (70 / 1200)), (hauteur * (700 / 800)),
                       tag='menu', remplissage='salmon')
    texte((largeur * (100 / 1200)), (hauteur * (680 / 800)), "DYNAMIQUE", ancrage='w',
          tag='menu', police="Arial", couleur='AntiqueWhite', taille=defaut)
    texte(largeur / 6, (hauteur * (720 / 800)), "Les rayons de toutes les boules s'incrémentent de",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 6, (hauteur * (735 / 800)), str(increment) + "px à chaque tour en respectant les règles",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 6, (hauteur * (750 / 800)), "données (dès que deux boules de couleurs",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 6, (hauteur * (765 / 800)), "différentes se touchent, elles arrêtent de grandir).",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')

    # Définition de la variante "Terminaison" du jeu ainsi que le paramètre de sélection permettant de jouer avec la variante
    recter = rectangle((largeur * (430 / 1200)), (hauteur * (660 / 800)), (largeur *
                                                                           (470 / 1200)), (hauteur * (700 / 800)),
                       tag='menu', remplissage='salmon')
    texte((largeur * (500 / 1200)), (hauteur * (680 / 800)), "TERMINAISON", ancrage='w',
          tag='menu', police="Arial", couleur='AntiqueWhite', taille=defaut)
    texte(largeur / 2, (hauteur * (720 / 800)), "Permet à un joueur de décider une fois par partie",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (735 / 800)), "que le jeu se termine dans 5 tours chacun.",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (750 / 800)), "en appuyant sur la touche 't'",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')

    # Définition de la variante "Obstacles" du jeu ainsi que le paramètre de sélection permettant de jouer avec la variante
    recobs = rectangle((largeur * (830 / 1200)), (hauteur * (660 / 800)), (largeur *
                                                                           (870 / 1200)), (hauteur * (700 / 800)),
                       tag='menu', remplissage='salmon')
    texte((largeur * (900 / 1200)), (hauteur * (680 / 800)), "OBSTACLES", ancrage='w',
          tag='menu', police="Arial", couleur='AntiqueWhite', taille=defaut)
    texte((largeur * (1000 / 1200)), (hauteur * (720 / 800)), "Le tableau commence avec certains obstacles que",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')
    texte((largeur * (1000 / 1200)), (hauteur * (735 / 800)), "les boules ne peuvent pas toucher",
          ancrage='center', taille=smoll, tag='menu', police="Arial", couleur='AntiqueWhite')

    return [recsab, recsco, rectai, recdyn, recter, recobs]


def changement_variante(variante, rectangle_variante, x1, y1, x2, y2):
    """Fonction permettant de changer la couleur du rectangle de sélection de la variante si un joueur la sélectionne ou la désélectionne
    Prend en paramètres la variante sélectionnée, le rectangle de sélection de la variante, les coordonnées du rectangle de sélection de la variante tels x1, y1, x2, y2
    Renvoie la variante sous la forme d'un booléen définissant la variante sélectionnée : True si la variante est sélectionnée, False sinon"""
    efface(rectangle_variante)
    if variante == True:
        variante = False
        rectangle_variante = rectangle(
            x1, y1, x2, y2, tag='menu', remplissage='salmon')
    else:
        variante = True
        rectangle_variante = rectangle(
            x1, y1, x2, y2, tag='menu', remplissage='PaleGreen1')
    return variante


def clique_charger():
    """Fonction permettant de vérifier s'il y a des sauvegardes et de charger la partie si c'est le cas, sinon d'afficher un message d'erreur"""
    global charger
    efface('menu')
    liste_sauvegardes = liste_saves()
    if len(liste_sauvegardes) != 0:
        affichage_saves(liste_sauvegardes)
        chargement_partie()
        charger = True
        verifier_taille_aire_de_jeu()
    else:
        rectangle(0, 0, largeur, hauteur, remplissage='grey25',
                  tag='demandesauvegarde')
        rectangle((largeur*(400/1200)), hauteur/3, (largeur*(800/1200)),
                  (hauteur*(533/800)), remplissage='white smoke', tag='demandesauvegarde')
        texte((largeur*(600/1200)), (hauteur*(350/800)), "Aucune sauvegarde",
              taille=biggie, ancrage='center', tag='demandesauvegarde', police="Arial")
        texte((largeur*(600/1200)), (hauteur*(380/800)), "à charger ...",
              taille=biggie, ancrage='center', tag='demandesauvegarde', police="Arial")
        texte((largeur*(600/1200)), (hauteur*(500/800)), "Appuyez sur une touche ou",
              taille=smoll, ancrage='center', tag='demandesauvegarde', police="Arial")
        texte((largeur*(600/1200)), (hauteur*(520/800)), "cliquez pour revenir au menu",
              taille=smoll, ancrage='center', tag='demandesauvegarde', police="Arial")
        attente_clic_ou_touche()
        efface_tout()
        menu_principal()


def verifier_taille_aire_de_jeu():
    """Fonction permettant de vérifier si la taille de l'aire de jeu de la sauvegarde est compatible avec celle actuelle
    Si ce n'est pas le cas, affiche un message d'erreur et on réouvre le jeu au bon format"""
    global largeur
    global hauteur
    global largeur_aire
    global hauteur_aire
    global liste_variantes
    lst_problemes = []
    if dico_chargement['largeur_aire'] != largeur_aire:
        lst_problemes.append('Largeur de l\'aire différente de la sauvegarde')
    if dico_chargement['hauteur_aire'] != hauteur_aire:
        lst_problemes.append('Hauteur de l\'aire différente de la sauvegarde')
    if dico_chargement['largeur_aire'] > (2 / 3) * largeur:
        lst_problemes.append('Aire trop large par rapport à la fenêtre')
    if dico_chargement['hauteur_aire'] > hauteur:
        lst_problemes.append('Aire trop haute par rapport à la fenêtre')
    if len(lst_problemes) > 0:
        affiche = '\n'.join(lst_problemes)
        efface_tout()
        rectangle(0, 0, largeur, hauteur, remplissage="grey25")
        texte(largeur / 2, (hauteur * (200 / 800)), "Le jeu n'a pas pu être lancé...",
              police="Arial", taille=very_big, couleur="Antique White", ancrage='center')
        texte(largeur / 2, (hauteur * (250 / 800)), "Nous allons réouvrir le jeu",
              police="Arial", taille=very_big, couleur="Antique White", ancrage='center')
        texte(largeur / 2, (hauteur * (300 / 800)), "Raisons : ", police="Arial",
              taille=very_big, couleur="Antique White", ancrage='center')
        texte(largeur / 2, (hauteur * (400 / 800)), str(affiche), ancrage='center',
              police="Arial", taille=very_big, couleur='Antique White')
        mise_a_jour()
        sleep(5)
        ferme_fenetre()
        cree_fenetre(dico_chargement['largeur'], dico_chargement['hauteur'])
        largeur = dico_chargement['largeur']
        hauteur = dico_chargement['hauteur']
        largeur_aire = dico_chargement['largeur_aire']
        hauteur_aire = dico_chargement['hauteur_aire']
    liste_variantes = dico_chargement['liste_variantes']
    jouer()


def dico_transition_global():
    """Affectation des variables globales à partir du dictionnaire de chargement"""
    global nb_tour
    global rayon
    global lst_couleurs_joueurs
    global liste_obstacles
    global lst_coord_tour_joueur
    global coord_nb_tour
    global si_ter
    global increment
    global temps_tour
    nb_tour = dico_chargement['nb_tour']
    rayon = dico_chargement['rayon']
    lst_couleurs_joueurs = dico_chargement['lst_couleurs_joueurs']
    liste_obstacles = dico_chargement['liste_obstacles']
    si_ter = dico_chargement['si_ter']
    increment = dico_chargement['increment']
    temps_tour = dico_chargement['temps_tour']
    lst_coord_tour_joueur = [((largeur * (1025 / 1200)), (hauteur * (150 / 800))),
                             ((largeur * (1100 / 1200)), (hauteur * (150 / 800)))]
    coord_nb_tour = ((largeur * (1100 / 1200)), (hauteur * (550 / 800)))


def chargement_boules(joueur):
    """Fonction permettant de charger les boules du joueur à partir du dictionnaire de chargement
    Prend en paramètre le joueur dont on veut charger les boules
    Renvoie la liste des boules"""
    lst_boules = []
    if charger == True:
        if joueur == 'J1':
            for element in dico_chargement['lst_J1']:
                lst_boules.append(cercle(
                    element[0], element[1], element[2], remplissage=element[3], tag=element[4]))
        elif joueur == 'J2':
            for element in dico_chargement['lst_J2']:
                lst_boules.append(cercle(
                    element[0], element[1], element[2], remplissage=element[3], tag=element[4]))
    return lst_boules


def choix_variantes(x, liste_carres_variantes):
    """Fonction permettant de choisir les variantes du jeu et de changer la couleur des carrés de sélection des variantes
    Prend en paramètres les coordonnées du clic de l'utilisateur, la liste des carrés de sélection des variantes"""
    global liste_variantes
    global var_sab
    global var_sco
    global var_tai
    global var_dyn
    global var_ter
    global var_obs
    # si l'utilisateur clique sur jouer
    if x[0] >= ((largeur * (200 / 1200))) and x[0] <= ((largeur * (400 / 1200))) and x[1] >= (
            (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800))):
        efface('menu')
        jouer()

    elif x[0] >= ((largeur * (500 / 1200))) and x[0] <= ((largeur * (700 / 1200))) and x[1] >= (
            (hauteur * (350 / 800))) and x[1] <= (hauteur * (450 / 800)):
        clique_charger()

    # Change la couleur du carré de sélection de chaque variante lorsque l'utilisateur clique dessus
    # (se transforme en vert si il est rouge à l'origine et en rouge si il est vert à l'origine ou si l'utilisateur a déjà cliqué dessus.
    # change la valeur de la variable correspondant à la variante en fonction de la couleur du carré de sélection
    else:
        while ((not (x[0] >= (largeur * (200 / 1200)) and x[0] <= (largeur * (400 / 1200)) and x[1] >= (
                hauteur * (350 / 800)) and x[1] <= (hauteur * (450 / 800)))) or (not (
                x[0] >= (largeur * (500 / 1200)) and x[0] <= (largeur * (700 / 1200)) and x[1] >= (
                hauteur * (350 / 800)) and x[1] <= (hauteur * (450 / 800))))):
            # Changement pour la variante Sablier
            if x[0] >= (largeur * (30 / 1200)) and x[0] <= (largeur * (70 / 1200)) and x[1] >= (
                    hauteur * (530 / 800)) and x[1] <= (hauteur * (570 / 800)):
                var_sab = changement_variante(var_sab, liste_carres_variantes[0], (largeur * (
                    30 / 1200)), (hauteur * (530 / 800)), (largeur * (70 / 1200)), (hauteur * (570 / 800)))
            # Changement pour la variante Scores
            elif x[0] >= (largeur * (430 / 1200)) and x[0] <= (largeur * (470 / 1200)) and x[1] >= (
                    hauteur * (530 / 800)) and x[1] <= (hauteur * (570 / 800)):
                var_sco = changement_variante(var_sco, liste_carres_variantes[1], (largeur * (
                    430 / 1200)), (hauteur * (530 / 800)), (largeur * (470 / 1200)), (hauteur * (570 / 800)))
            # Changement pour la variante Taille des  boules
            elif x[0] >= (largeur * (830 / 1200)) and x[0] <= (largeur * (870 / 1200)) and x[1] >= (
                    hauteur * (530 / 800)) and x[1] <= (hauteur * (570 / 800)):
                var_tai = changement_variante(var_tai, liste_carres_variantes[2], (largeur * (
                    830 / 1200)), (hauteur * (530 / 800)), (largeur * (870 / 1200)), (hauteur * (570 / 800)))
            # Changement pour la variante Dynamique
            elif x[0] >= (largeur * (30 / 1200)) and x[0] <= (largeur * (70 / 1200)) and x[1] >= (
                    hauteur * (660 / 800)) and x[1] <= (hauteur * (700 / 800)):
                var_dyn = changement_variante(var_dyn, liste_carres_variantes[3], (largeur * (
                    30 / 1200)), (hauteur * (660 / 800)), (largeur * (70 / 1200)), (hauteur * (700 / 800)))
            # Changement pour la variante Terminaison
            elif x[0] >= (largeur * (430 / 1200)) and x[0] <= (largeur * (470 / 1200)) and x[1] >= (
                    hauteur * (660 / 800)) and x[1] <= (hauteur * (700 / 800)):
                var_ter = changement_variante(var_ter, liste_carres_variantes[4], (largeur * (
                    430 / 1200)), (hauteur * (660 / 800)), (largeur * (470 / 1200)), (hauteur * (700 / 800)))
            # Changement pour la variante Obstacles
            elif x[0] >= (largeur * (830 / 1200)) and x[0] <= (largeur * (870 / 1200)) and x[1] >= (
                    hauteur * (660 / 800)) and x[1] <= (hauteur * (700 / 800)):
                var_obs = changement_variante(var_obs, liste_carres_variantes[5], (largeur * (
                    830 / 1200)), (hauteur * (660 / 800)), (largeur * (870 / 1200)), (hauteur * (700 / 800)))

            mise_a_jour()
            x = attente_clic()
            # Permet à l'utilisateur de cliquer sur les boutons Jouer ou Quitter afin de voir s'afficher une fenêtre de sortie ou de continuité sur le jeu
            # (affichant dans ce cas directement la suite du jeu : choix des couleurs, ...)
            if x[0] >= ((largeur * (200 / 1200))) and x[0] <= ((largeur * (400 / 1200))) and x[1] >= (
                    (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800))):
                efface('menu')
                liste_variantes = [var_sab, var_sco,
                                   var_tai, var_dyn, var_ter, var_obs]
                jouer()
            elif x[0] >= ((largeur * (800 / 1200))) and x[0] <= ((largeur * (1000 / 1200))) and x[1] >= (
                    (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800))):
                quitter()
            elif x[0] >= ((largeur * (500 / 1200))) and x[0] <= ((largeur * (700 / 1200))) and x[1] >= (
                    (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800))):
                clique_charger()


def menu_principal():
    """Affiche le menu principal permettant de jouer (avec ou sans variantes) ou de quitter le jeu"""
    global nb_tour
    global budget
    global si_ter
    global liste_variantes
    global lst_couleurs_joueurs
    global liste_obstacles
    global var_sab
    global var_sco
    global var_tai
    global var_dyn
    global var_ter
    global var_obs
    global rayon
    global charger
    charger = False
    var_sab = False
    var_sco = False
    var_tai = False
    var_dyn = False
    var_ter = False
    var_obs = False
    liste_variantes = [var_sab, var_sco, var_tai, var_dyn, var_ter, var_obs]
    budget = dico_valeurs['budget']
    nb_tour = dico_valeurs['nb_tour']
    rayon = dico_valeurs['rayon']
    si_ter = 0
    lst_couleurs_joueurs = []
    liste_obstacles = []
    liste_carres_variantes = affichage_menu_principal()
    mise_a_jour()
    x = attente_clic()
    choix_variantes(x, liste_carres_variantes)


# CHARGEMENT DE PARTIE


def liste_saves():
    """Renvoie la liste des derniers fichiers de sauvegarde disponibles
    (6 au maximum)"""
    liste = os.listdir()[::-1]
    liste_saves = []
    for i in liste:
        if i[-4:] == '.txt' and i[:4] == 'save':
            liste_saves.append(i)
        if len(liste_saves) == 6:
            break
    return liste_saves


def affichage_saves(liste_saves):
    """Affiche la liste des fichiers de sauvegarde
    Permet de charger une partie ou de revenir au menu principal
    Prend en paramètre la liste des fichiers de sauvegarde"""
    # Affichage du fond
    rectangle(0, 0, largeur, hauteur, remplissage='grey25', tag='saves')
    # Affichage du cadre
    rectangle((largeur * (100 / 1200)), (hauteur * (50 / 800)), (largeur * (1100 / 1200)),
              (hauteur * (600 / 800)), remplissage='grey50', tag='saves')
    # Affichage du titre
    texte(largeur / 2, (hauteur * (80 / 800)), 'Sauvegardes',
          ancrage='center', taille=loelia, tag='saves')
    texte(largeur / 2, (hauteur * (115 / 800)), 'Voici vos dernières',
          ancrage='center', taille=smoll, tag='saves', couleur='AntiqueWhite')
    texte(largeur / 2, (hauteur * (130 / 800)), 'sauvegardes (max=6)',
          ancrage='center', taille=smoll, tag='saves', couleur='AntiqueWhite')
    # Affichage des boutons
    rectangle((largeur * (200 / 1200)), (hauteur * (650 / 800)), (largeur * (400 / 1200)),
              (hauteur * (750 / 800)), remplissage='sky blue', tag='saves', couleur='black')
    texte(largeur / 4, (hauteur * (700 / 800)), 'CHOISIR', ancrage='center',
          taille=very_big, tag='saves', couleur='black')
    rectangle((largeur * (800 / 1200)), (hauteur * (650 / 800)), (largeur * (1000 / 1200)),
              (hauteur * (750 / 800)), remplissage='salmon', tag='saves', couleur='black')
    texte((largeur * (900 / 1200)), (hauteur * (700 / 800)), 'RETOUR',
          ancrage='center', taille=very_big, tag='saves', couleur='black')
    # Affichage des fichiers de sauvegarde
    for i in range(len(liste_saves)):
        rectangle((largeur * (200 / 1200)), (hauteur * (150 / 800) + i * (hauteur * (400 / 800)) / len(liste_saves)),
                  (largeur * (1000 / 1200)),
                  (hauteur * (250 / 800) + i * (hauteur * (400 / 800)) / len(liste_saves)), remplissage='AntiqueWhite',
                  tag=i)
        texte((largeur * (600 / 1200)), (hauteur * (195 / 800) + i * (hauteur * (400 / 800)) /
                                         len(liste_saves)), liste_saves[i], ancrage='center', taille=defaut, tag=i)
    mise_a_jour()

    nombre = ''
    while type(nombre) != int:
        clic = attente_clic()
        if clic[0] >= ((largeur * (800 / 1200))) and clic[0] <= ((largeur * (1000 / 1200))) and clic[1] >= (
                (hauteur * (650 / 800))) and clic[1] <= ((hauteur * (750 / 800))):
            efface_tout()
            menu_principal()
        elif clic[0] >= ((largeur * (200 / 1200))) and clic[0] <= ((largeur * (400 / 1200))) and clic[1] >= (
                (hauteur * (650 / 800))) and clic[1] <= ((hauteur * (750 / 800))):
            nombre = demande_save(liste_saves)

            rectangle(largeur / 3, (hauteur * (300 / 800)), (largeur * (800 / 1200)),
                      (hauteur * (500 / 800)), remplissage='white smoke', tag='message')
            texte(largeur / 2, (hauteur * (360 / 800)), "Vous allez charger",
                  taille=biggie, ancrage='center', tag='message', police="Arial")
            texte(largeur / 2, (hauteur * (390 / 800)), "la sauvegarde " + str(nombre),
                  taille=biggie, ancrage='center', tag='message', police="Arial")
            rectangle((largeur * (550 / 1200)), (hauteur * (425 / 800)), (largeur * (650 / 1200)),
                      (hauteur * (475 / 800)), remplissage='sky blue', tag='message')
            texte(largeur / 2, (hauteur * (450 / 800)), "OK", ancrage='center',
                  tag='message', couleur='white', police="Arial", taille=biggie)
            mise_a_jour()

            while (not (clic[0] >= ((largeur * (550 / 1200))) and clic[0] <= ((largeur * (650 / 1200))) and clic[1] >= (
                    (hauteur * (425 / 800))) and clic[1] <= ((hauteur * (475 / 800))))):
                clic = attente_clic()
                if clic[0] >= ((largeur * (550 / 1200))) and clic[0] <= ((largeur * (650 / 1200))) and clic[1] >= (
                        (hauteur * (425 / 800))) and clic[1] <= ((hauteur * (475 / 800))):
                    efface('message')
                elif clic[0] >= ((largeur * (800 / 1200))) and clic[0] <= ((largeur * (1000 / 1200))) and clic[1] >= (
                        (hauteur * (650 / 800))) and clic[1] <= ((hauteur * (750 / 800))):
                    efface_tout()
                    menu_principal()

    efface_tout()
    global nom_save
    nom_save = liste_saves[nombre - 1]


def demande_save(liste_saves):
    """Fonction qui demande le numéro de la sauvegarde à charger
    Prend en paramètre la liste des sauvegardes
    Renvoie le numéro de la sauvegarde à charger"""
    rectangle((largeur * (400 / 1200)), hauteur / 3, (largeur * (800 / 1200)),
              (hauteur * (533 / 800)), remplissage='white smoke', tag='demandesauvegarde')
    texte((largeur * (600 / 1200)), (hauteur * (310 / 800)), "Quel sauvegarde voulez vous charger?",
          taille=biggie, ancrage='center', tag='demandesauvegarde', police="Arial")
    texte((largeur * (600 / 1200)), (hauteur * (330 / 800)), "Choisissez un chiffre de 1 à " +
          str(len(liste_saves)), taille=biggie, ancrage='center', tag='demandesauvegarde', police="Arial")
    entree = ('', '')
    nombre = ''
    while entree[1] != "Return":
        # L'utilisateur doit appuyer sur entrée pour valider
        entree = attente_clic_ou_touche()
        if entree[2] == 'Touche':
            # vérifie si l'entrée est un chiffre convenable
            if entree[1] in [str(i) for i in range(1, len(liste_saves) + 1)]:
                nombre = entree[1]  # ajoute l'entrée au nombre total
            # supprime la derniere entree si on appuie sur BackSpace
            elif entree[1] == 'BackSpace':
                if nombre != '':
                    nombre = ''
            efface("textesauvegarde")
            texte((largeur * (600 / 1200)), hauteur * (400 / 800), nombre, taille=biggie,
                  ancrage='center', tag='demandesauvegarde textesauvegarde', police="Arial")
            mise_a_jour()
        else:
            # si le joueur clique sur le bouton quitter
            if entree[0] >= (largeur * (800 / 1200)) and entree[0] <= (largeur * (1000 / 1200)) and entree[1] >= (
                    hauteur * (650 / 800)) and entree[1] <= (hauteur * (750 / 800)):
                efface_tout()
                menu_principal()
    efface('demandesauvegarde')
    if nombre != '':
        nombre = int(nombre)
    return nombre


def chargement_partie():
    """Fonction qui charge les données de la partie
    Extrait les données du fichier et les met dans le dictionnaire dico_chargement"""
    global dico_chargement
    with open(nom_save, 'r') as fichier:
        lignes = fichier.read().splitlines()
    for i in range(11):
        dico_chargement[lignes[i].split('=')[0]] = int(lignes[i].split('=')[1])

    chaine = lignes[11].split('=')[1]
    dico_chargement[lignes[11].split('=')[0]] = mise_forme_couleur(chaine)
    chaine = lignes[12].split('=')[1]
    dico_chargement[lignes[12].split('=')[0]] = mise_forme_variantes(chaine)
    chaine = lignes[13].split('=')[1]
    dico_chargement[lignes[13].split('=')[0]] = mise_forme_lst(chaine)
    chaine = lignes[14].split('=')[1]
    dico_chargement[lignes[14].split('=')[0]] = mise_forme_lst(chaine)
    chaine = lignes[15].split('=')[1]
    dico_chargement[lignes[15].split('=')[0]] = mise_forme_lst_obstacle(chaine)


def mise_forme_couleur(chaine):
    """Extrait la liste des couleurs des joueurs du fichier et renvoie la liste mise en forme"""
    lst_couleurs = chaine[1:-1].split(', ')
    lst_couleurs[0] = lst_couleurs[0][1:-1]
    lst_couleurs[1] = lst_couleurs[1][1:-1]
    return lst_couleurs


def mise_forme_variantes(chaine):
    """Extrait la liste des variantes du fichier de la chaîne prise en paramètres et renvoie la liste mise en forme"""
    lst_variantes = chaine[1:-1].split(', ')
    for i in range(len(lst_variantes)):
        if lst_variantes[i] == 'False':
            lst_variantes[i] = False
        else:
            lst_variantes[i] = True
    return lst_variantes


def mise_forme_lst_obstacle(chaine):
    """Extrait la liste des obstacles du fichier de la chaîne prise en paramètres et renvoie la liste mise en forme"""
    if chaine == '[]':
        return []
    return json.loads(chaine.replace("\'", "\""))


def mise_forme_lst(chaine):
    """Extrait la liste des joueurs ou des obstacles du fichier de la chaîne prise en paramètres et renvoie la liste mise en forme"""
    if chaine == '[]':
        return []
    entree = chaine[1:-1].split(', ')
    lst_joueur = []
    for i in range((len(entree) // 5)):
        lst_temp = []
        for j in range(5):
            if j < 3:
                if j == 0:
                    entree[j + 5 * i] = entree[j + 5 * i][1:]
                lst_temp.append(float(entree[j + 5 * i]))
            if j == 3:
                lst_temp.append(entree[j + 5 * i][1:-1])
            if j == 4:
                lst_temp.append(entree[j + 5 * i][1:-2])
        lst_joueur.append(lst_temp)
    return lst_joueur


# CHOIX DES COULEURS
def choix_couleur_joueur(couleur_par_defaut):
    """Affiche un cadre permettant au joueur de choisir sa couleur de boule
    Prend en paramètre la couleur par défaut du joueur
    Renvoie la couleur choisie par le joueur"""
    # Choix de couleur du joueur
    x = attente_clic()
    if x[0] >= (largeur * (350 / 1200)) and x[0] <= (largeur * (450 / 1200)) and x[1] >= (hauteur * (275 / 800)) and x[
            1] <= (hauteur * (375 / 800)):
        couleur = 'salmon'
    elif x[0] >= (largeur * (550 / 1200)) and x[0] <= (largeur * (650 / 1200)) and x[1] >= (hauteur * (275 / 800)) and \
            x[1] <= (hauteur * (375 / 800)):
        couleur = 'tan1'
    elif x[0] >= (largeur * (750 / 1200)) and x[0] <= (largeur * (850 / 1200)) and x[1] >= (hauteur * (275 / 800)) and \
            x[1] <= (hauteur * (375 / 800)):
        couleur = 'khaki'
    elif x[0] >= (largeur * (350 / 1200)) and x[0] <= (largeur * (450 / 1200)) and x[1] >= (hauteur * (525 / 800)) and \
            x[1] <= (hauteur * (625 / 800)):
        couleur = 'MediumPurple1'
    elif x[0] >= (largeur * (550 / 1200)) and x[0] <= (largeur * (650 / 1200)) and x[1] >= (hauteur * (525 / 800)) and \
            x[1] <= (hauteur * (625 / 800)):
        couleur = 'SkyBlue2'
    elif x[0] >= (largeur * (750 / 1200)) and x[0] <= (largeur * (850 / 1200)) and x[1] >= (hauteur * (525 / 800)) and \
            x[1] <= (hauteur * (625 / 800)):
        couleur = 'PaleGreen1'
    else:
        couleur = couleur_par_defaut
    return couleur


def choix_couleur():
    """Permet aux deux joueurs de choisir une couleur différente parmi 6 couleurs possibles (rouge, orange, jaune, violet, bleu, vert)"""
    rectangle(0, 0, largeur, hauteur,
              remplissage='grey50', tag='configuration')
    rectangle((largeur * (300 / 1200)), (hauteur * (100 / 800)), (largeur * (900 / 1200)),
              (hauteur * (700 / 800)), remplissage='grey25', tag='configuration')
    texte(largeur / 2, (hauteur * (150 / 800)), "Configuration de la partie", taille=smoll,
          ancrage='center', tag='configuration', police="Arial", couleur='AntiqueWhite')

    # Affichage des couleurs possibles
    choixcouleur = texte(largeur / 2, (hauteur * (200 / 800)), "Joueur 1, choisissez une couleur",
                         ancrage='center', tag='choix_de_couleur', police="Arial", couleur='AntiqueWhite',
                         taille=defaut)
    rectangle((largeur * (350 / 1200)), (hauteur * (275 / 800)), (largeur * (450 / 1200)),
              (hauteur * (375 / 800)), remplissage='salmon', tag='choix_de_couleur')
    rectangle((largeur * (550 / 1200)), (hauteur * (275 / 800)), (largeur * (650 / 1200)),
              (hauteur * (375 / 800)), remplissage='tan1', tag='choix_de_couleur')
    rectangle((largeur * (750 / 1200)), (hauteur * (275 / 800)), (largeur * (850 / 1200)),
              (hauteur * (375 / 800)), remplissage='khaki', tag='choix_de_couleur')
    rectangle((largeur * (350 / 1200)), (hauteur * (525 / 800)), (largeur * (450 / 1200)),
              (hauteur * (625 / 800)), remplissage='MediumPurple1', tag='choix_de_couleur')
    rectangle((largeur * (550 / 1200)), (hauteur * (525 / 800)), (largeur * (650 / 1200)),
              (hauteur * (625 / 800)), remplissage='SkyBlue2', tag='choix_de_couleur')
    rectangle((largeur * (750 / 1200)), (hauteur * (525 / 800)), (largeur * (850 / 1200)),
              (hauteur * (625 / 800)), remplissage='PaleGreen1', tag='choix_de_couleur')
    mise_a_jour()

    # Choix de couleur du joueur 1
    couleur1 = choix_couleur_joueur('SkyBlue2')

    # Choix de couleur du joueur 2
    efface(choixcouleur)
    choixcouleur = texte(largeur / 2, (hauteur * (200 / 800)), "Joueur 2, choisissez une autre couleur",
                         ancrage='center', tag='choix_de_couleur', police="Arial", couleur='AntiqueWhite',
                         taille=defaut)
    mise_a_jour()
    couleur2 = choix_couleur_joueur('salmon')

    # attribue une couleur différente au joueur2 s'il choisit la même que le joueur1
    if couleur1 == couleur2:
        if couleur1 == 'SkyBlue2':
            couleur2 = 'salmon'
        else:
            couleur2 = 'SkyBlue2'

    # sauvegarde des couleurs choisies dans une liste dédiée
    lst_couleurs_joueurs.append(couleur1)
    lst_couleurs_joueurs.append(couleur2)

    efface("choix_de_couleur")

    # Résumé du choix des couleurs de chaque joueur
    texte(largeur / 2, (hauteur * (300 / 800)), "JOUEUR 1", couleur=couleur1,
          taille=bbb, ancrage='center', tag='configuration', police="Arial")
    ligne((largeur * (400 / 1200)), (hauteur * (400 / 800)), (largeur * (800 / 1200)),
          (hauteur * (400 / 800)), epaisseur=3, tag='configuration')
    texte(largeur / 2, (hauteur * (500 / 800)), "JOUEUR 2", couleur=couleur2,
          taille=bbb, ancrage='center', tag='configuration', police="Arial")
    mise_a_jour()

    attente_clic()
    efface("configuration")
    efface("choix_de_couleur")
    mise_a_jour()


# INTERFACE DE JEU


def interface_jeu():
    """Affiche l'aire de jeu, les informations sur les variantes, et le bouton quitter et pause"""
    # délimitation de l'aire de jeu disponible
    rectangle(0, 0, largeur_aire, hauteur_aire,
              remplissage='grey19', tag='aire_de_jeu')

    # début panneau d'informations situé à droite de l'aire de jeu
    rectangle(largeur, hauteur, (largeur*(800/1200)),
              0, remplissage='gray40', tag='infos')

    texte((largeur*(1000/1200)), (hauteur*(50/800)), "Bataille des Boules",
          taille=bbb, ancrage='center', tag='infos', police="Arial")

    texte((largeur*(850/1200)), (hauteur*(150/800)), "Tour de : ",
          ancrage='w', tag='infos', police="Arial", taille=defaut)

    # Informations sur la variante "Sablier"
    if liste_variantes[0] == True:
        texte((largeur * (850 / 1200)), (hauteur * (250 / 800)), "Sablier ⏳: ",
              ancrage='w', tag='infos', police="Arial", taille=defaut)

    # Informations sur la variante "Scores"
    if liste_variantes[1] == True:
        texte((largeur * (850 / 1200)), (hauteur * (350 / 800)), "Scores 🏆: ",
              ancrage='w', tag='infos', police="Arial", taille=defaut)
        texte((largeur * (1025 / 1200)), (hauteur * (350 / 800)), "J1", ancrage='w',
              tag='infos', couleur=lst_couleurs_joueurs[0], police="Arial", taille=defaut)
        texte((largeur * (1100 / 1200)), (hauteur * (350 / 800)), "J2", ancrage='w',
              tag='infos', couleur=lst_couleurs_joueurs[1], police="Arial", taille=defaut)

    # Informations sur la variante "Budgets
    if liste_variantes[2] == True:
        texte((largeur * (850 / 1200)), (hauteur * (450 / 800)), "Budgets 💰: ",
              ancrage='w', tag='infos', police="Arial", taille=defaut)
        texte((largeur * (1025 / 1200)), (hauteur * (450 / 800)), "J1", ancrage='w',
              tag='infos', couleur=lst_couleurs_joueurs[0], police="Arial", taille=defaut)
        texte((largeur * (1100 / 1200)), (hauteur * (450 / 800)), "J2", ancrage='w',
              tag='infos', couleur=lst_couleurs_joueurs[1], police="Arial", taille=defaut)

    # Informations sur le nombre de tours restants avant la fin de la partie
    texte((largeur * (850 / 1200)), (hauteur * (550 / 800)), "Tours restants : ",
          ancrage='w', tag='infos', police="Arial", taille=defaut)

    rectangle((largeur * (850 / 1200)), (hauteur * (610 / 800)), (largeur * (1150 / 1200)),
              (hauteur * (670 / 800)), remplissage='tan1', couleur='tan1', tag='infos')
    texte((largeur * (1000 / 1200)), (hauteur * (640 / 800)), "Pause", ancrage='center',
          tag='infos', couleur='white', police="Arial", taille=defaut)

    rectangle((largeur * (850 / 1200)), (hauteur * (690 / 800)), (largeur * (1150 / 1200)),
              (hauteur * (750 / 800)), remplissage='salmon', couleur='salmon', tag='infos')
    texte((largeur * (1000 / 1200)), (hauteur * (720 / 800)), "Quitter", ancrage='center',
          tag='infos', couleur='white', police="Arial", taille=defaut)
    # fin panneau d'informations

    mise_a_jour()


# ORGANISATION DU JEU
def action_joueur(clic, couleur_ennemi, liste_ennemi, liste_cercles_ennemi, budget_joueur, couleur_joueur, liste_joueur,
                  liste_cercles_joueur, budgetJ1, budgetJ2, lst_J1, lst_J2):
    """Fonction qui permet de gérer les actions du joueur lorsqu'il clique sur l'aire de jeu
    Prend en paramètres le clic du joueur, la couleur de l'ennemi, la liste des coordonnees des cercles ennemis, la liste des cercles ennemis, le budget du joueur, la couleur du joueur, la liste des coordonnees des cercles du joueur, la liste des cercles du joueur
    Renvoie le budget du joueur"""
    global rayon
    if liste_variantes[2] == True and verifier_divise_ennemi(clic, liste_ennemi, liste_cercles_ennemi) == False:
        if budget_joueur >= 1:
            rayon = tailledesboules(
                budget_joueur, budgetJ1, budgetJ2, lst_J1, lst_J2)
        else:
            rayon = 0
            # le joueur perd son tour
    if verifier_hors_aire(clic) == True:  # si le cercle sort de l'aire de jeu
        # si le joueur ne clique pas sur une boule ennemie
        if verifier_divise_ennemi(clic, liste_ennemi, liste_cercles_ennemi) == False:
            pass  # joueur perd son tour
        else:
            # sinon, on récupère les coordonnées du cercle à supprimer
            xc, yc, rc, cercle_a_supprimer = verifier_divise_ennemi(
                clic, liste_ennemi, liste_cercles_ennemi)
            coupe_ennemi(xc, yc, rc, clic, liste_ennemi, couleur_ennemi,
                         cercle_a_supprimer, liste_cercles_ennemi)  # couper l'ennemi
    else:
        # si le joueur clique trop près d'un ennemi
        if verifier_trop_proche(clic, liste_ennemi) == True:
            # si le joueur ne clique pas sur une boule ennemie
            if verifier_divise_ennemi(clic, liste_ennemi, liste_cercles_ennemi) == False:
                pass  # joueur perd tour
            else:
                # sinon, on récupère les coordonnées du cercle à supprimer
                xc, yc, rc, cercle_a_supprimer = verifier_divise_ennemi(
                    clic, liste_ennemi, liste_cercles_ennemi)
                coupe_ennemi(xc, yc, rc, clic, liste_ennemi, couleur_ennemi,
                             cercle_a_supprimer, liste_cercles_ennemi)  # couper l'ennemi
        # si la boule touche un obstacle
        elif liste_variantes[5] == True and verifier_collision_obstacle(clic, rayon) == True:
            pass  # le joueur perd son tour
        else:
            if liste_variantes[2] == True:
                if budget_joueur >= 1:
                    liste_cercles_joueur.append(cercle(
                        clic[0], clic[1], rayon, remplissage=couleur_joueur, tag='cercle'))  # ajouter une boule
                    # ajouter les coordonnées de la boule dans la liste des boules du joueur 1
                    liste_joueur.append(
                        [clic[0], clic[1], rayon, couleur_joueur, 'cercle'])
                    budget_joueur -= rayon  # soustrait le rayon du cercle au budget du J1
            else:
                liste_cercles_joueur.append(cercle(
                    clic[0], clic[1], rayon, remplissage=couleur_joueur, tag='cercle'))  # ajouter une boule
                # ajouter les coordonnées de la boule dans la liste des boules du joueur 1
                liste_joueur.append(
                    [clic[0], clic[1], rayon, couleur_joueur, 'cercle'])
    return budget_joueur


def jeu():
    """Définition de l'ensemble des informations permettant à chaque joueur de placer des boules et d'actualiser le nombre de tours restants
    Retourne les listes des coordonnées des boules des joueurs"""
    global liste_obstacles
    global si_ter
    global nb_tour
    if charger == True:
        # liste des coordonnees des boules du joueur 1
        lst_J1 = dico_chargement['lst_J1']
        # liste des coordonnees des boules du joueur 2
        lst_J2 = dico_chargement['lst_J2']
    else:
        lst_J1 = []
        lst_J2 = []
    liste_cercles_J1 = chargement_boules('J1')  # liste des cercles du joueur 1
    liste_cercles_J2 = chargement_boules('J2')  # liste des cercles du joueur 2
    texte_joueur = texte(lst_coord_tour_joueur[nb_tour % 2][0], lst_coord_tour_joueur[nb_tour % 2][1],
                         joueur_actif[nb_tour %
                                      2], ancrage='w', couleur=lst_couleurs_joueurs[nb_tour % 2], police="Arial",
                         taille=defaut)  # affichage du joueur qui joue
    texte_tour = texte(coord_nb_tour[0], coord_nb_tour[1], str(
        nb_tour), ancrage='w', police="Arial", taille=defaut)  # affichage des tours restants
    if charger == False:
        budgetJ1, budgetJ2 = budget, budget  # Le budget de la variante Taille des boules
    else:
        budgetJ1, budgetJ2 = dico_chargement['budgetJ1'], dico_chargement['budgetJ2']
    if liste_variantes[5] == True:  # si la variante Obstacles est activée
        if charger == False:
            if choix_obstacles():
                obstacles()
            else:
                choix = choix_obstacles_fichier()
                obstacles_fichier_texte(choix)
        else:
            liste_obstacles = dico_chargement['liste_obstacles']
        for element in liste_obstacles:
            if element[0] == 'c':
                cercle(element[2], element[3], element[1], remplissage='grey50', couleur=element[4],
                       tag='obstacles')
            elif element[0] == 'r':
                rectangle(element[1], element[2], element[3], element[4], remplissage='grey50',
                          couleur=element[5], tag='obstacles')

    while nb_tour != 0:  # boucle while se terminant lorsque tous les tours ont été joués
        if nb_tour % 2 == 0:
            coord_tour = lst_coord_tour_joueur[1][0]
            joueur = joueur_actif[1]
            couleur = lst_couleurs_joueurs[1]
        else:
            coord_tour = lst_coord_tour_joueur[0][0]
            joueur = joueur_actif[0]
            couleur = lst_couleurs_joueurs[0]
        if liste_variantes[2] == True:
            # affiche les budgets si la variante est activée
            variante_budget(budgetJ1, budgetJ2)
        if liste_variantes[0] == True:
            evenement, nb_tour = timer(
                lst_J1, lst_J2, texte_tour, budgetJ1, budgetJ2)

            texte_tour = texte(coord_nb_tour[0], coord_nb_tour[1], str(
                nb_tour), ancrage='w', police="Arial", taille=defaut)

            if evenement != None:
                clic = (clic_x(evenement), clic_y(evenement))
                if nb_tour % 2 == 1:
                    budgetJ2 = action_joueur(clic, lst_couleurs_joueurs[0], lst_J1, liste_cercles_J1, budgetJ2,
                                             lst_couleurs_joueurs[1], lst_J2, liste_cercles_J2, budgetJ1, budgetJ2,
                                             lst_J1, lst_J2)
                elif nb_tour % 2 == 0:
                    budgetJ1 = action_joueur(clic, lst_couleurs_joueurs[1], lst_J2, liste_cercles_J2, budgetJ1,
                                             lst_couleurs_joueurs[0], lst_J1, liste_cercles_J1, budgetJ1, budgetJ2,
                                             lst_J1, lst_J2)
            nb_tour -= 1
        else:
            ev = attente_clic_ou_touche()
            if ev[2] == 'Touche':
                if ev[1] == 's' and liste_variantes[1] == True:
                    # affichage des scores pendant deux secondes
                    variante_score(lst_J1, lst_J2)
                elif ev[1] == 't' and liste_variantes[4] == True:
                    # Laisse l'option de décider si le jeu se termine dans 5 tour
                    nb_tour1 = terminaison()
                    if nb_tour1 == 10:
                        if nb_tour % 2 == 0:
                            nb_tour = 10
                        else:
                            nb_tour = 9
                        si_ter = 1
                    efface(texte_tour)
                    texte_tour = texte(coord_nb_tour[0], coord_nb_tour[1], str(
                        nb_tour), ancrage='w', police="Arial", taille=defaut)
                    mise_a_jour()

                continue
            elif ev[2] == 'ClicGauche' or 'ClicDroit':
                clic = ev
            # si le joueur clique sur le bouton quitter
            if clic[0] >= (largeur * (850 / 1200)) and clic[0] <= (largeur * (1150 / 1200)) and clic[1] >= (
                    hauteur * (690 / 800)) and clic[1] <= (hauteur * (750 / 800)):
                quitter()
                continue
            # si le joueur clique sur le bouton pause
            elif clic[0] >= (largeur * (850 / 1200)) and clic[0] <= (largeur * (1150 / 1200)) and clic[1] >= (
                    hauteur * (610 / 800)) and clic[1] <= (hauteur * (670 / 800)):
                pause(budgetJ1, budgetJ2, lst_J1, lst_J2)
                continue
            # si le joueur clique dans l'aire de jeu
            elif clic[0] >= 0 and clic[0] <= largeur_aire and clic[1] >= 0 and clic[1] <= hauteur_aire:
                # Dans le cas du joueur 1
                if nb_tour % 2 == 0:
                    budgetJ1 = action_joueur(clic, lst_couleurs_joueurs[1], lst_J2, liste_cercles_J2, budgetJ1,
                                             lst_couleurs_joueurs[0], lst_J1, liste_cercles_J1, budgetJ1, budgetJ2,
                                             lst_J1, lst_J2)

                # Dans le cas du joueur 2
                elif nb_tour % 2 == 1:
                    budgetJ2 = action_joueur(clic, lst_couleurs_joueurs[0], lst_J1, liste_cercles_J1, budgetJ2,
                                             lst_couleurs_joueurs[1], lst_J2, liste_cercles_J2, budgetJ1, budgetJ2,
                                             lst_J1, lst_J2)

                nb_tour -= 1
            else:
                continue

        if liste_variantes[3] == True:
            liste_cercles_J1, liste_cercles_J2 = dynamique(
                lst_J1, lst_J2, liste_cercles_J1, liste_cercles_J2)
        # Actualisation du nombre de tours restants lorsque chaque joueur a placé une boule et du joueur dont c'est le tour
        efface(texte_joueur)
        efface(texte_tour)
        texte_joueur = texte(coord_tour, (hauteur * (150 / 800)), joueur,
                             ancrage='w', couleur=couleur, police="Arial", taille=defaut)
        texte_tour = texte(coord_nb_tour[0], coord_nb_tour[1], str(
            nb_tour), ancrage='w', police="Arial", taille=defaut)
        mise_a_jour()

    return lst_J1, lst_J2


def verifier_hors_aire(clic):
    """Permet de vérifier si le cercle sort de l'aire de jeu
    Prend en paramètres les coordonnées du clic
    Renvoie False si la boule est dans l'aire, et True sinon"""
    # vérifier si le cercle sort de l'aire (en prenant en compte le clic et le rayon)
    if clic[0] >= rayon and clic[0] <= largeur_aire-rayon and clic[1] >= rayon and clic[1] <= hauteur_aire-rayon:
        return False
    return True


def verifier_trop_proche(clic, lst_ennemi):
    """Permet de vérifier si le cercle est trop proche d'un cercle ennemi
    Prend en paramètres les coordonnées du clic et la liste des coordonnées des boules ennemies
    Renvoie True si le clic est trop proche d'une boule ennemie, et False sinon"""
    for element in lst_ennemi:
        # vérifier si les cercles s'intersecteront (distance inférieure au rayon*2)
        if sqrt((clic[0] - element[0]) ** 2 + (clic[1] - element[1]) ** 2) <= (rayon + element[2]):
            return True
    return False


def verifier_divise_ennemi(clic, lst_coord_ennemi, lst_cercle_ennemi):
    """Permet de vérifier si le joueur peut diviser un cercle ennemi
    Prend en paramètres les coordonnées du clic, la liste des coordonnées des boules ennemies et liste des cercles de l'ennemi
    Renvoie l'abscisse, l'ordonnée du centre et le rayon du cercle à diviser, ainsi que l'élément concerné dans la liste des cercles de l'ennemi et False sinon"""
    i = len(lst_coord_ennemi) - 1
    # parcourir la liste ennemie à partir du dernier cercle
    for element in lst_coord_ennemi[::-1]:
        # vérifier si la distance entre le clic et le centre est inférieure au rayon
        if sqrt((clic[0] - element[0]) ** 2 + (clic[1] - element[1]) ** 2) <= element[2]:
            return element[0], element[1], element[2], lst_cercle_ennemi[i]
        i -= 1
    return False


def coupe_ennemi(xc, yc, rc, clic, lst_coord_ennemi, couleur, cercle_a_supprimer, lst_cercle_ennemi):
    """Permet à l'un des 2 joueurs lorsque son tour arrive de découper le cercle de son adversaire
    Prend en paramètres l'abscisse, l'ordonnée du centre et le rayon du cercle à diviser, la liste des coordonnées des boules ennemies,
    la couleur de l'ennemi, l'élément concerné dans la liste des cercles de l'ennemi et liste des cercles de l'ennemi"""
    if clic[0] != xc and clic[1] != yc:
        # calculer le produit scalaire du vecteur u partant du centre du cercle initial au clic
        distance_clic_centre = sqrt((clic[0] - xc) ** 2 + (clic[1] - yc) ** 2)
        # le rayon est égal à la différence entre le rayon du cercle initial et le vecteur u
        r1 = abs(rc - distance_clic_centre)
        # les vecteurs u et le vecteur reliant le centre du deuxième cercle au cercle initial sont colinéaires, donc il existe une constante k telle que u=kv
        # Ainsi k=u/v. Or u=distance_clic_centre et v=r1
        k = distance_clic_centre / r1
        # En prenant les coordonnées des vecteurs et retournant la formule k=u/v on trouve les coordonnées du deuxième cercle
        # trouver les coordonnées x du centre du deuxième cercle
        x2 = xc - ((clic[0] - xc) / k)
        y2 = yc - ((clic[1] - yc) / k)
        # ajouter les coordonnées des nouveaux cercles à la liste
        lst_coord_ennemi.append([clic[0], clic[1], r1, couleur, 'cercle'])
        lst_coord_ennemi.append(
            [x2, y2, distance_clic_centre, couleur, 'cercle'])
        # enlever le cercle ennemi
        i = 0
        lst_cercle_ennemi.append(cercle(
            clic[0], clic[1], r1, remplissage=couleur, tag='cercle'))  # créer le premier cercle
        lst_cercle_ennemi.append(cercle(x2, y2, distance_clic_centre,
                                        remplissage=couleur, tag='cercle'))  # créer le deuxième cercle
        for element in lst_coord_ennemi:
            # trouver les coordonnées du cercle initial à supprimer
            if element[0] == xc and element[1] == yc and element[2] == rc:
                # supprimer les coordonnées du cercle initial
                lst_coord_ennemi.remove(element)
                lst_cercle_ennemi.pop(i)  # supprimer le cercle dans la liste
                break
            i += 1
        # effacer le cercle ennemi
        efface(cercle_a_supprimer)


# VARIANTES
def timer(lst_J1, lst_J2, texte_tour, budgetJ1, budgetJ2):
    """Permet de lancer un timer de 5 secondes
    Prend en paramètres les listes des coordonnées des cercles des joueurs, le texte permettant d'afficher le nombre de tours restants, le numéro du tour et les budgets des joueurs
    Renvoie l'évènement si le jouueur à cliqué, sinon None ; et le nombre de tours restants"""
    global si_ter
    global nb_tour
    # type_ev != 'Touche'
    temps = time()
    texte(largeur * (1062 / 1200), (hauteur * (250 / 800)), '',
          ancrage='w', tag='timer', police="Arial", taille=defaut)
    mise_a_jour()
    decompte = temps_tour
    while time() - temps <= temps_tour:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        texte(largeur * (1062 / 1200), (hauteur * (250 / 800)), str(temps_tour -
                                                                    int(time() - temps)) + 's', ancrage='w',
              tag='timer', police="Arial")
        mise_a_jour()
        if type_ev == 'Touche':
            touche(ev)
            if touche(ev) == 's' and liste_variantes[1] == True:
                # affichage des scores pendant deux secondes
                variante_score(lst_J1, lst_J2)
            elif touche(ev) == 't' and liste_variantes[4] == True:
                # Laisse l'option de décider si le jeu se termine dans 5 tour
                nb_tour1 = terminaison()
                if nb_tour1 == 10:
                    if nb_tour % 2 == 0:
                        nb_tour = 10
                    else:
                        nb_tour = 9
                    si_ter = 1
                    efface(texte_tour)
                    texte_tour = texte(coord_nb_tour[0], coord_nb_tour[1], str(
                        nb_tour), ancrage='w', police="Arial", taille=defaut)
                mise_a_jour()
            continue

        elif type_ev == 'ClicDroit' or type_ev == "ClicGauche":
            texte(largeur * (1062 / 1200), (hauteur * (250 / 800)), '',
                  ancrage='w', tag='timer', police="Arial", taille=defaut)
            mise_a_jour()
            clic = (clic_x(ev), clic_y(ev))
            # si le joueur clique sur le bouton quitter
            if clic[0] >= (largeur * (850 / 1200)) and clic[0] <= (largeur * (1150 / 1200)) and clic[1] >= (
                    hauteur * (690 / 800)) and clic[1] <= (hauteur * (750 / 800)):
                quitter()
            # si le joueur clique sur le bouton pause
            elif clic[0] >= (largeur * (850 / 1200)) and clic[0] <= (largeur * (1150 / 1200)) and clic[1] >= (
                    hauteur * (610 / 800)) and clic[1] <= (hauteur * (670 / 800)):
                pause(budgetJ1, budgetJ2, lst_J1, lst_J2)
            # si le joueur clique dans l'aire de jeu
            elif clic[0] >= 0 and clic[0] <= largeur_aire and clic[1] >= 0 and clic[1] <= hauteur_aire:
                efface(texte_tour)
                return ev, nb_tour

        efface('timer')
        if time() - temps < decompte:
            # actualise le timer à chaque decrementation
            mise_a_jour()
            decompte -= 1
    efface(texte_tour)
    return None, nb_tour


def terminaison():
    """Permet au joueur de décider s'il souhaite que le jeu se termine dans 5 tours lorsqu'il appuie sur la touche 't'
    Renvoie 10 si le joueur a choisi de terminer le jeu dans 5 tours"""
    if si_ter == 0:
        # Demande si le joueur est sûr de vouloir activer Terminaison
        rectangle(largeur / 3, (hauteur * (300 / 800)), (largeur * (800 / 1200)),
                  (hauteur * (500 / 800)), remplissage='white smoke', tag='terminaison')
        texte(largeur / 2, (hauteur * (350 / 800)), "Voulez-vous vraiment terminer dans 5 tours ?",
              taille=smoll, ancrage='center', tag='terminaison', police="Arial")

        rectangle((largeur * (450 / 1200)), (hauteur * (425 / 800)), (largeur * (550 / 1200)),
                  (hauteur * (475 / 800)), remplissage='PaleGreen3', tag='terminaison')
        texte((largeur * (500 / 1200)), (hauteur * (450 / 800)), "Oui", ancrage='center',
              tag='terminaison', couleur='white', police="Arial", taille=biggie)

        rectangle((largeur * (650 / 1200)), (hauteur * (425 / 800)), (largeur * (750 / 1200)),
                  (hauteur * (475 / 800)), remplissage='salmon', tag='terminaison')
        texte((largeur * (700 / 1200)), (hauteur * (450 / 800)), "Non", ancrage='center',
              tag='terminaison', couleur='white', police="Arial", taille=biggie)

        mise_a_jour()

        switch_ter = False
        while switch_ter == False:
            x = attente_clic()
            if x[0] >= largeur * (450 / 1200) and x[0] <= largeur * (550 / 1200) and x[1] >= (hauteur * (425 / 800)) and \
                    x[1] <= (hauteur * (475 / 800)):
                # S'il souhaite activer Terminaison, la fonction renvoie 5 comme étant le nombre de tours
                switch_ter = True
                efface('terminaison')
                mise_a_jour()
                return 10

            elif x[0] >= largeur * (650 / 1200) and x[0] <= largeur * (750 / 1200) and x[1] >= (
                    hauteur * (425 / 800)) and x[1] <= (hauteur * (475 / 800)):
                # Sinon, il revient à l'écran de jeu
                switch_ter = True
                efface('terminaison')
                mise_a_jour()
    else:
        # Si Terminaison a déjà été activé dans la partie, il ne peut pas être réactivé
        rectangle(largeur / 3, (hauteur * (300 / 800)), (largeur * (800 / 1200)),
                  hauteur / 2, remplissage='white smoke', tag='terminaison')
        texte(largeur / 2, (hauteur * (350 / 800)), "Vous avez déjà utilisé Terminaison",
              taille=biggie, ancrage='center', tag='terminaison', police="Arial")
        mise_a_jour()
        sleep(1)
        efface('terminaison')
        mise_a_jour()


def obstacles():
    """Permet de créer les coordonnées des obstacles et de les intégrer à la liste_obstacles"""
    liste_couleurs_possibles = list(lst_couleurs)
    liste_couleurs_possibles.remove(lst_couleurs_joueurs[0])
    liste_couleurs_possibles.remove(lst_couleurs_joueurs[1])
    global liste_obstacles
    nb_obstacles = randint(4, 7)
    while len(liste_obstacles) < nb_obstacles:
        # 0 pour les cercles et 1 pour les rectangles
        num_obstacles = randint(0, 1)
        if num_obstacles == 0:  # Lorsqu'on tombe sur 0
            r = randint(rayon*(largeur_aire)//largeur, rayon *
                        (hauteur_aire)//hauteur)  # Valeur aléatoire du rayon
            # Valeur aléatoire de la coordonnée x du centre
            x = randint(r, largeur_aire - r)
            # Valeur aléatoire de la coordonnée y du centree
            y = randint(r, hauteur_aire - r)
            for element in liste_obstacles:
                if x == element[2] and y == element[3]:
                    continue
            liste_obstacles.append(
                ["c", r, x, y, liste_couleurs_possibles[randint(0, 3)], liste_couleurs_possibles[randint(0, 3)]])  # Ajout à la liste des obstacles
        else:  # Lorsqu'on tombe sur 1
            ax = largeur_aire
            ay = 0
            bx = 0
            by = 0
            # Limite la taille de l'obstacle (Perimetre/2)
            while bx - ax + by - ay > largeur_aire / 8 or bx - ax + by - ay < largeur_aire / 10:
                # Valeur aléatoire de la coordonnée x du coin supérieur gauche
                ax = randint(0, largeur_aire)
                # Valeur aléatoire de la coordonnée y du coin supérieur gauche
                ay = randint(0, hauteur_aire)
                # Valeur aléatoire de la coordonnée x du coin inférieur droit
                bx = randint(0, largeur_aire)
                # Valeur aléatoire de la coordonnée y du coin inférieur droit
                by = randint(0, hauteur_aire)
                continue
            for element in liste_obstacles:
                if ax == element[1] and ay == element[2] and bx == element[3] and by == element[4]:
                    continue
            liste_obstacles.append(['r', ax, ay, bx, by, liste_couleurs_possibles[randint(
                0, 3)], liste_couleurs_possibles[randint(0, 3)]])  # Ajout à la liste des obstacles


def choix_obstacles():
    """Permet à l'utilisateur de choisir entre des obstacles générés de manière aléatoire ou depuis un fichier texte
    Renvoie True si l'utilisateur souhaite des obstacles aléatoires et False si il souhaite des obstacles depuis un fichier texte"""
    rectangle(largeur_aire / 2 - 200, hauteur_aire / 2 - 100, largeur_aire / 2 + 200, hauteur_aire / 2 + 100,
              remplissage="white smoke", tag='choix_obstacles')
    texte(largeur_aire / 2, hauteur_aire / 2 - 80, "Quelles types d'obstacles voulez-vous ?", taille=smoll,
          ancrage="center", tag='choix_obstacles', police="Arial")

    rectangle(largeur_aire / 2 - 180, hauteur_aire / 2, largeur_aire / 2 - 60, hauteur_aire / 2 + 80,
              remplissage="PaleGreen3", tag='choix_obstacles')
    texte(largeur_aire / 2 - 120, hauteur_aire / 2 + 40, "Aléatoire", ancrage="center", tag='choix_obstacles',
          couleur="White", police="Arial", taille=smoll)

    rectangle(largeur_aire / 2 + 180, hauteur_aire / 2, largeur_aire / 2 + 60, hauteur_aire / 2 + 80,
              remplissage="salmon", tag='choix_obstacles')
    texte(largeur_aire / 2 + 120, hauteur_aire / 2 + 40, " Depuis un\nfichier texte", ancrage="center",
          tag='choix_obstacles', couleur="White", police="Arial", taille=smoll)

    mise_a_jour()

    switch_obst = False
    while switch_obst == False:
        x = attente_clic()
        if x[0] >= largeur_aire / 2 - 180 and x[0] <= largeur_aire / 2 - 60 and x[1] >= hauteur_aire / 2 and x[
                1] <= hauteur_aire / 2 + 80:
            # choix des obstacles de manière aléatoire
            switch_obst = True
            efface('choix_obstacles')
            mise_a_jour()
            return True

        elif x[0] >= largeur_aire / 2 + 60 and x[0] <= largeur_aire / 2 + 180 and x[1] >= hauteur_aire / 2 and x[
                1] <= hauteur_aire / 2 + 80:
            # sinon choix des obstacles à partir d'un fichier
            switch_obst = True
            efface('choix_obstacles')
            mise_a_jour()
            return False


def verifier_collision_obstacle(clic, rayon):
    """Permet de vérifier si la boule du joueur entre en colision avec un obstacle
    Prend en paramètres les coordonnées du clic et le rayon de la boule
    Renvoie True si le clic est trop proche d'un obstacle, et False sinon"""
    for element in liste_obstacles:
        # vérifier si les boules des joueurs s'intersecteront avec les obstacles par rapport au centre de la boule posée
        if element[0] == 'c':  # Dans le cas d'un cercle
            distance = sqrt((clic[0] - element[2]) **
                            2 + (clic[1] - element[3]) ** 2)
            if (distance > rayon + element[1]):
                continue
            return True
        elif element[0] == 'r':  # Dans le cas d'un rectangle
            rl = min(element[1], element[3])
            rb = min(element[2], element[4])
            rr = max(element[1], element[3])
            rt = max(element[2], element[4])

            if clic[0] + rayon < rl or clic[0] - rayon > rr:
                continue
            if clic[1] + rayon < rb or clic[1] - rayon > rt:
                continue
            return True
    return False


def obstacles_fichier_texte(choix):
    """Offre la possibilité de choisir un niveau d'obstacles parmi 3 proposés : Facile, Intermédiare et Difficile et ceux depuis un
    fichier texte par niveau.
    Prend en paramètres le choix de l'utilisateurs"""
    global liste_obstacles
    liste_couleurs_possibles = list(lst_couleurs)
    liste_couleurs_possibles.remove(
        lst_couleurs_joueurs[0])  # Supprime dans la liste de couleurs d'obstacles la couleur sélectionnée par J1
    liste_couleurs_possibles.remove(
        lst_couleurs_joueurs[1])  # Supprime dans la liste de couleurs d'obstacles la couleur sélectionnée par J2

    liste_obstacles = []
    if choix == '1':  # Si l'utilisateur a sélectionné les obstacles Faciles
        fichier = 'Facile.txt'
    elif choix == '2':  # Si l'utilisateur a sélectionné les obstacles Intermédiaires
        fichier = 'Intermédiaire.txt'
    else:  # Si l'utilisateur a sélectionné les obstacles Difficiles
        fichier = 'Difficile.txt'

    with open(fichier) as fichier:  # Ouverture du fichier sélectionné
        dico = json.load(fichier)
        for obstacle in dico["structure"]:
            # La première valeur de la liste du dico est une forme
            forme = str(obstacle[0])
            if forme == 'c':  # Si la forme est un cercle
                # La 2e valeur de la liste du dico est le rayon
                r = min(obstacle[1] * largeur_aire/largeur,
                        obstacle[1] * hauteur_aire/hauteur)
                # La 3e valeur de la liste du dico est la coordonnée x du centre
                x = obstacle[2]*largeur_aire/largeur
                # La 4e valeur de la liste du dico est la coordonnée y du centre
                y = obstacle[3]*hauteur_aire/hauteur
                liste_obstacles.append([forme, r, x, y, liste_couleurs_possibles[randint(
                    0, 3)], liste_couleurs_possibles[randint(0, 3)]])  # Ajout de toutes les informations à la liste d'obstacles
            elif forme == 'r':  # Si la forme est un rectangle
                # La 2e valeur de la liste du dico est la coordonnée x du coin supérieur gauche
                ax = obstacle[1]*largeur_aire/largeur
                # La 3e valeur de la liste du dico est la coordonnée y du coin supérieur gauche
                ay = obstacle[2]*hauteur_aire/hauteur
                # La 4e valeur de la liste du dico est la coordonnée x du coin inférieur droit
                bx = obstacle[3]*largeur_aire/largeur
                # La 5e valeur de la liste du dico est la coordonnée y du coin inférieur droit
                by = obstacle[4]*hauteur_aire/hauteur
                liste_obstacles.append([forme, ax, ay, bx, by, liste_couleurs_possibles[randint(
                    0, 3)], liste_couleurs_possibles[randint(0, 3)]])  # Ajout de toutes les informations à la liste d'obstacles


def choix_obstacles_fichier():
    '''Affichage d'une fenêtre offrant la possibilité à l'utilisateur de choisir entre 3 niveaux de difficulté d'obstacles différents :
    Facile, Intermédiaire et Difficile
    Renvoie le choix du niveau de l'utilisateur 1, 2 ou 3'''
    rectangle(largeur_aire / 2 - 200, hauteur_aire / 2 - 100, largeur_aire / 2 + 200, hauteur_aire / 2 + 100,
              remplissage='white smoke', tag='choix_obstacles')
    texte(largeur_aire / 2, hauteur_aire / 2 - 80, "Choisissez un niveau d'obstacles :", taille=13, ancrage='center',
          tag='choix_obstacles', police="Arial")

    rectangle(largeur_aire / 2 - 180, hauteur_aire / 2 - 40, largeur_aire / 2 + 180, hauteur_aire / 2,
              remplissage='PaleGreen3', tag='choix_obstacles')
    texte(largeur_aire / 2, hauteur_aire / 2 - 20, "Facile", ancrage='center', tag='choix_obstacles', couleur='white',
          police="Arial", taille=16)

    rectangle(largeur_aire / 2 - 180, hauteur_aire / 2, largeur_aire / 2 + 180, hauteur_aire / 2 + 40,
              remplissage='orange', tag='choix_obstacles')
    texte(largeur_aire / 2, hauteur_aire / 2 + 20, "Intermédiaire", ancrage='center', tag='choix_obstacles',
          couleur='white', police="Arial", taille=16)

    rectangle(largeur_aire / 2 - 180, hauteur_aire / 2 + 40, largeur_aire / 2 + 180, hauteur_aire / 2 + 80,
              remplissage='salmon', tag='choix_obstacles')
    texte(largeur_aire / 2, hauteur_aire / 2 + 60, "Difficile", ancrage='center', tag='choix_obstacles',
          couleur='white', police="Arial", taille=16)

    mise_a_jour()
    switch_obs = False
    while switch_obs == False:
        x = attente_clic()
        if x[0] >= largeur_aire / 2 - 180 and x[0] <= largeur_aire / 2 + 180 and x[1] >= hauteur_aire / 2 - 40 and x[
                1] <= hauteur_aire / 2:  # Choix du niveau Facile
            switch_obs = True
            efface('choix_obstacles')
            mise_a_jour()
            return '1'

        elif x[0] >= largeur_aire / 2 - 180 and x[0] <= largeur_aire / 2 + 180 and x[1] >= hauteur_aire / 2 and x[
                1] <= hauteur_aire / 2 + 40:  # Choix du niveau Intermédiaire
            switch_obs = True
            efface('choix_obstacles')
            mise_a_jour()
            return '2'

        elif x[0] >= largeur_aire / 2 - 180 and x[0] <= largeur_aire / 2 + 180 and x[1] >= hauteur_aire / 2 + 40 and x[
                1] <= hauteur_aire / 2 + 80:  # Choix du niveau Difficile
            switch_obs = True
            efface('choix_obstacles')
            mise_a_jour()
            return '3'


def variante_score(lst_J1, lst_J2):
    """Permet d'afficher les scores au cours de la partie, quand l'un des joueur appuie sur la touche 's' de son clavier
    Prend en paramètres les listes des coordonnées des boules des joueurs"""
    liste_aires = scores(lst_J1, lst_J2)
    rec_var_sco = rectangle((largeur * (1000 / 1200)), (hauteur * (300 / 800)),
                            (largeur * (1150 / 1200)), hauteur / 2, remplissage="gray40", couleur="gray40")
    score_j1 = texte((largeur * (1025 / 1200)), (hauteur * (350 / 800)), int(
        ((liste_aires[0]) * 100) / 640_000), ancrage='w', tag='infos', couleur=lst_couleurs_joueurs[0], police="Arial",
        taille=defaut)
    score_j2 = texte((largeur * (1100 / 1200)), (hauteur * (350 / 800)), int(
        ((liste_aires[1]) * 100) / 640_000), ancrage='w', tag='infos', couleur=lst_couleurs_joueurs[1], police="Arial",
        taille=defaut)
    mise_a_jour()
    sleep(2)
    efface(score_j1)
    efface(score_j2)
    efface(rec_var_sco)
    mise_a_jour()


def variante_budget(budgetJ1, budgetJ2):
    """Permet d'afficher le budget relatif à chaque joueur
    Prend en paramètres le budget de chaque joueur"""
    rectangle((largeur * (1025 / 1200)), (hauteur * (425 / 800)), largeur,
              (hauteur * (475 / 800)), remplissage="gray40", couleur="gray40")
    texte((largeur * (1025 / 1200)), (hauteur * (450 / 800)), budgetJ1, ancrage='w',
          couleur=lst_couleurs_joueurs[0], police="Arial", taille=defaut)
    texte((largeur * (1100 / 1200)), (hauteur * (450 / 800)), budgetJ2, ancrage='w',
          couleur=lst_couleurs_joueurs[1], police="Arial", taille=defaut)


def demande_tailledesboules(budgetJ1, budgetJ2, lst_J1, lst_J2):
    """Fonction qui demande le rayon que l'utilisateur souhaite mettre
    Prend en paramètres le budget de chaque joueur, les listes des coordonnées des boules des joueurs
    Renvoie le rayon choisi par l'utilisateur"""
    rectangle((largeur_aire * (250 / 1200)), hauteur_aire / 3, (largeur_aire * (950 / 1200)),
              (hauteur_aire * (550 / 800)), remplissage='white smoke', tag='tailledesboules')
    texte((largeur_aire / 2), (hauteur_aire * (320 / 800)), "Quel rayon voulez vous donner?",
          taille=biggie, ancrage='center', tag='tailledesboules', police="Arial")
    entree = ('', '')
    nombre = ''
    while entree[1] != "Return":
        # L'utilisateur doit appuyer sur entrée pour valider
        entree = attente_clic_ou_touche()
        if entree[2] == 'Touche':
            if entree[1] in "0123456789":  # vérifie si l'entrée est un chiffre
                nombre += entree[1]  # ajoute l'entrée au nombre total
            # supprime la derniere entree si on appuie sur BackSpace
            elif entree[1] == 'BackSpace':
                if nombre != '':
                    nombre = nombre[:-1]
            efface('texteboule')
            texte((largeur_aire / 2), hauteur_aire * (420 / 800), nombre, taille=biggie,
                  ancrage='center', tag='tailledesboules texteboule', police="Arial")
            mise_a_jour()
        else:
            # si le joueur clique sur le bouton quitter
            if entree[0] >= (largeur * (850 / 1200)) and entree[0] <= (largeur * (1150 / 1200)) and entree[1] >= (
                    hauteur * (690 / 800)) and entree[1] <= (hauteur * (750 / 800)):
                quitter()
            # si le joueur clique sur le bouton pause
            elif entree[0] >= (largeur * (850 / 1200)) and entree[0] <= (largeur * (1150 / 1200)) and entree[1] >= (
                    hauteur * (610 / 800)) and entree[1] <= (hauteur * (670 / 800)):
                pause(budgetJ1, budgetJ2, lst_J1, lst_J2)
    efface('tailledesboules')
    if nombre != '':
        nombre = int(nombre)
    return nombre


def tailledesboules(budget, budgetJ1, budgetJ2, lst_J1, lst_J2):
    """Permet de récupérer la valeur du rayon demandé et de la comparer au budget
    Prend en paramètre le budget du joueur, le budget de chaque joueur en général, les listes des coordonnées des boules des joueurs
    Renvoie le rayon choisi par le joueur"""
    while True:
        rayon = demande_tailledesboules(budgetJ1, budgetJ2, lst_J1, lst_J2)
        while rayon == '' or rayon == 0:  # vérifie si l'utilisateur a rentré un nombre
            rayon = demande_tailledesboules(budgetJ1, budgetJ2, lst_J1, lst_J2)
        if budget - rayon < 0:  # Si le rayon est supérieur au budget, le jeu redemande à saisir un rayon
            rectangle((largeur_aire * (200 / 800)), hauteur_aire / 3, (largeur_aire * (600 / 800)),
                      hauteur_aire * ((1600 / 3) / 800), remplissage='white smoke', tag='tailledesboules')
            texte((largeur_aire * (400 / 800)), hauteur_aire * (400 / 800), "Budget insuffisant !",
                  taille=biggie, ancrage='center', tag='tailledesboules', police="Arial")
            mise_a_jour()
            sleep(1)
            efface('tailledesboules')
            mise_a_jour()
        else:
            return rayon  # retourne le rayon entré


def dynamique(lstJ1, lstJ2, liste_cercles_J1, liste_cercles_J2):
    """Permet d'incrémenter le rayon de chaque boule à chaque tour
    Prend en paramètres les listes des coordonnées des cercles des joueurs et la liste de leurs cercles
    Renvoie les listes des cercles des joueurs"""
    global increment
    listeJ1temp = list(lstJ1)  # garde les valeurs de J1 avant la modification
    efface('cercle')  # efface tous les cercles
    liste_cercles_J1 = verifier_dynamique(
        lstJ1, lstJ2, lst_couleurs_joueurs[0])
    liste_cercles_J2 = verifier_dynamique(
        lstJ2, listeJ1temp, lst_couleurs_joueurs[1])
    mise_a_jour()
    return liste_cercles_J1, liste_cercles_J2


def verifier_dynamique(lst_joueur, lst_ennemi, couleur):
    """Vérifier les élements qui entourent les cercles du joueur pour les incrémenter selon la distance les séparant
    Prend en paramètres la listes du joueur, celle de l'ennemi et la couleur du joueur
    Retourne la liste des cercles du joueur"""
    liste_cercle_joueur = []  # liste temporaire pour retenir les nouvelles valeurs des boules
    for cercle_joueur in lst_joueur:
        # parcourt les cerlces pour les incrémenter
        a_rajoutermin = increment  # initialiser le minimum à rajouter
        a_rajouter = increment  # savoir de combien le cercle va grandir

        # verifier la distance à rajouter pour chaque possibilité
        a_rajoutermin = verifier_increment_cercle(
            cercle_joueur, lst_ennemi, a_rajoutermin, a_rajouter)
        a_rajoutermin = verifier_increment_aire(
            cercle_joueur, a_rajouter, a_rajoutermin)
        a_rajoutermin = verifier_increment_obstacles(
            cercle_joueur, a_rajouter, a_rajoutermin)

        liste_cercle_joueur.append(cercle(
            cercle_joueur[0], cercle_joueur[1], cercle_joueur[2] + a_rajoutermin, remplissage=couleur, tag='cercle'))
        cercle_joueur[2] += a_rajoutermin  # actualise la liste des rayons

    return liste_cercle_joueur


def verifier_increment_cercle(cercle_joueur, lst_ennemi, a_rajoutermin, a_rajouter):
    """Vérifier si le cercle touche d'autres cercles
    Prend en paramètres le cercle du joueur, la liste ennemie, ce qui doit être rajouté, et la valeur temporaire qui doit etre ajoutée
    Revnoie le minimum à rajouter"""
    for cercles_ennemi in lst_ennemi:
        # déterminer la distance séparant le centre des cercles
        distance_cercles = sqrt(
            (cercle_joueur[0] - cercles_ennemi[0]) ** 2 + (cercle_joueur[1] - cercles_ennemi[1]) ** 2)
        if distance_cercles <= (cercle_joueur[2] + cercles_ennemi[2] + 2 * increment):
            # vérifier si la distance entre les cercles sera toujours inférieure au rayon avec l'incrément
            # rajouter ce qu'il reste de distance
            a_rajouter = (distance_cercles -
                          cercle_joueur[2] - cercles_ennemi[2]) / 2

        if a_rajouter < a_rajoutermin:
            a_rajoutermin = a_rajouter  # actualise la distance min à rajouter

    return a_rajoutermin


def verifier_increment_aire(cercle_joueur, a_rajouter, a_rajoutermin):
    """Vérifier la distance entre le cercle et les bords de l'aire de jeu
    Prend en paramètres le cercle du joueur, la valeur temporaire qui doit etre ajoutée, ce qui doit être rajouté et l'increment
    Renvoie le minimum à rajouter"""
    # vérifie quel côté de l'aire est proche du cercle
    if cercle_joueur[0] <= cercle_joueur[2] + increment:
        # rajoute la distance séparant le bord du cercle au bord de l'aire
        a_rajouter = (cercle_joueur[0] - cercle_joueur[2]) // 2
    elif cercle_joueur[0] >= largeur_aire - (cercle_joueur[2] + increment):
        a_rajouter = (largeur_aire - cercle_joueur[2] - cercle_joueur[0]) // 2

    if a_rajouter < a_rajoutermin:
        a_rajoutermin = a_rajouter

    if cercle_joueur[1] <= cercle_joueur[2] + increment:
        a_rajouter = (cercle_joueur[1] - cercle_joueur[2]) // 2
    elif cercle_joueur[1] >= hauteur_aire - (cercle_joueur[2] + increment):
        a_rajouter = (hauteur_aire - cercle_joueur[2] - cercle_joueur[1]) // 2

    if a_rajouter < a_rajoutermin:
        a_rajoutermin = a_rajouter
    return a_rajoutermin


def verifier_increment_obstacles(cercle_joueur, a_rajouter, a_rajoutermin):
    """Vérifier la distance entre le cercle et les obstacles
    Prend en paramètres le cercle du joueur, la valeur temporaire qui doit etre ajoutée et ce qui doit être rajouté
    Renvoie le minimum à rajouter"""
    # global increment
    global liste_obstacles
    for element in liste_obstacles:
        # vérifier si les obstacles et les cercles s'intersecteront
        # calcule la distance entre la boule et les obstacles
        if element[0] == 'c':
            distance_obstacles = sqrt(
                (cercle_joueur[0] - element[2]) ** 2 + (cercle_joueur[1] - element[3]) ** 2)
            if distance_obstacles <= (cercle_joueur[2] + element[1] + increment):
                a_rajouter = distance_obstacles - cercle_joueur[2] - element[1]
        elif element[0] == 'r':
            rx1, ry1, rx2, ry2 = min(element[1], element[3]), min(
                element[2], element[4]), max(element[1], element[3]), max(element[2], element[4])
            # On récupère les coins supérieurs gauche (rx1, ry1) et inférieur droit (rx2, ry2)
            dx = max(rx1 - cercle_joueur[0], 0, cercle_joueur[
                0] - rx2)  # On calcule la distance entre le cercle et les bords du rectangle sur l'axe des x
            dy = max(ry1 - cercle_joueur[1], 0, cercle_joueur[
                1] - ry2)  # On calcule la distance entre le cercle et les bords du rectangle sur l'axe des y
            if sqrt(dx ** 2 + dy ** 2) <= increment + cercle_joueur[2]:
                # Si la distance entre le bord des 2 formes est inférieure à l'incrément
                # Le cercle augmente de cette distance
                a_rajouter = sqrt(dx ** 2 + dy ** 2) - cercle_joueur[2]

    if a_rajouter < a_rajoutermin:
        a_rajoutermin = a_rajouter
    return a_rajoutermin


# SCORES
def scores(lst_J1, lst_J2):
    """Permet de calculer les scores
    Prend en paramètres les listes des coordonnées des boules des joueurs
    Renvoie la liste contenant le score de chaque joueur"""
    pixels_J1 = []
    pixels_J2 = []
    for element in lst_J1:
        # Coordonnées des pixels contenus dans les boules du joueur 1
        centre_x = int(element[0])
        centre_y = int(element[1])
        rayon = int(element[2])
        for x in range(centre_x - rayon, centre_x + rayon + 1):
            for y in range(centre_y - rayon, centre_y + rayon + 1):
                if (x - centre_x) ** 2 + (y - centre_y) ** 2 <= rayon ** 2:
                    pixels_J1.append((x, y))

    for element in lst_J2:
        # Coordonnées des pixels contenus dans les boules du joueur 2
        centre_x = int(element[0])
        centre_y = int(element[1])
        rayon = int(element[2])
        for x in range(centre_x - rayon, centre_x + rayon + 1):
            for y in range(centre_y - rayon, centre_y + rayon + 1):
                if (x - centre_x) ** 2 + (y - centre_y) ** 2 <= rayon ** 2:
                    pixels_J2.append((x, y))

    # score des joueurs correspondant au nombre de pixels (sans doublons) de leurs boules
    score_J1 = len(set(pixels_J1))
    score_J2 = len(set(pixels_J2))
    return [score_J1, score_J2]


# ECRAN DE VICTOIRE
def victoire(lst_J1, lst_J2):
    """Permet d'afficher le gagnant lorsque le nombre de tours est écoulé pour chacun des joueurs
    Prend en paramètres les listes des coordonnées des boules des joueurs"""
    efface_tout()
    rectangle(0, 0, largeur, hauteur, remplissage='grey20', tag='victoire')

    # Création du bouton permettant à l'utilisateur de rejouer au jeu si il le souhaite
    rectangle((largeur * (200 / 1200)), (hauteur * (350 / 800)), (largeur * (400 / 1200)),
              (hauteur * (450 / 800)), tag='victoire', couleur='PaleGreen3', remplissage='PaleGreen3')
    texte(largeur / 4, hauteur / 2, "REJOUER", ancrage='center',
          tag='victoire', couleur='white', police="Arial", taille=defaut)

    # Création du bouton permettant à l'utilisateur de quitter le jeu si il ne souhaite pas rejouer
    rectangle((largeur * (800 / 1200)), (hauteur * (350 / 800)), (largeur * (1000 / 1200)),
              (hauteur * (450 / 800)), tag='victoire', couleur='salmon', remplissage='salmon')
    texte((largeur * (900 / 1200)), hauteur / 2, "QUITTER", ancrage='center',
          tag='victoire', couleur='white', police="Arial", taille=defaut)

    liste_aires = scores(lst_J1, lst_J2)

    if liste_aires[0] > liste_aires[1]:
        # Affichage du gagnant dans la couleur choisit au début. Ajout d'une image illustrant cette victoire
        texte(largeur / 2, (hauteur * (650 / 800)), 'LE JOUEUR 1 EST VAINQUEUR',
              couleur=lst_couleurs_joueurs[0], ancrage='center', taille=bbb, tag='victoire', police="Arial")
        image(largeur / 2, (hauteur * (200 / 800)),
              os.path.join(os.path.dirname(__file__), 'victory_lol.png'), ancrage='center')
    elif liste_aires[0] < liste_aires[1]:
        texte(largeur / 2, (hauteur * (650 / 800)), 'LE JOUEUR 2 EST VAINQUEUR',
              couleur=lst_couleurs_joueurs[1], ancrage='center', taille=bbb, tag='victoire', police="Arial")
        image(largeur / 2, (hauteur * (200 / 800)),
              os.path.join(os.path.dirname(__file__), 'victory_lol.png'), ancrage='center')
    else:
        # Affichage du message d'egalité. Ajout d'une image illustrant la défaite des 2 joueurs
        texte(largeur / 2, (hauteur * (650 / 800)), 'EGALITE', couleur='black',
              ancrage='center', taille=bbb, tag='victoire', police="Arial")
        image(largeur / 2, (hauteur * (200 / 800)),
              os.path.join(os.path.dirname(__file__), 'game_over.png'), ancrage='center')

    mise_a_jour()

    x = (0, 0)

    # Si le joueur appuie sur le bouton rejouer on retourne à l'écran d'accueil
    while not (x[0] >= ((largeur * (200 / 1200))) and x[0] <= ((largeur * (400 / 1200))) and x[1] >= (
        (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800)))) or not (
            x[0] >= ((largeur * (800 / 1200))) and x[0] <= ((largeur * (1000 / 1200))) and x[1] >= (
                (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800)))):
        x = attente_clic()
        # s'il clique sur rejouer on retourne à l'écran d'accueil
        if x[0] >= ((largeur * (200 / 1200))) and x[0] <= ((largeur * (400 / 1200))) and x[1] >= (
                (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800))):
            efface_tout()
            menu_principal()
            return
        # s'il clique sur quitter on quitte le jeu
        elif x[0] >= ((largeur * (800 / 1200))) and x[0] <= ((largeur * (1000 / 1200))) and x[1] >= (
                (hauteur * (350 / 800))) and x[1] <= ((hauteur * (450 / 800))):
            quitter()
        continue


def supp_save():
    """Fonction permettant de supprimer la sauvegarde"""
    efface_tout()
    rectangle(0, 0, largeur, hauteur, remplissage='grey20', tag='supp')

    rectangle(largeur / 3, (hauteur * (300 / 800)), (largeur * (800 / 1200)),
              (hauteur * (500 / 800)), remplissage='white smoke', tag='supp')
    texte(largeur / 2, (hauteur * (325 / 800)), "Voulez-vous supprimer",
          taille=biggie, ancrage='center', tag='supp', police="Arial")
    texte(largeur / 2, (hauteur * (355 / 800)), "la sauvegarde ?",
          taille=biggie, ancrage='center', tag='supp', police="Arial")

    rectangle((largeur * (450 / 1200)), (hauteur * (425 / 800)), (largeur * (550 / 1200)),
              (hauteur * (475 / 800)), remplissage='PaleGreen3', tag='supp')
    texte((largeur * (500 / 1200)), (hauteur * (450 / 800)), "Oui", ancrage='center',
          tag='supp', couleur='white', police="Arial", taille=biggie)

    rectangle((largeur * (650 / 1200)), (hauteur * (425 / 800)), (largeur *
                                                                  (750 / 1200)), (hauteur * (475 / 800)),
              remplissage='salmon', tag='supp')
    texte((largeur * (700 / 1200)), (hauteur * (450 / 800)), "Non", ancrage='center',
          tag='supp', couleur='white', police="Arial", taille=biggie)

    mise_a_jour()

    switch = False
    while switch == False:
        x = attente_clic()
        # s'il clique sur oui, on supprime le fichier de sauvegarde
        if x[0] >= (largeur * (450 / 1200)) and x[0] <= (largeur * (550 / 1200)) and x[1] >= (hauteur * (425 / 800)) and \
                x[1] <= (hauteur * (475 / 800)):
            switch = True
            if os.path.exists(nom_save):
                os.remove(nom_save)
        # s'il clique sur non, on affiche directement l'écran de victoire
        elif x[0] >= (largeur * (650 / 1200)) and x[0] <= (largeur * (750 / 1200)) and x[1] >= (
                hauteur * (425 / 800)) and x[1] <= (hauteur * (475 / 800)):
            switch = True
    efface_tout()


# QUITTER


def quitter():
    """Fonction qui demande à l'utilisateur s'il est sûr de vouloir quitter le jeu.
    Permet de quitter le jeu ou de changer d'avis et de rester sur l'interface de jeu"""

    # demander à l'utilisateur s'il est sûr de vouloir quitter le jeu
    rectangle(largeur / 3, (hauteur * (300 / 800)), (largeur * (800 / 1200)),
              (hauteur * (500 / 800)), remplissage='white smoke', tag='quitter')
    texte(largeur / 2, (hauteur * (350 / 800)), "Voulez-vous vraiment quitter ?",
          taille=biggie, ancrage='center', tag='quitter', police="Arial")

    rectangle((largeur * (450 / 1200)), (hauteur * (425 / 800)), (largeur * (550 / 1200)),
              (hauteur * (475 / 800)), remplissage='PaleGreen3', tag='quitter')
    texte((largeur * (500 / 1200)), (hauteur * (450 / 800)), "Oui", ancrage='center',
          tag='quitter', couleur='white', police="Arial", taille=biggie)

    rectangle((largeur * (650 / 1200)), (hauteur * (425 / 800)), (largeur * (750 / 1200)),
              (hauteur * (475 / 800)), remplissage='salmon', tag='quitter')
    texte((largeur * (700 / 1200)), (hauteur * (450 / 800)), "Non", ancrage='center',
          tag='quitter', couleur='white', police="Arial", taille=biggie)

    mise_a_jour()

    switch = False
    while switch == False:
        x = attente_clic()

        # Si l'utilisateur souhaite réellement quitter, on affiche une fenêtre signifiant que le jeu est terminé
        if x[0] >= (largeur * (450 / 1200)) and x[0] <= (largeur * (550 / 1200)) and x[1] >= (hauteur * (425 / 800)) and \
                x[1] <= (hauteur * (475 / 800)):
            switch = True
            efface_tout()
            rectangle(0, 0, largeur, hauteur, remplissage='grey35')

            liste_couleurs_possibles = [
                'SkyBlue2', 'PaleGreen1', 'salmon', 'MediumPurple1', 'khaki', 'tan1']
            r = (largeur * (50 / 1200))
            x = 2 * r + r
            for _ in range(10):
                cercle(x, (hauteur * (100 / 800)), r,
                       remplissage=liste_couleurs_possibles[randint(0, 5)])
                cercle(x, (hauteur * (700 / 800)), r,
                       remplissage=liste_couleurs_possibles[randint(0, 5)])
                x += 2 * r
            ligne((largeur * (200 / 1200)), (hauteur * (300 / 800)),
                  (largeur * (1000 / 1200)), (hauteur * (300 / 800)), epaisseur=3)
            texte(largeur / 2, hauteur / 2, "Merci d'avoir joué ! Au revoir, et à bientôt !",
                  police='Verdana', ancrage='center', taille=loelia)
            ligne((largeur * (200 / 1200)), (hauteur * (500 / 800)),
                  (largeur * (1000 / 1200)), (hauteur * (500 / 800)), epaisseur=3)

            mise_a_jour()
            sleep(3)
            exit()

        # Si le joueur ne souhaite pas réellement quitter le jeu, on revient à l'écran
        elif x[0] >= (largeur * (650 / 1200)) and x[0] <= (largeur * (750 / 1200)) and x[1] >= (
                hauteur * (425 / 800)) and x[1] <= (hauteur * (475 / 800)):
            switch = True
            efface('quitter')
            mise_a_jour()

# PAUSE


def pause(budgetJ1, budgetJ2, lst_J1, lst_J2):
    """Fonction qui demande à l'utilisateur s'il est sûr de vouloir quitter et sauvegarder le jeu.
    Permet de quitter le jeu et de sauvegarder ou de changer d'avis et de rester sur l'interface de jeu
    Prend en paramètres le budget des joueurs et la liste des joueurs"""
    # demander à l'utilisateur s'il est sûr de vouloir quitter et sauvegarder le jeu
    rectangle(largeur / 3, (hauteur * (300 / 800)), (largeur * (800 / 1200)),
              (hauteur * (500 / 800)), remplissage='white smoke', tag='pause')
    texte(largeur / 2, (hauteur * (350 / 800)), "Voulez-vous quitter et sauvegarder ?",
          taille=biggie, ancrage='center', tag='pause', police="Arial")

    rectangle((largeur * (450 / 1200)), (hauteur * (425 / 800)), (largeur * (550 / 1200)),
              (hauteur * (475 / 800)), remplissage='PaleGreen3', tag='pause')
    texte((largeur * (500 / 1200)), (hauteur * (450 / 800)), "Oui", ancrage='center',
          tag='pause', couleur='white', police="Arial", taille=biggie)

    rectangle((largeur * (650 / 1200)), (hauteur * (425 / 800)), (largeur * (750 / 1200)),
              (hauteur * (475 / 800)), remplissage='salmon', tag='pause')
    texte((largeur * (700 / 1200)), (hauteur * (450 / 800)), "Non", ancrage='center',
          tag='pause', couleur='white', police="Arial", taille=biggie)

    mise_a_jour()

    switch = False
    while switch == False:
        x = attente_clic()

        # Si l'utilisateur souhaite réellement quitter et sauvegarder, on appelle la fonction de sauvegarder affiche une fenêtre signifiant que le jeu est terminé
        if x[0] >= (largeur * (450 / 1200)) and x[0] <= (largeur * (550 / 1200)) and x[1] >= (hauteur * (425 / 800)) and \
                x[1] <= (hauteur * (475 / 800)):
            switch = True

            nom_fichier = formatage_nom_fichier()
            creation_fichier(nom_fichier, budgetJ1, budgetJ2, lst_J1, lst_J2)

            efface_tout()
            rectangle(0, 0, largeur, hauteur, remplissage='grey35')

            r = (largeur * (50 / 1200))
            x = 2 * r + r
            for _ in range(10):
                cercle(x, (hauteur * (100 / 800)), r,
                       remplissage=lst_couleurs[randint(0, 5)])
                cercle(x, (hauteur * (700 / 800)), r,
                       remplissage=lst_couleurs[randint(0, 5)])
                x += 2 * r
            ligne((largeur * (200 / 1200)), (hauteur * (300 / 800)),
                  (largeur * (1000 / 1200)), (hauteur * (300 / 800)), epaisseur=3)
            texte(largeur / 2, hauteur / 2, "Merci d'avoir joué ! Au revoir, et à bientôt !",
                  police='Verdana', ancrage='center', taille=loelia)
            ligne((largeur * (200 / 1200)), (hauteur * (500 / 800)),
                  (largeur * (1000 / 1200)), (hauteur * (500 / 800)), epaisseur=3)

            mise_a_jour()
            sleep(3)
            exit()

        # Si le joueur ne souhaite pas réellement quitter le jeu, on revient à l'écran
        elif x[0] >= (largeur * (650 / 1200)) and x[0] <= (largeur * (750 / 1200)) and x[1] >= (
                hauteur * (425 / 800)) and x[1] <= (hauteur * (475 / 800)):
            switch = True
            efface('pause')
            mise_a_jour()


def formatage_nom_fichier():
    """Fonction qui permet de formater le nom du fichier de sauvegarde au format "save_YYYY-MM-DD_HH-MM-SS.txt"
    Renvoie le nom du fichier"""
    nom_fichier = 'save_' + str(datetime.now())
    nom_fichier = nom_fichier.replace(" ", "_")
    nom_fichier = nom_fichier.replace(":", "-")
    nom_fichier = nom_fichier.replace(".", "-")
    nom_fichier = nom_fichier + '.txt'
    return nom_fichier


def creation_fichier(nom_fichier, budgetJ1, budgetJ2, lst_J1, lst_J2):
    """Fonction qui permet de créer le fichier de sauvegarde
    Prend en paramètres le nom du fichier, le budget des joueurs et les listes des joueurs
    Renvoie le fichier de sauvegarde"""
    with open((nom_fichier), 'w') as sauvegarde:
        sauvegarde.writelines(
            ["largeur=" + str(largeur) + "\n", "hauteur=" + str(hauteur) + "\n",
             "largeur_aire=" + str(largeur_aire) +
             "\n", "hauteur_aire=" + str(hauteur_aire) + "\n",
             "nb_tour=" + str(nb_tour) + "\n", "rayon=" + str(rayon) +
             "\n", "budgetJ1=" + str(budgetJ1) + "\n",
             "budgetJ2=" + str(
                 budgetJ2) + "\n", "si_ter=" + str(si_ter) + "\n", "increment=" + str(increment) + "\n",
             "temps_tour=" + str(temps_tour) + "\n",
             "lst_couleurs_joueurs=" +
             str(lst_couleurs_joueurs) + "\n", "liste_variantes=" +
             str(liste_variantes) + "\n",
             "lst_J1=" + str(lst_J1) + "\n", "lst_J2=" + str(lst_J2) + "\n",
             "liste_obstacles=" + str(liste_obstacles) + "\n"]
        )
    return nom_fichier

# FONCTION PRINCIPALE


def jouer():
    """Fonction qui permet de lancer le jeu
    Appelle choix_couleur() si on joue ou dico_transition_global() si on charge une partie
    Appelle supp_save() si on termine une partie chargée"""
    if charger == False:
        choix_couleur()
    else:
        dico_transition_global()
    interface_jeu()
    lst_J1, lst_J2 = jeu()
    if charger == True:
        supp_save()
    victoire(lst_J1, lst_J2)


if __name__ == '__main__':
    recuperation_parametres()
    affectation_parametres()
    if si_para == 0:
        cree_fenetre(largeur, hauteur)
        menu_principal()
