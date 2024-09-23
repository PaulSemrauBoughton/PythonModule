# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:20:37 2023

@author: paulb
"""
"""
MATH20621 - Coursework 3
Student name: Paul Semrau-Boughton
Student id:   10855624
Student mail: paul.semrau-boughton@student.manchester.ac.uk

Do not change any part of this string except to replace
the <tags> with your name, id and university email address.
"""

def request_location(question_str):
    """
    Prompt the user for a board location, and return that location.
    
    Takes a string parameter, which is displayed to the user as a prompt.
    
    Raises InputError if input is not a valid integer, 
    or RuntimeError if the location typed is not in the valid range.
    
    *************************************************************
    DO NOT change this function in any way
    You MUST use this function for ALL user input in your program
    *************************************************************
    """
    loc = int(input(question_str))
    if loc<0 or loc>=24:
        raise RuntimeError("Not a valid location")
    return loc


def draw_board(g):
    """
    Display the board corresponding to the board state g to console.
    Also displays the numbering for each point on the board, and the
    number of counters left in each players hand, if any.
    A reference to remind players of the number of each point is also displayed.
    
    You may use this function in your program to display the board
    to the user, but you may also use your own similar function, or
    improve this one, to customise the display of the game as you choose
    """
    def colored(r, g, b, text):
        """
        Spyder supports coloured text! This function creates coloured
        version of the text 'text' that can be printed to the console.
        The colour is specified with red (r), green (g), blue (b) components,
        each of which has a range 0-255.
        """
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def piece_char(i):
        """
        Return the (coloured) character corresponding to player i's counter,
        or a + to indicate an unoccupied point
        """
        if i==0:
            return colored(100,100,100,'+')
        elif i==1:
            return colored(255,60,60,'X')
        elif i==2:
            return colored(60,120,255,'O')

        
    board = '''
x--------x--------x  0--------1--------2 
|        |        |  |        |        |
|  x-----x-----x  |  |  3-----4-----5  |
|  |     |     |  |  |  |     |     |  |
|  |  x--x--x  |  |  |  |  6--7--8  |  |
|  |  |     |  |  |  |  |  |     |  |  |
x--x--x     x--x--x  9-10-11    12-13-14
|  |  |     |  |  |  |  |  |     |  |  |
|  |  x--x--x  |  |  |  | 15-16-17  |  |
|  |     |     |  |  |  |     |     |  |
|  x-----x-----x  |  |  18---19----20  |
|        |        |  |        |        |
x--------x--------x  21------22-------23
'''    
    boardstr = ''
    i = 0
    for c in board:
        if c=='x':
            boardstr += piece_char(g[0][i])
            i += 1
        else:
            boardstr += colored(100,100,100,c)
    if g[1]>0 or g[2]>0:
        boardstr += '\nPlayer 1: ' + (piece_char(1)*g[1])
        boardstr += '\nPlayer 2: ' + (piece_char(2)*g[2])
    print(boardstr)
    
    
    
#############################    
# The functions for each task
    
def is_adjacent(i, j):
    """
    Checks if two points on the board are adjacent to each other.

    Parameters
    ----------
    i : integer
        i is a point on the board.
    j : integer
        j is point on the board.

    Returns
    -------
    boolean
        Returns True if points are adjacent or false if points are not adjacent.

    """
    
    try:    
        adjacent_dict = {0:[1,9],               #create dictionary of adjacent positions.
                         1:[0,2,4],
                         2:[1,14],
                         3:[4,10],
                         4:[1,3,5,7],
                         5:[4,13],
                         6:[7,11],
                         7:[4,6,8],
                         8:[7,12],
                         9:[0,10,21],
                         10:[3,9,11,18],
                         11:[6,10,15],
                         12:[8,13,17] ,
                         13:[5,12,14,20], 
                         14:[2,13,23], 
                         15:[11,16], 
                         16:[15,17,19], 
                         17:[12,16], 
                         18:[10,19],
                         19:[16,18,20,22],
                         20:[13,19],
                         21:[9,22],
                         22:[19,21,23],
                         23:[14,22]}
        if i in adjacent_dict[j] and j in adjacent_dict[i]:      #checks if i and j are both in eachothers dictionaries.
            return True
        else:
            return False
    except KeyError or NameError:
        return False
    
def new_game():
    """
    Starts a new game state, with an empty board and 9 counters
    for each player and player 1 being the active player.

    Returns
    -------
    list
        Returns the inital game state, g.

    """
    board=[0]*24                     #creates list for empty board.
    player1_counters=9
    player2_counters=9
    player_current=1
    return [board, player1_counters, player2_counters, player_current] #combines variables to return game state

def remaining_counters(g):
    """
    Determines the total number of counters the active player 
    has on the board and yet to place, from the game state.

    Parameters
    ----------
    g : list
        The game state.

    Returns
    -------
    total_counters : integer
        Total number of counters the active player has.

    """
    total_counters=g[g[3]]+g[0].count(g[3])     #counts the number of counters in hand and on the board belonging to the active player.
    return total_counters

def is_in_mill(g, i):
    """
    Determines if placing a counter at position i creates a
    mill (3 in a row) for the active player.

    Parameters
    ----------
    g : list
        The game state.
    i : integer
        Position on the board.

    Returns
    -------
    boolean
        Returns True if placing the counter at i creates a mill
        for the active player, False if it does not.

    """
    mills = [[0, 1, 2],                     #creates list of possible mills.
             [3, 4, 5],
             [6, 7, 8],
             [9, 10, 11],
             [12, 13, 14],
             [15, 16, 17],
             [18, 19, 20],
             [21, 22, 23],
             [0, 9, 21],
             [3, 10, 18],
             [6, 11, 15],
             [1, 4, 7],
             [16, 19, 22],
             [8, 12, 17],
             [5, 13, 20],
             [2, 14, 23]
             ]
    
    if i>23 or i<0:
        return -1
    if g[0][i]==0:
        return -1
    else:
        for mill in mills:
            if i in mill:
                lst = [index for index, e in enumerate(g[0]) if e == g[0][i]]   #create list with elements of g[0] that are equal to value of g[0][i].
                if all(x in lst for x in mill):   #checks if all elements in mill are present in the temporary list "lst"
                    return g[0][i]
            else:
                pass
        return 0
    

def player_can_move(g):
    """
    Checks if the active player can make a move, either by
    placing a counter or moving an already placed one.

    Parameters
    ----------
    g : list
        The game state.

    Returns
    -------
    boolean
        Returns True if they can make a move, False if they can not.

    """
    #checks if the player has any counters in hand that they can place first.
    if g[g[3]]>0:
        return True
    
    else:
        lst = [index for index, e in enumerate(g[0]) if e == g[3]]      #creates list of values in g[0] that are equal to g[3] (active player number)
        for counter in lst:
            for i in range (0,24):
                if is_adjacent(counter,i) and g[0][i]==0:               #checks that if for each counter of the players there is an adjacent empty space.
                    return True
                    break                     #returns true if there are any counters of the active player that can move.
                else:
                    pass
        return False
            
            
def place_counter(g, i):
    """
    Adjusts the game state, to place a counter at position i.

    Parameters
    ----------
    g : list
        The game state.
    i : integer
        Position on the board.

    Raises
    ------
    RuntimeError
        If there is already a counter at point the position i.

    Returns
    -------
    g : list
        The new game state, with a counter at position i.

    """
    if g[0][i]==0 and g[g[3]]>0:        #checks that i is empty and active player has counter to place.
        g[0][i]=g[3]
        g[g[3]]=g[g[3]]-1
        return g
    else:
        raise RuntimeError
    
        

def move_counter(g, i, j):
    """
    Adjusts the game state to move a counter from position i to j,
    for the current player.

    Parameters
    ----------
    g : list
        The game state.
    i : integer
        The initial position of the counter on the board.
    j : integer
        The target position of the counter on the board.

    Raises
    ------
    RuntimeError
        If the move is not possible, if i and j are not adjacent,
        if i does not contain counter of active player, or if there
        is already a counter at j.

    Returns
    -------
    g : list
        The new game state with the counter at position
        i moved to position j.

    """
    if player_can_move(g)==False:
        raise RuntimeError
    
    #checks that location j is empty, i and j are adjacent and that i is occupied by active players counter.
    if is_adjacent(i,j) and g[0][j]==0 and g[0][i]==g[3]:
        g[0][j]=g[0][i]
        g[0][i]=0
        return g
    else:
        raise RuntimeError
        
    pass

def remove_opponent_counter(g, i):
    """
    Adjusts the game state to remove the opponents counter from position i.

    Parameters
    ----------
    g : list
        The game state.
    i : integer
        Position of the opponents counter you want to remove.

    Raises
    ------
    RuntimeError
        If there is not an opponents counter at position i.

    Returns
    -------
    g : list
        The new game state with the opponents counter
        at position i removed.

    """
    if g[0][i]!=0 and g[0][i]!=g[3]:    #checks that i is not empty and is occupied by oppnents counter.
        g[0][i]=0
        return g
    else:
        raise RuntimeError

def turn(g):
    """
    Completes a turn for the active player, using previous functions allows 
    them to placeor remove a counter. If the counter they placed/moved 
    created a mill allows them to remove an opponents counter.

    Parameters
    ----------
    g : list
        The game state.

    Returns
    -------
    boolean
        Returns True if the turn was successful, or False if it is not.

    """
    #checks if the player can move or place a counter, if not the player is unable to make a turn.
    if player_can_move(g)==False or remaining_counters(g)<=2:
        return False
    
    if g[g[3]]>0:
        while True:
            try:
                #if the player has counters in hand, places it in inputted location if valid.
                location_target = request_location("Enter location: ")     
                place_counter(g,location_target)
                break
            except RuntimeError:
                print ("--invalid place--")
                pass
    else:
        while True:
            try:
                #if the player does not have counters in hand, moves a placed counter to inputted location if valid.
                location_source= request_location("Enter source location: ")
                location_target= request_location("Enter target location: ")
                move_counter(g,location_source,location_target)
                break
            except RuntimeError:
                print ("--invalid move--")
                pass
    
    #if the placed or removed counter forms a mill, removes one of the oponent's counter at inputted location if valid.
    if is_in_mill(g,location_target)==g[3]:
        draw_board(g)
        print ("--mill formed--")
        while True:
            location_remove= request_location("Enter remove location: ")
            if g[0][location_remove]!=0 and g[0][location_remove]!=g[3]:
                remove_opponent_counter(g, location_remove)
                break
            else:
                print ("--invalid remove--")
                pass
                
    g[3]=3-g[3]            #changes active player.
    return True
    
            


def save_state(g, filename):
    """
    Saves the current game state to a file called "my_file.txt".

    Parameters
    ----------
    g : list
        The game state.
    my_fiile.txt : txt
        The file the gamestate is saved to.

    Raises
    ------
    RuntimeError
        If there is an error when saving the game state to the file.

    """
    try:
        f= open(filename, "w")                     #opens the file to write.
        f.write(", ".join(map(str,g[0]))+"\n")     #writes the board witout brackets and commas.
        f.write(str(g[1])+"\n")                    #writes player 1's counters in hand on next line.     
        f.write(str(g[2])+"\n")                    #writes player 2's coutners in hand on next line.
        f.write(str(g[3])+"\n")                    #writes active player on next line.
        f.close()                                  #closes the file.
        
    except Exception:
        raise RuntimeError
    pass

def load_state(filename):
    """
    Loads the game state from the file called "my_file.txt",
    and makes it the active game state.

    Parameters
    ----------
    filename : txt
        The name of the text file where the game state is loaded from.

    Raises
    ------
    RuntimeError
        If there is an error loading the game state from the file.

    Returns
    -------
    list
        The loaded game state.

    """
    try:
        f=open(filename, "r")                                       #opens the file to read.
        board = list(map(int, f.readline().strip().split(",")))     #reads the board state, creates list "board" in format.
        player1_counters = int(f.readline().strip())                #reads the player1 counters, and creates integer "player1_counters".
        player2_counters = int(f.readline().strip())                #reads the player1 counters, and creates integer "player2_counters".
        player_current = int(f.readline().strip())                  #reads the active player counters.
        return [board, player1_counters, player2_counters, player_current] #combines all these variables, and returns the loaded game state in format used by other functions.
        
    except Exception:
        raise RuntimeError

def play_game():
    """
    Starts the game and loops turns, loading and saving the game 
    state each turn, until a winner is determined.
    Prints the winner at the end.


    """
    g=new_game()                        #starts new game.
    save_state(g,"my_file.txt")         #saves initial game state.
    while True:
        print ("________________________________________________")    #breaks up rounds to make game easier to follow.
        print ("Player",g[3],"'s go")
        load_state("my_file.txt")       #loads game state from initial/last turn.
        draw_board(g)
        try:
            if turn(g)==False:       #if turn is unsuccesful, while loop breaks and winner is declared.
                break
            else:
                save_state(g, "my_file.txt")  #if turn is successful, save the game state and proceed to next turn.
                pass
        except ValueError:    #if "enter" key is pressed allows turn to be repeated without crashing code.
            print ("--invalid input--")
            pass
    
    winner=3-g[3]      #winner is calculated.
    print ("🎉🎉Player",winner," wins!🎉🎉") #winner is delcared.

    
def main():
    # You could add some tests to main()
    # to check your functions are working as expected

    # The main function will not be assessed. All code to
    # play the game should be in the play_game() function,
    # and so your main function should simply call this.
    play_game()
    
main()    