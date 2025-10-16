#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import operator as op
import copy

#La liste des nombres disponibles
NUMBERS_POOL = tuple(range(1, 11)) * 2 + (25, 50, 75, 100)

#Un dictionnaire des opérateurs et leur correspondance
OPERATORS = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.floordiv,  # floor division
}

def display_numbers(initial_number, drawn_numbers,start=False):
    """
    Affiche les nombres disponibles pour effectuer des calculs

    :param initial_number: Nombre à trouver
    :param drawn_numbers: liste de nombres disponible pour accomplir le calcul
    :param start:
    :return:
    """
    if start: print ("Voici le premier coup de chiffres")
    print (initial_number,end=" | ")
    # Affiche les nombres de facon linéaire sans les crochets
    print (*drawn_numbers)


def ask_operator(prompt):
    """
    Demande l'opérateur à l'utilisateur
    :param prompt:
    :return:
    """
    while True:
        operator = input(prompt)
        if operator == "+" or operator == "/" or operator == "*" or operator == "-":
            return operator
        else:
            print("Merci de rentrer +,-,* ou /")


def calculate_and_print(a, b, sign):
    """
    Calcule et affiche l'opération en utilisant la librairie operator
    :param a:
    :param b:
    :param sign:
    :return:
    """
    if sign not in OPERATORS:
        print(f"Unknown operator: {sign}")
        return False
    try:
        result = OPERATORS[sign](a, b)
        print(f"{a} {sign} {b} = {result}")
        return  result
    except ZeroDivisionError:
        print("Error: division by zero")


def ask_to_continue(prompt):
    while True:
        decision = input(prompt)
        if decision == "continuer" or decision == "c":
            return True
        elif decision == "proposer" or decision == "p":
            return False
        print("merci d'entrer un terme valide (proposer | continuer)")


def solve_countdown(drawn_numbers, target_number):
    """
    Solveur du jeu automatique, basé sur dfs(depth first search).
    On enregistre les combinaisons explorées dans un dictionnaire.

    :param drawn_numbers:
    :param target_number:
    :return:
    """



    #la solution est dans les chiffres proposés
    if target_number in drawn_numbers:
        return target_number
    else:

        tested_pairs= dict(operation=str,pair=tuple)
        drawn_numbers_list = list()
        calculate_multiplication(0,drawn_numbers)


def calculate_multiplication(left_shift,drawn_numbers):
    for i, number in enumerate(drawn_numbers):
        for k, number2 in enumerate(drawn_numbers):
            if k < len(drawn_numbers) - 1:
                print(f"{drawn_numbers[i + left_shift]} x {drawn_numbers[k + 1]} = {number * drawn_numbers[k + 1]}")
                if k == len(drawn_numbers):
                    calculate_multiplication(i,drawn_numbers)



def start_game(solve=False):
    """
    Démarre la partie, initialise les nombres utilisables ainsi que le nombre cible, puis les affiche.
    Lance alors une boucle infinie pour accomplir chaque tour de jeu
    :return:
    """

    drawn_numbers = random.choices(NUMBERS_POOL,k=6)
    target_number = random.randrange(101, 999)
    display_numbers(target_number, drawn_numbers, True)
    if not solve:
        while len(drawn_numbers)>0:
            results = next_turn(drawn_numbers, target_number)
            if target_number in results:
                print ("le compte est bon")
                break
            if not ask_to_continue("Voulez vous \"continuer\" ou \"proposer\" un nombre"):
                proposed_number = ask_number("proposer un nombre de la liste",results)
                break
    else:
        solve_countdown(drawn_numbers,target_number)



def next_turn(drawn_numbers, target_number: int):
    """
    Enclenche un tour de jeu, on demande à chaque fois l'opérateur ainsi que les deux nombres utilisés dans le calcul.
    Chaque fois qu'un nombre est choisi, on le retire de la liste des nombres disponibles, et on y ajoute le résultat.
    :param drawn_numbers:
    :param target_number:
    :return:
    """
    operator = ask_operator("Choisissez un opérateur  (+,-,* ou /) : ")
    first_number_result = ask_number("Merci de choisir un premier nombre dans la liste : ", drawn_numbers)
    display_numbers(target_number, drawn_numbers)
    second_number_result = ask_number("Merci de choisir le deuxième nombre dans la liste : ", first_number_result[1])
    result = calculate_and_print(first_number_result[0], second_number_result[0], operator)
    second_number_result[1].append(result)
    display_numbers(target_number, second_number_result[1])
    return second_number_result[1]

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
            if input_number in drawn_numbers:
                drawn_numbers.remove(input_number)
                return input_number,drawn_numbers
        else:
            print("Merci de rentrer un entier positif")
        print("Merci de choisir un nombre de la liste")


if __name__ == '__main__':
    start_game(True)