#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import operator as op

# La liste des nombres disponibles
NUMBERS_POOL = tuple(range(1, 11)) * 2 + (25, 50, 75, 100)

# Un dictionnaire des opérateurs et leur correspondance
OPERATORS = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.floordiv,  # floor division
}
VALID_OPS = ('+','-','/','*')

# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions utilitaires ----------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

def display_numbers(initial_number, drawn_numbers, start=False):
    """
    Affiche les nombres disponibles pour effectuer des calculs

    :param initial_number: Nombre à trouver
    :param drawn_numbers: liste de nombres disponible pour accomplir le calcul
    :param start:
    :return:
    """
    if start: print("Voici le premier coup de chiffres")
    print(initial_number, end=" | ")
    # Affiche les nombres de facon linéaire sans les crochets
    print(*drawn_numbers)


def calculate_and_print(a, b, sign):
    """
    Calcule et affiche l'opération en utilisant la librairie operator
    :param a:
    :param b:
    :param sign:
    :return:
    """
    if sign not in OPERATORS:
        print(f"Operateur inconnu: {sign}")
        return False
    try:
        result = OPERATORS[sign](a, b)
        print(f"{a} {sign} {b} = {result}")
        return result
    except ZeroDivisionError:
        print("Erreur: division par zéro")


def compute_score(drawn_numbers, target_number, proposition=False):
    """
    Donne un score basé sur la distance entre les deux numéros proposés
    :param drawn_numbers:
    :param target_number:
    :param proposition:
    :return:
    """
    if not proposition:
        if len(drawn_numbers) > 1:
            for number in drawn_numbers:
                proposition = number
    else:
        proposition = drawn_numbers

    score = abs(proposition - target_number)
    return score


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions de contrôles d'entrées utilisateur  ----------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


def ask_number(prompt, drawn_numbers):
    """
    Demande un nombre parmi la liste des nombres disponibles
    :param prompt:
    :param drawn_numbers:
    :return:
    """
    while True:
        input_number = input(prompt).strip()
        if input_number.isdigit():
            input_number = int(input_number)
            # on enlève le chiffre entré de la liste
            if input_number in drawn_numbers:
                return input_number, drawn_numbers
        else:
            print("Merci de rentrer un entier positif")
        print("Merci de choisir un nombre de la liste")



def ask_operation(prompt,drawn_numbers):
    """
    Demande une opération binaire (ex. `25+50') et la découpe.

    :param prompt:
    :param drawn_numbers:
    :return:
    """
    while True:
        candidate_op = ""
        operation = input(prompt)
        operation = operation.replace(" ","")
        if any(operators in operation for operators in VALID_OPS) :
            for operator in VALID_OPS:
                if operator in operation:
                    candidate_op = operator
            left,right = operation.split(candidate_op,1)
            if int(left) in drawn_numbers and int(right) in drawn_numbers:
                return int(left),int(right),candidate_op
            else:
                print("rentrez un entier de la liste")
        else:
            print("rentrez un opérateur valide (*,+,-,/)")


def ask_to_continue(prompt):
    """
    Propose à l'utilisateur de continuer la partie ou bien de proposer un nombre
    :param prompt:
    :return:
    """
    while True:
        decision = input(prompt)
        if decision == "continuer" or decision == "c":
            return True
        elif decision == "proposer" or decision == "p":
            return False
        print("merci d'entrer un terme valide (proposer | continuer) : ")


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions principales de jeu   -------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


def start_game(solve=False):
    """
    Démarre la partie, initialise les nombres utilisables ainsi que le nombre cible, puis les affiche.
    Lance alors une boucle infinie pour accomplir chaque tour de jeu
    :return:
    """

    drawn_numbers = random.choices(NUMBERS_POOL, k=6)
    target_number = random.randrange(101, 999)
    display_numbers(target_number, drawn_numbers, True)
    if not solve:
        # Tant que la liste a plus d'un nombre, on continue le jeu
        while len(drawn_numbers) > 1:
            results = next_turn(drawn_numbers)
            display_numbers(target_number, drawn_numbers, False)
            # le nombre cible est dans la liste des nombres trouvés
            if target_number in results:
                print("le compte est bon")
                break
            # après un tour, on demande à l'utilisateur de proposer un nombre ou de continuer
            if not ask_to_continue("Voulez vous \"continuer\" ou \"proposer\" un nombre"):
                proposed_number, results = ask_number("proposer un nombre de la liste", results)
                print(f"votre proposition est {proposed_number}")
                print("votre score est : " + str(compute_score(proposed_number, target_number, True)))
                break
        else:

            print(f"votre proposition est {drawn_numbers}")
            print("votre score est : " + str(compute_score(drawn_numbers, target_number)))
    else:
        solve_countdown(drawn_numbers, target_number)


def next_turn(drawn_numbers):
    """
    Exécute un tour : demande une opération, calcule le résultat, met à jour la liste de nombres.
    :param drawn_numbers:
    :return:
    """
    first_number,second_number,operator = ask_operation("Rentrer votre calcul : ",drawn_numbers)

    result = calculate_and_print(first_number, second_number, operator)
    drawn_numbers.remove(first_number)
    drawn_numbers.remove(second_number)
    drawn_numbers.append(result)
    return drawn_numbers


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Solveur ------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

def solve_countdown(drawn_numbers, target_number):
    """
    Solveur du jeu automatique, basé sur dfs(depth first search).
    On enregistre les combinaisons explorées dans un dictionnaire.

    :param drawn_numbers:
    :param target_number:
    :return:
    """

    # la solution est dans les chiffres proposés
    if target_number in drawn_numbers:
        return target_number
    else:
        return False


def calculate(drawn_numbers, expression):
    for i in range(len(drawn_numbers)):
        for j in range(len(drawn_numbers)):
            if j < len(drawn_numbers) - 1:
                remaining = []
                for k in range(len(drawn_numbers)):
                    if k != i and k != j:
                        remaining.append(drawn_numbers[k])
                print("remaining ")
                print(remaining)
                """print(f"{drawn_numbers[i + left_shift]} x {drawn_numbers[j + 1]} = {drawn_numbers[i] * drawn_numbers[j + 1]}")
                print(f"{drawn_numbers[i + left_shift]} + {drawn_numbers[j + 1]} = {drawn_numbers[i] + drawn_numbers[j + 1]}")
                print(f"{drawn_numbers[i + left_shift]} - {drawn_numbers[j + 1]} = {drawn_numbers[i] - drawn_numbers[j + 1]}")
                print(f"{drawn_numbers[i + left_shift]} / {drawn_numbers[j + 1]} = {drawn_numbers[i] / drawn_numbers[j + 1]}")"""
                calculate(remaining + [drawn_numbers[i] - drawn_numbers[j]], f"({expression[i]} / {expression[j]})")


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions d'initialisation -----------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    start_game(False)
