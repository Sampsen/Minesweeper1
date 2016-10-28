# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 13:40:39 2016

@author: Sampsen
"""

# Minesweeper V 0.1

from random import random
import copy
import sys

alphabet = "0abcdefghijklmnopqrstuvwxyz"
alphabet = list(alphabet)

def playerinput():
    print("")
    print("Welcome to my minesweeper game, preprealpha")
    print("")
    print("Flag a bomb: 'bomb'")
    print("Make a guess: 'guess'")
    print("Exit: 'exit'")
    rows = int(input("How many rows and columns would you like?  "))
    def bombchoice():    
        bombs = int(input("How many bombs would you like?  "))
        if bombs >= rows ** 2:
            return rows ** 2 - 1
        else:
            return bombs
    gamearea(rows, bombchoice())
        
def gamearea(rows, bombs):
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
    print("")
    guess(rows, bombs, playarea)
 
def randombombs(rows, bombs, playarea, columnguess, rowguess, firstturn):
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
        for row in playarea:
            print(" ".join(row))
        return playareacopy
        
    letsplay(rows, playarea, setplayarea(playareacopy), rowguess, columnguess, firstturn)
        
#def changemode(rows, playarea, playareacopy):
#    pass

def guess(rows, bombs, playarea, playareacopy = [], firstturn = True):
    winning(playarea, playareacopy)
    for row in playarea:
        print(" ".join(row))    
    print("Find tiles with no bombs.")    
    columnguess = input("Guess a column:  ").lower()
    if columnguess == "bomb":
        bombflag(rows, playarea, playareacopy)
    if columnguess == 'exit':
        sys.exit()
    alphabetindex = 0    
    for letter in alphabet:
        if columnguess == letter:
            columnguess = alphabetindex
        alphabetindex += 1
    try:    
        rowguess = int(input("Guess a row:  "))
    except ValueError:
        print("")
        print("Please enter A to " + str(alphabet[rows].upper()) + " for column.")
        print("Please enter a whole number, 1 to " + str(rows ) + " for rows.")
        print("")
        return guess(rows, bombs, playarea, playareacopy, firstturn)
    if 1 > columnguess or columnguess > rows or 1 > rowguess or rowguess > rows:
        print("That's outside the gamearea, choose again.")
        print(" ")
        return guess(rows, bombs, playarea, playareacopy, firstturn)
    if firstturn == True:
        firstturn = False
        randombombs(rows, bombs, playarea, columnguess, rowguess, firstturn)
    else:
        letsplay(rows, playarea, playareacopy, rowguess, columnguess, firstturn)

def bombflag(rows, playarea, playareacopy):
    winning(playarea, playareacopy)
    bombs = 0
    print(" ")
    for row in playarea:
        print(" ".join(row))
    print("Flag a bomb.")
    columnguess = input("Guess a column:  ").lower()
    if columnguess == "guess":
        guess(rows, bombs, playarea, playareacopy)
    if columnguess == 'exit':
        sys.exit()
    alphabetindex = 0    
    for letter in alphabet:
        if columnguess == letter:
            columnguess = alphabetindex
        alphabetindex += 1
    rowguess = int(input("Guess a row:  "))
    if 1 > columnguess or columnguess > rows or 1 > rowguess or rowguess > rows:
        print("That's outside the gamearea, choose again.")
        return bombflag(rows, playarea, playareacopy)
    else:
        playarea[rowguess][columnguess] = "b"
        bombflag(rows, playarea, playareacopy)
    
#def makeaguess(rows, playarea, playareacopy):
#    winning(playarea, playareacopy)
#    for row in playarea:
#        print(" ".join(row))    
#    print("Find tiles with no bombs")    
#    columnguess = input("Guess a column:  ").lower()
#    
#    alphabetindex = 0    
#    for letter in alphabet:
#        if columnguess == letter:
#            columnguess = alphabetindex
#        alphabetindex += 1
#    rowguess = int(input("Guess a row:  "))
#    if 1 > columnguess or columnguess > rows or 1 > rowguess or rowguess > rows:
#        print("That's outside the gamearea, choose again.")
#        print(" ")
#        makeaguess(rows, playarea, playareacopy)
#    else:
#        letsplay(rows, playarea, playareacopy, rowguess, columnguess)
                    
def letsplay(rows, playarea, playareacopy, rowguess, columnguess, firstturn):    
    print("")
    bombs = 0
    if playareacopy[rowguess][columnguess] == "b":
        again = input("You hit a bomb, game over.  Want to play again?  Y/N:  ").lower()
        if again == "y" or again == "yes":
            playerinput()
        else:
            print("Thanks for playing.")
            sys.exit()
    elif playareacopy[rowguess][columnguess] == "0":
        revealon0(rowguess, columnguess, playarea, playareacopy)
        for number in range((len(playarea) - 2)):
            cascadeon0(rowguess, columnguess, playarea, playareacopy)
        guess(rows, bombs, playarea, playareacopy, firstturn)
    else:
        playarea[rowguess][columnguess] = playareacopy[rowguess][columnguess]
        guess(rows, bombs, playarea, playareacopy, firstturn)
            
def revealon0(rowguess, columnguess, playarea, playareacopy):
    #reveals all tiles around the guessed tile when there are no bombs touching it
    for column in range(columnguess - 1, columnguess + 2):
        for row in range(rowguess - 1, rowguess +2):
            playarea[row][column] = playareacopy[row][column]
#    playarea[rowguess - 1][columnguess - 1] = playareacopy[rowguess - 1][columnguess - 1]
#    playarea[rowguess - 1][columnguess] = playareacopy[rowguess - 1][columnguess]
#    playarea[rowguess - 1][columnguess + 1] = playareacopy[rowguess - 1][columnguess + 1]
#    playarea[rowguess][columnguess - 1] = playareacopy[rowguess][columnguess - 1]
#    playarea[rowguess][columnguess] = playareacopy[rowguess][columnguess]
#    playarea[rowguess][columnguess + 1] = playareacopy[rowguess][columnguess + 1]
#    playarea[rowguess + 1][columnguess - 1] = playareacopy[rowguess + 1][columnguess - 1]
#    playarea[rowguess + 1][columnguess] = playareacopy[rowguess + 1][columnguess]
#    playarea[rowguess + 1][columnguess + 1] = playareacopy[rowguess + 1][columnguess + 1]

     
def cascadeon0(rowguess, columnguess, playarea, playareacopy):
    #clean up empty areas of the game board when one empty tile is selected 
    #iterates on every square on the board        
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
 
               
#Create function that creates board after first guess, will allow user to not lose on first click

def winning(playarea, playareacopy):
    if playarea == playareacopy:
        for row in playarea:
            print(" ".join(row))
        again = input("You win!  Want to play again?  Y/N:  ").lower()
        if again == 'y' or again == 'yes':
            playerinput()
        else:
            print("Thanks for playing.")
            sys.exit()
                             
               
    
playerinput()

#for pos, x in enumerate(y):
#    print("pos {} = {}".format(pos, x))

#Errors to clean up:
#    DONE - Nonetype on failed bomb creation
#    non integer entries on all inputs
#    guesses outside of gameboard range