# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 13:40:39 2016

@author: Sampsen
"""

# Minesweeper V 0.9

from random import random
import copy
import sys
import string

alphabet = "0" + string.ascii_lowercase

def playerinput():
    # player input that will be used to create gameboard    
    try:
        rows = int(input("How many rows and columns would you like? (Max 25) "))
        if rows > 25:
            print("Maximum rows is 25.")
            return playerinput()
        bombs = int(input("How many bombs would you like?  "))
        # if player wants more bombs than game tiles, function returns 1 less bomb than amount of tiles        
        if bombs >= rows ** 2:
            bombs = rows ** 2 - 1
        return rows,bombs
    except ValueError:
        print("Please enter whole numbers.")
        return playerinput()        
        
def gamearea(rows, bombs):
    # creates generic playarea based on input
    playarea = []
    columnindex = 0
    rowindex = 0
    for x in range(2 + rows):
        playarea.append(["?"] * (2 + rows))
        while columnindex < len(playarea):
            for column in playarea[0]:
                playarea[0][columnindex] = alphabet[columnindex].upper()
            columnindex += 1
            if (2 + rows) == columnindex:
                playarea[0][columnindex - 1] = " "
        while rowindex < len(playarea):
            for row in playarea:
                if rowindex < 10:
                    playarea[rowindex][0] = "0" + str(rowindex)
                else:
                    playarea[rowindex][0] = str(rowindex)
                playarea[rowindex][rows + 1] = " "
            rowindex += 1
            if (2 + rows) == rowindex:
                playarea[rowindex-1] = [" "] * (2 + rows)       
        playarea[0][0] = "  "
    print()
    return playarea
 
def randombombs(rows, bombs, playarea, columnguess, rowguess):
    # creates a copy of the generic gameboard that has bombs
    playareacopy = copy.deepcopy(playarea)
    bombchance = bombs / (rows ** 2)
    while bombs > 0:
        rowindex = 1
        while rowindex < len(playareacopy) - 1:
            columnindex = 1
            while columnindex < len(playareacopy) - 1:                 
                bombchance2 = random()
                if bombs < 1:
                    break
                if rowindex == rowguess and columnindex == columnguess:
                    columnindex += 1
                if bombchance >= bombchance2 and playareacopy[rowindex][columnindex] != "b":                  
                    playareacopy[rowindex][columnindex] = "b"
                    bombs -= 1
                columnindex += 1
            rowindex += 1
    
    def setplayarea(playareacopy):
        rowindex = 1
        while rowindex < len(playareacopy):
            bnumber = 0
            columnindex = 1
            while columnindex < len(playareacopy):
                if playareacopy[rowindex][columnindex] == "?":
                    for square in range(rowindex - 1, rowindex + 2):
                        for circle in range(columnindex - 1, columnindex + 2):
                            if playareacopy[square][circle] == "b":
                                bnumber += 1
                    playareacopy[rowindex][columnindex] = str(bnumber)
                    bnumber = 0
                columnindex += 1
            rowindex += 1
        return playareacopy
        
    return setplayarea(playareacopy)

def print_game_board(playarea):
    for row in playarea:
        print(" ".join(row))
        
def tile_guess(rows, guess):
    try:
        columnguess = input("Guess a column:  ").lower()
        if columnguess == "guess":
            guess = True
            return 0, 0
        if columnguess == "bomb":
            guess = False
            return 0, 0
        if columnguess == 'exit':
            sys.exit()    
        if columnguess not in alphabet:
            print("Please enter A to {} for column.".format(alphabet[rows].upper()))
            return tile_guess(rows, guess)
        for a, x in enumerate(alphabet):
            if columnguess == x:
                columnguess = int(a)
        rowguess = int(input("Guess a row:  "))
        if 1 > columnguess or columnguess > rows or 1 > rowguess or rowguess > rows:
            print("That's outside the gamearea, choose again.\n")
            return tile_guess(rows, guess)
        return columnguess, rowguess
    except ValueError:
        print("\nPlease enter a whole number, 1 to {} for rows.\n".format(rows))
        return tile_guess(rows, guess)
                       
def letsplay(playarea, playareacopy, rowguess, columnguess):    
    print()
    if playarea[rowguess][columnguess] == "b":
        print("You've marked this tile as a bomb, please choose a different tile")
    elif playareacopy[rowguess][columnguess] == "b":
        print_game_board(playareacopy)
        again = input("You hit a bomb, game over.  Want to play again?  Y/N:  ").lower()
        return play_again(again)
    elif playareacopy[rowguess][columnguess] == "0":
        revealon0(rowguess, columnguess, playarea, playareacopy)
        for number in range((len(playarea) - 2)):
            cascadeon0(rowguess, columnguess, playarea, playareacopy)
    else:
        playarea[rowguess][columnguess] = playareacopy[rowguess][columnguess]
        return 0
            
def revealon0(rowguess, columnguess, playarea, playareacopy):
    # reveals all tiles around the guessed tile when there are no bombs touching it
    for column in range(columnguess - 1, columnguess + 2):
        for row in range(rowguess - 1, rowguess +2):
            if playareacopy != "b":
                playarea[row][column] = playareacopy[row][column]
     
def cascadeon0(rowguess, columnguess, playarea, playareacopy):
    # clean up empty areas of the game board when one empty tile is selected 
    # iterates on every square on the board        
    rowindex = 1
    while rowindex < len(playarea) - 2:
        for row in playarea:
            columnindex = 1
            for column in row:
                if playarea[rowindex][columnindex] == "0":
                    revealon0(rowindex, columnindex, playarea, playareacopy)
                if columnindex < len(playarea) - 2:
                    columnindex += 1
            if rowindex < len(playarea) - 2:
                rowindex += 1

def play_again(response):
    if response in ("y","yes"):
        return 1
    else:
        print("Thanks for playing.")
        return 2
        
def winning(playarea, playareacopy, keepplaying):
    # currently evaluates if every tile has been revealed or flagged
    # TO DO - change victory condition to be either all bombs flagged or all non bomb tiles revealed
    if playarea == playareacopy:
        print_game_board(playarea)
        again = input("\nYou win!  Want to play again?  Y/N:  ").lower()
        return play_again(again)
    else:
        return keepplaying

while True:                             
    print("\nWelcome to my minesweeper game, alpha V0.9\n")
    print("Flag a bomb: 'bomb'")
    print("Make a guess: 'guess'")
    print("Exit: 'exit'")
    rows, bombs = playerinput()
    playarea = gamearea(rows, bombs)
    print_game_board(playarea)
    print("\nFind tiles with no bombs.")
    guess = True
    columnguess, rowguess = tile_guess(rows, guess)
    playareacopy = randombombs(rows, bombs, playarea, columnguess, rowguess)
    letsplay(playarea, playareacopy, rowguess, columnguess)
    keepplaying = 0
    while True:
        if keepplaying > 0:
            break
        print_game_board(playarea)
        if guess:            
            print("Find tiles with no bombs.")
            columnguess, rowguess = tile_guess(rows, guess)
            if columnguess > 0:
                keepplaying = letsplay(playarea, playareacopy, rowguess, columnguess)
            else:
                guess = False
        else:
            print("Flag or unflag a bomb.")
            columnguess, rowguess = tile_guess(rows, guess)
            if columnguess > 0:
                if playarea[rowguess][columnguess] == "?":
                    playarea[rowguess][columnguess] = "b"
                elif playarea[rowguess][columnguess] == "b":
                    playarea[rowguess][columnguess] = "?"
                else:
                    print("That tile is already revealed")
            else:
                guess = True
        keepplaying = winning(playarea, playareacopy, keepplaying)
    if keepplaying > 1:
        break
  
    
#for pos, x in enumerate(y):
#    print("pos {} = {}".format(pos, x))

#Errors to clean up:
#    DONE - Nonetype on failed bomb creation
#    DONE? - non integer entries on all inputs
#    DONE - guesses outside of gameboard range