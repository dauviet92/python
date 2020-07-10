import random

"""Class define Player Board and Game Rules """
class Grid():
    def __init__(self,size):
        self.size = size
        self.Grid = self.building()
        pass
    
    def __repr__(self):
        """function display current state of player board in console"""
        "o (x) for position occupied by horizontal (vertical) player"
        line = ''
        for i in range(self.size):
            for j in range(self.size):
                value = self.Grid[(i,j)]
                value = str(value)
                line =  line + '  ' + value
            line = line + '\n'
        return line      
    
    def building(self):
        """this function initialize the size of player board from input in main()"""        
        Grid = {}   
        for i in range(self.size):
            for j in range(self.size):
                Grid[(i,j)] = square(i,j)
        return Grid
    
    def play(self,i1,j1,i2,j2,player):
        """function implement move made by player"""
        square1 = self.Grid[(i1,j1)]
        square2 = self.Grid[(i2,j2)]
        square1.label = player
        square2.label = player
    
    def possible_move(self,player):
        """list all possible move that the player can make"""
        list_possible_move = []
        if player == "horizontale":
            for i in range(self.size):
                for j in range(self.size-1):
                 if self.Grid[(i,j)].label == None and self.Grid[(i,j+1)].label == None:
                     list_possible_move.append([i,j,i,j+1])
        else:
            for j in range(self.size):
                for i in range(self.size-1):
                 if self.Grid[(i,j)].label == None and self.Grid[(i+1,j)].label == None:
                     list_possible_move.append([i,j,i+1,j])
            pass
        return list_possible_move    
    
    def random_move(self,player):
        """function pick an uniformaly random move for player to make"""
        move = None        
        list_possible_move = self.possible_move(player)
        if(len(list_possible_move) != 0):
            rand = random.randint(0,len(list_possible_move)-1)
            move = list_possible_move[rand]
        else:
            move = "pass"
        return  move
    
    def game_over(self,player):
        """"function return a boolean to determine whether the game is finished or not"""
        if len(self.possible_move(player)) == 0:
            return True
        else:
            return False
            
    def next_player(self,player):
        """ give the name of next player """
        if player=="verticale":
            player="horizontale"
        else :
            player="verticale"
        return player
   
class square():
    def __init__(self,i,j):
        self.i = i
        self.j = j
        self.label = None
        
    def __repr__(self):
        """function return wildchar for label corresponding to each player """
        if self.label == None:
            return '.'
        elif self.label == 'verticale':
            return 'x'
        elif self.label == 'horizontale':
            return 'o'


if __name__ == "__main__":
    """
    First to play && Random_player = verticale => player plays randomly
    second player = horizontale => also plays randomly here 
    Let's see result of the game
    """
    board = Grid(8)
    # player = ['verticale', 'horizontale']
    # player = random.choice(player)
    player = 'verticale'
    first_player = player
    print("First to play : " + player )
    while (board.game_over(player)== False):
        
        print("Possible move for player : " + player)
        print(board.possible_move(player))

        move = board.random_move(player)
        board.play(move[0],move[1],move[2],move[3],player)
        player = board.next_player(player)
        print(board)
    print("First to play is :" + first_player)
    print("<Player verticale (random)> vs <Player horizontale (random)>")
    print("==> Player " + (board.next_player(player))+ " win the game <== ") 
