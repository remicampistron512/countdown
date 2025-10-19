#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import operator as op
from copy import deepcopy

# La liste des nombres disponibles
NUMBERS_POOL = tuple(range(1, 11)) * 2 + (25, 50, 75, 100)

# Un dictionnaire des opérateurs et leur correspondance
OPERATORS = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.floordiv,  # floor division
}
VALID_OPS = ('+', '-', '/', '*')

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


def ask_operation(prompt, drawn_numbers):
    """
    Demande une opération binaire (ex. `25+50') et la découpe.

    :param prompt:
    :param drawn_numbers:
    :return:
    """
    while True:
        candidate_op = ""
        operation = input(prompt)
        operation = operation.replace(" ", "")
        if any(operators in operation for operators in VALID_OPS):
            for operator in VALID_OPS:
                if operator in operation:
                    candidate_op = operator
            left, right = operation.split(candidate_op, 1)
            if int(left) in drawn_numbers and int(right) in drawn_numbers:
                return int(left), int(right), candidate_op
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

        res = solve_countdown(drawn_numbers, target_number, True)

        if isinstance(res, dict):
            print("Le compte est bon !")
            for s in res["steps"]:
                print(f"{s['expr']}")
        elif res[0]:
            print("Pas de solution trouvée, le plus proche est : ")
            print (res[0]["résultat"])


def next_turn(drawn_numbers):
    """
    Exécute un tour : demande une opération, calcule le résultat, met à jour la liste de nombres.
    :param drawn_numbers:
    :return:
    """
    first_number, second_number, operator = ask_operation("Rentrer votre calcul : ", drawn_numbers)

    result = calculate_and_print(first_number, second_number, operator)
    drawn_numbers.remove(first_number)
    drawn_numbers.remove(second_number)
    drawn_numbers.append(result)
    return drawn_numbers


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Solveur ------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


def solve_countdown(drawn_numbers, target_number, collect_steps=False):
    """
    Solveur du jeu automatique, basé sur dfs(depth first search).
    On enregistre les combinaisons explorées dans un dictionnaire.

    :param collect_steps:
    :param drawn_numbers:
    :param target_number:
    :return:
    """

    # créé un set pour enregistrer les nombres obtenus, cela permet de ne pas recalculer les mêmes combinaisons
    seen_states = set()

    # enregistre les calculs précédents
    steps = []

    score_board = []

    def add_to_score_board(result,target):
        score = compute_score(result, target, True)
        entry = {"résultat": result, "score": score}

        # Si vide ou inférieur au dernier le moins elevé
        if not score_board or score < score_board[0]["score"]:
            score_board[:] = [entry]
        return entry





    def replace_numbers(left_number_idx, right_number_idx, result, numbers):
        """
        Remplace les nombres utilisés dans le calcul précédent
        :param left_number_idx:
        :param right_number_idx:
        :param result:
        :param numbers:
        :return:
        """
        # vérifications basiques
        if left_number_idx == right_number_idx:
            raise ValueError("left_number_idx et right_number_idx doivent être différents")

        if left_number_idx < 0 or left_number_idx >= len(numbers):
            raise IndexError("left_number_idx out of range")
        if right_number_idx < 0 or right_number_idx >= len(numbers):
            raise IndexError("right_number_idx out of range")

        # Créé une nouvelle liste qui enregistre les nombres sauf les indices choisis
        new_numbers = []
        i = 0
        while i < len(numbers):
            if i != left_number_idx and i != right_number_idx:
                new_numbers.append(numbers[i])
            i += 1

        # Ajoute à la liste le résultat de l'opération
        new_numbers.append(result)
        return new_numbers

    def is_calculation_legal(right_number, left_number):
        """
        Le calcul doit être possible, pas de résultat négatif
        :param right_number:
        :param left_number:
        :return:
        """
        return (right_number - left_number) >= 0

    def reorder(numbers):
        """
        Créé un tuple d'ordre croissant permettant de comparer avec le résultat précédent
        :param numbers:
        :return:
        """
        return tuple(sorted(numbers))



    def track_step(depth_level, operator_used, left_value, right_value, result_value,
                   numbers_before, numbers_after):
        """
        Permet d'enregistrer les différentes étapes qui ont mené au résultat dans un dictionnaire
        :param depth_level:
        :param operator_used:
        :param left_value:
        :param right_value:
        :param result_value:
        :param numbers_before:
        :param numbers_after:
        :return:
        """
        # On ne désire pas obtenir les calculs
        if not collect_steps:
            return
        # copies pour éviter les alias
        before_copy = deepcopy(numbers_before)
        after_copy = deepcopy(numbers_after)
        steps.append({
            "depth": depth_level,
            "operator": operator_used,
            "left": left_value,
            "right": right_value,
            "result": result_value,
            "before_numbers": before_copy,
            "after_numbers": after_copy,
            "expr": f"({left_value} {operator_used} {right_value}) = {result_value}",
        })

    def calculate(numbers, target, depth=0):
        """

        :param numbers: la liste des nombres disponibles pour le calcul
        :param target: le résultat à atteindre
        :param depth: profondeur du calcul
        :return:
        """

        if len(numbers) <= 0:
            print("toutes les combinaisons ont été explorées")
            return False



        # On compare la liste des nombres avec les nombres vus précédemment
        current_numbers = reorder(numbers)
        if current_numbers in seen_states:
            return False
        seen_states.add(current_numbers)

        # On teste chaque paire (i, j).
        i = 0
        while i < len(numbers) - 1:
            j = i + 1
            while j < len(numbers):
                right_number = numbers[i]
                left_number = numbers[j]

                right_number_idx = i
                left_number_idx = j

                # ============== ADDITION ==============
                addition_result = OPERATORS["+"](right_number, left_number)
                add_to_score_board(addition_result, target)
                new_numbers = replace_numbers(left_number_idx, right_number_idx, addition_result, numbers)
                if collect_steps:
                    track_step(depth, '+', left_number, right_number, addition_result, numbers, new_numbers)
                if addition_result == target or calculate(new_numbers, target, depth + 1):
                    return True
                if collect_steps:
                    steps.pop()  # retire le résultat enregistré le plus haut dans la pile

                # ============ MULTIPLICATION ===========
                multiplication_result = OPERATORS["*"](right_number, left_number)
                add_to_score_board(multiplication_result, target)
                new_numbers = replace_numbers(left_number_idx, right_number_idx, multiplication_result, numbers)
                if collect_steps:
                    track_step(depth, '*', left_number, right_number, multiplication_result, numbers,
                               new_numbers)
                if multiplication_result == target or calculate(new_numbers, target, depth + 1):
                    return True
                if collect_steps:
                    steps.pop()
                # =============== DIVISION ==============
                # left / right si exact
                if right_number != 0 and left_number % right_number == 0:
                    division_result = OPERATORS["/"](left_number, right_number)
                    add_to_score_board(division_result, target)
                    new_numbers = replace_numbers(left_number_idx, right_number_idx, division_result, numbers)
                    if collect_steps:
                        track_step(depth, '/', left_number, right_number, division_result, numbers, new_numbers)
                    if division_result == target or calculate(new_numbers, target, depth + 1):
                        return True
                    if collect_steps:
                        steps.pop()

                # right / left si exact
                if left_number != 0 and right_number % left_number == 0:
                    division_result = OPERATORS["/"](right_number, left_number)
                    add_to_score_board(division_result, target)
                    new_numbers = replace_numbers(left_number_idx, right_number_idx, division_result, numbers)
                    if collect_steps:
                        track_step(depth, '/', right_number, left_number, division_result, numbers, new_numbers)
                    if division_result == target or calculate(new_numbers, target, depth + 1):
                        return True
                    if collect_steps:
                        steps.pop()

                # ============ SOUSTRACTION =============
                # right - left (>= 0)
                if is_calculation_legal(right_number, left_number):
                    substraction_result = OPERATORS["-"](right_number, left_number)
                    add_to_score_board(substraction_result, target)
                    new_numbers = replace_numbers(left_number_idx, right_number_idx, substraction_result,
                                                  numbers)
                    if collect_steps:
                        track_step(depth, '-', right_number, left_number, substraction_result, numbers,
                                   new_numbers)
                    if substraction_result == target or calculate(new_numbers, target, depth + 1):
                        return True
                    if collect_steps:
                        steps.pop()

                # left - right (>= 0)
                if is_calculation_legal(left_number, right_number):
                    substraction_result2 = OPERATORS["-"](left_number, right_number)
                    add_to_score_board(substraction_result2, target)
                    new_numbers = replace_numbers(left_number_idx, right_number_idx, substraction_result2,
                                                  numbers)
                    if collect_steps:
                        track_step(depth, '-', left_number, right_number, substraction_result2, numbers,
                                   new_numbers)
                    if substraction_result2 == target or calculate(new_numbers, target, depth + 1):
                        return True
                    if collect_steps:
                        steps.pop()

                j += 1
            i += 1

        return False


    # la solution est dans les chiffres proposés
    if target_number in drawn_numbers:
        if collect_steps:
            return {"Le compte est bon !": target_number, "steps": steps}
        return target_number
    else:
    # on lance le solveur
        found = calculate(drawn_numbers, target_number, depth=0)

    if collect_steps:
        if found:
            return {"result": target_number, "steps": steps}
        else:
            return score_board

    return target_number if found else score_board


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions d'initialisation -----------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    start_game(True)
