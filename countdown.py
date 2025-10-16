#!/usr/bin/env python
# -*- coding: utf-8 -*-
NUMBERS_POOL = tuple(range(1, 11)) * 2 + (25, 50, 75, 100)
import random


def display_first_numbers(initial_number, drawn_numbers):
    print ("Voici le premier coup de chiffres")
    print (initial_number,end=" | ")
    print (*drawn_numbers)


def ask_operator(prompt):
    while True:
        operator = input(prompt)
        if operator == "+" or operator == "/" or operator == "*" or operator == "-":
            return operator
        else:
            print("Merci de rentrer +,-,* ou /")



def start_game():
    drawn_numbers = random.choices(NUMBERS_POOL,k=6)
    initial_number = random.randrange(101, 999)
    display_first_numbers(initial_number,drawn_numbers)
    ask_operator("Choisissez un opérateur  (+,-,* ou /)")
    ask_for_two_numbers("Merci de choisir deux nombre dans la liste",drawn_numbers)

def ask_for_two_numbers(prompt,drawn_numbers):
    while True:
        txt = input(prompt)
        parts = txt.replace(",", " ").split()
        print (parts)
        print(f"Valeur invalide. Entrez un chiffre compris dans la liste.")

    
    
    
    
def init_game(param):
    start_game()
    





if __name__ == '__main__':
    init_game(True)