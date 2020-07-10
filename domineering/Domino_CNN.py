import Domino_Random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.optimizers import SGD , Adam
import copy


# Disable Tensorflow + Keras depreciation warning 
import tensorflow as tf
import os
from absl import logging
logging._warn_preinit_stderr = 0

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

NUM_PARALLEL_EXEC_UNITS = 4
os.environ['OMP_NUM_THREADS'] = str(NUM_PARALLEL_EXEC_UNITS)
os.environ["KMP_AFFINITY"] = "granularity=fine,verbose,compact,1,0"
#os.environ['KMP_WARNINGS'] = 'off'
#os.environ["KMP_AFFINITY"] = "verbose" # no affinity
#os.environ["KMP_AFFINITY"] = "none" # no affinity
os.environ["KMP_AFFINITY"] = "disabled" # completely disable thread pools

# Data augmentation : generate the positions for the four symmetries of a board.
def transform(board):
    '''
    we should first transform the board in an array
    if the grid is not null, the value is 1, otherwise, is 0 
    '''
    board = []
    for i in range(board.size):
        temp = []
        for j in range(board.size):
            if board.Grid[(i,j)].label == None:
                temp.append(0)
            else:
                temp.append(1)
        board.append(temp)
        
    return board
    

def flipped_board(board):
    """this function transform the board if a case in board 
        take the value 1 it will be assigned to 0 in flipped board and vice versa	"""
    board_flipped_board = []
    for i in range(len(board)):
        temp = []
        for j in range(len(board[0])):
            if board[i][j] == 1:
                temp.append(0)
            else:
                temp.append(1)
        board_flipped_board.append(temp)
        
    return board_flipped_board
           
            
def symmetry_up_down(board):
    """this function generate the positions for two symmetries of a 
	board up/down"""
    n = len(board)
    for i in range(int(n/2)):
        for j in range(n):
            board[i][j], board[n-i-1][j] = board[n-i-1][j], board[i][j]
    return board
    
    
def symmetry_left_right(board):
    """this function generate the positions for two symmetries of a 
	board left/right"""
    n = len(board)
    for i in range(n):
        for j in range(int(n/2)):
            board[i][j], board[i][n-j-1] = board[i][n-j-1], board[i][j]
    return board

    
def display(board):
    """this function display the board"""
    for i in range(len(board)):
        print(board[i])
    print("\n")
    
def Convnets(inp):
    ''' this function train the model to predict the next best move correctlty
    we can assign one of the created data above to train the model '''
    inp='domineering.csv'
    dataset = pd.read_csv(inp, sep=',')
    X = dataset.iloc[:, 0:192].values
    y = dataset.iloc[:, 192:256].values
    dataset = pd.read_csv(inp, sep=',')
    X = dataset.iloc[:, 0:192].values
    y = dataset.iloc[:, 192:256].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    X_train = X_train.reshape(X_train.shape[0],3, 8, 8)
    X_test = X_test.reshape(X_test.shape[0],3,8, 8)
    print("==> Building model CNN <==")

    model = Sequential()
    #  - Convolution
    model.add(Convolution2D(64,3,3,border_mode='same',activation='relu', input_shape=(3,8,8)))
    model.add(Convolution2D(64,3,3,border_mode='same',activation='relu', input_shape=(3,8,8)))
    model.add(Convolution2D(64,3,3,border_mode='same',activation='relu', input_shape=(3,8,8)))
    model.add(Convolution2D(64,3,3,border_mode='same',activation='relu', input_shape=(3,8,8)))
    model.add(Convolution2D(64,3,3,border_mode='same',activation='relu', input_shape=(3,8,8)))

    model.add(Flatten())
    #  - Full connection
    model.add(Dense(output_dim = 128, activation = 'relu'))
    model.add(Dense(output_dim = 64, activation = 'softmax'))
    model.compile(loss='mse',optimizer='rmsprop', metrics=['accuracy'])

    # Fit model on training data
    sc=model.fit(X_train, y_train,batch_size=20, nb_epoch=10, verbose=1) 

    # Evaluate model on test data
    scores = model.evaluate(X_test, y_test, verbose=1)

    # Display result
    print( "\n" + "==> Completed <==")
    print(model.summary())
    
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])   

    out=model.predict_proba(X_test, verbose=0)
    return out,sc

def predict_best_move(board, player,net):
    '''this function predict the next best move using CNN'''
    retour = None
    board_copy = copy.deepcopy(board)  

    player = 'horizontale'
    out = net[0]
    model = net[1]
    list_possible_move = board_copy.possible_move(player)
    if not list_possible_move:
        retour = "pass"
    else:
        possiblite = []
        N_possible_Moves = len(list_possible_move)
        for i in range(N_possible_Moves):
            move = list_possible_move[i]
            i, j = move[0], move[1]
            possiblite.append(out[i][j])
        best_choice = possiblite.index(max(possiblite))
        retour = list_possible_move[best_choice]
    return retour
    
if __name__ == '__main__':    
    """
    First to play && Random_player = verticale => player plays randomly
    CNN_player = horizontale => we want to make this player win by using CNN
     
    """
    board = Domino_Random.Grid(8)
    player = "verticale"
    first_player = player
    inp='domineering.csv'

    #create model to fit with input data
    net = Convnets(inp)
    print()
    print("First to play : " + player )
    while (board.game_over(player)== False):
        
        print("Possible move for player : " + player)
        print(board.possible_move(player))

        if player == 'verticale':
            move = board.random_move(player)
            board.play(move[0],move[1],move[2],move[3],player)
        else: 
            move = predict_best_move(board, player, net)
            board.play(move[0],move[1],move[2],move[3],player)

        player = board.next_player(player)
        
        print(board)

    print("First to play is : " + first_player)
    print("<Player verticale (random)> vs <Player horizontale (CNN)>")
    print("==> Player " + (board.next_player(player))+ " win the game <== ") 

    #Generating stats for MC vs Random 
    print("\n ==> Generating stats for CNN vs Random ...")
    import time
    start = time.time()

    nb_Simul = 100
    MC_win = 0
    nb_Simul = 1000
    CNN_win = 0

    for i in range(nb_Simul):
        board = Domino_Random.Grid(8)
        player = "verticale"

        while (board.game_over(player)== False):
            if player == 'verticale':
                move = board.random_move(player)
                board.play(move[0],move[1],move[2],move[3],player)
            else: 
                move = predict_best_move(board, player, net)
                board.play(move[0],move[1],move[2],move[3],player)

            player = board.next_player(player)

        if board.next_player(player) == "horizontale":
            CNN_win += 1

    print(" Over : %d simulations, CNN win Random player in %d  times which is %d %%" %(nb_Simul, CNN_win, CNN_win/nb_Simul*100))
    print(" it took %f s to finish the stats " %(time.time() - start))
    
