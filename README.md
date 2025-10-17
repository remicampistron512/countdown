# Le compte est bon

Ce programme permet de jouer à l'épreuve de la celèbre émission des chiffres et des lettres.

## Table des matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Règles du jeu](#règles-du-jeu)
- [Fonctionnalités](#fonctionnalités)
- [Structure du code](#structure-du-code)

## Installation

1. Assurez-vous d’avoir **Python 3** installé sur votre machine.
2. Téléchargez le fichier `countdown.py` dans un répertoire de votre choix.
3. Ouvrez un terminal et exécutez le script : `countdown.py`

## Règles du jeu

Le but de cette épreuve est d'obtenir un nombre (de 101 à 999) à partir d'opérations élémentaires 
(Addition "+", Soustraction "−", Multiplication "*", Division "/") sur des entiers naturels,
en partant de nombres tirés au hasard (de 1 à 10, 25, 50, 75 et 100).
Le jeu comporte vingt-quatre plaques : les nombres de 1 à 10 présents en double exemplaire 
et les nombres 25, 50, 75 et 100 présents en un seul exemplaire. Sont alors tirées six valeurs.  
À défaut de trouver le compte exact, il faut tenter de s'en approcher le plus près possible.

## Fonctionnalités

Le programme offre la possibilité à chaque tour de proposer un nombre si le compte n'est pas bon.
Lors de la proposition d'un nombre un score est attribué au joueur et la partie s'arrête.
À venir : Le programme permet de résoudre le jeu automatiquement.

## Structure du code

### `display_numbers(initial_number, drawn_numbers, start=False)`  
 Affiche les nombres disponibles pour effectuer des calculs

### `calculate_and_print(a, b, sign)`
Calcule et affiche l'opération en utilisant la librairie operator
### `compute_score(drawn_numbers, target_number, proposition=False)`
Donne un score basé sur la distance entre les deux numéros proposés
### `ask_number(prompt, drawn_numbers)`
Demande un nombre parmi la liste des nombres disponibles
### `ask_operation(prompt, drawn_numbers)`
Demande une **opération binaire** (ex. `25+50`) et la découpe.
 
### `ask_to_continue(prompt)`
Propose à l'utilisateur de continuer la partie ou bien de proposer un nombre
### `start_game(solve=False)`
Démarre la partie, initialise les nombres utilisables ainsi que le nombre cible, puis les affiche.
Lance alors une boucle infinie pour accomplir chaque tour de jeu
### `next_turn(drawn_numbers, target_number)`
Exécute un tour : demande une opération, calcule le résultat, met à jour la liste de nombres.
