import Domino_Random
import copy 
import random

def random_play(board,player):
    """play random move until the end of game"""  
    board_copy = copy.deepcopy(board)    
    
    carry_on = True
    player_IA = player
        
    while carry_on:
        move = board_copy.random_move(player)
        if move == "pass":  # if there is no possible move for either player ("pass") then game is over
            carry_on = False
        else:
            board_copy.play(move[0],move[1],move[2],move[3],player)
            player = board.next_player(player)
    
    if player == player_IA:
        score = 0 # if player lose he gets nothing
    else:
        score = 1 # if player win he gets a reward
    
    return score

def playouts(board, player):
    '''function simulate 100 random playouts and compute the reward'''
    playout_number = 100
    total_score = 0
    board_copy = copy.deepcopy(board)
    
    i = 0
    while i < playout_number:
        total_score += random_play(board_copy,player)
        i = i+1
    return total_score
    
def best_move(board, player):
    '''function determine next possible best move'''
    move = None
    board_copy = copy.deepcopy(board)     
    list_possible_move = board_copy.possible_move(player)
    if not list_possible_move:
        move = "pass"
    else:
        scores_liste = []
        nb_possible = len(list_possible_move) 
        for i in range(nb_possible):
            coup = list_possible_move[i]
            board_copy.play(coup[0],coup[1],coup[2],coup[3],player)
            scores_liste.append(playouts(board_copy,player))
        best = scores_liste.index(max(scores_liste))
        move = list_possible_move[best]
    return move


if __name__ == '__main__':
    """
    First to play && Random_player = verticale => player plays randomly
    MC_player = horizontale => we want to make this player win by using FlatMC or later UCB
     
    """
    board = Domino_Random.Grid(8)
    player = "verticale"
    first_player = player

    print()

    print("<Player verticale (random)> vs <Player horizontale (FlatMC)> :")
    print("First to play is : " + first_player)

    while (board.game_over(player)== False):
        
        print("Possible move for player : " + player)
        print(board.possible_move(player))

        if player == 'verticale':
            move = board.random_move(player)
            board.play(move[0],move[1],move[2],move[3],player)
        else: 
            move = best_move(board, player)
            board.play(move[0],move[1],move[2],move[3],player)

        player = board.next_player(player)
        
        print(board)

    print("First to play is : " + first_player)
    print("<Player verticale (random)> vs <Player horizontale (FlatMC)>")
    print("==> Player " + (board.next_player(player))+ " win the game <== ") 

    #Generating stats for MC vs Random 


"""
    print("\n ==> Generating stats for MC vs Random ...")
    import time
    start = time.time()

    nb_Simul = 100
    MC_win = 0

    for i in range(nb_Simul):
        board = Domino_Random.Grid(8)
        player = "verticale"

        while (board.game_over(player)== False):

            if player == 'verticale':
                move = board.random_move(player)
                board.play(move[0],move[1],move[2],move[3],player)
            else: 
                move = best_move(board, player)
                board.play(move[0],move[1],move[2],move[3],player)

            player = board.next_player(player)

        if board.next_player(player) == "horizontale":
            MC_win += 1

    print(" Over : %d simulations, CNN win Random player in %d  times which is %d %%" %(nb_Simul, MC_win, MC_win/nb_Simul*100))
    print(" it took %f s to finish the stats " %(time.time() - start))
"""