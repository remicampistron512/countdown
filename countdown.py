#!/usr/bin/env python
# -*- coding: utf-8 -*-
NUMBERS_POOL = tuple(range(1, 11)) * 2 + (25, 50, 75, 100)
import random
import operator as op

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

def start_game():
    """
    Démarre la partie, initialise les nombres utilisables ainsi que le nombre cible, puis les affiche.
    Lance alors une boucle infinie pour accomplir chaque tour de jeu
    :return:
    """
    drawn_numbers = random.choices(NUMBERS_POOL,k=6)
    initial_number = random.randrange(101, 999)
    display_numbers(initial_number, drawn_numbers,True)
    while len(drawn_numbers)>0:
        next_turn(drawn_numbers, initial_number)



def next_turn(drawn_numbers, initial_number: int):
    """
    Enclenche un tour de jeu, on demande à chaque fois l'opérateur ainsi que les deux nombres utilisés dans le calcul.
    Chaque fois qu'un nombre est choisi, on le retire de la liste des nombres disponibles, et on y ajoute le résultat.
    :param drawn_numbers:
    :param initial_number:
    :return:
    """
    operator = ask_operator("Choisissez un opérateur  (+,-,* ou /)")
    first_number_result = ask_number("Merci de choisir un premier nombre dans la liste : ", drawn_numbers)
    display_numbers(initial_number, drawn_numbers)
    second_number_result = ask_number("Merci de choisir le deuxième nombre dans la liste : ", first_number_result[1])
    result = calculate_and_print(first_number_result[0], second_number_result[0], operator)
    second_number_result[1].append(result)
    display_numbers(initial_number, second_number_result[1])

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
            if int(input_number) in drawn_numbers:
                drawn_numbers.remove(input_number)
                return input_number,drawn_numbers
        else:
            print("Merci de rentrer un entier positif")
        print("Merci de choisir un nombre de la liste")


if __name__ == '__main__':
    start_game()