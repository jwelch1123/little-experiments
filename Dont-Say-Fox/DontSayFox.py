import numpy as np  

class DSF_grid():

    def __init__(self, dims=(4, 4)):
        print("Initializing Grid...")
        self.grid_dimensions = dims
        x = self.grid_dimensions[0]
        y = self.grid_dimensions[1]
        self.grid = np.full((x, y), "", dtype=str)
        

    def return_next_empty(self):
        for i in range(self.grid_dimensions[0]):
            for j in range(self.grid_dimensions[1]):
                if self.grid[i][j] == "":
                    return (i, j)
        return None

    def add_letter(self, letter):
        next_empty = self.return_next_empty()
        if next_empty is not None:
            self.grid[next_empty[0]][next_empty[1]] = letter
            return True
        return False
    
    def value(self, x, y):
        if (0 <= x < self.grid_dimensions[0]) \
            and (0 <= y < self.grid_dimensions[1]):
            return self.grid[x][y]
        return None
    
    def clear_grid(self):
        print("Clearing grid...")
        self.grid = [["" for i in range(self.grid_dimensions[0])] for j in range(self.grid_dimensions[1])]
        return None

    def __str__(self):
        output = []
        border = "-"*(self.grid_dimensions[1]*4+1)

        output.append(border)
        
        for i in range(self.grid_dimensions[0]):
            row = "| "
            for j in range(self.grid_dimensions[1]):
                letter = self.grid[i][j] if self.grid[i][j] != "" else " " 
                row += f"{letter} | "
            output.append(row)
            output.append(border)
        
        return "\n".join(output)




class DontSayFox_game():
    game_state = False
    turn_count = 0
    letter_list = ["F","F","F","F","F",\
                    "O","O","O","O","O","O",\
                    "X","X","X","X","X"]
    game_letters = []

    def __init__(self):
        print("Initializing Game...")
        self.game_state = True
        self.game_letters = self.letter_list[:]
        self.game_grid = DSF_grid()
        print("Game Grid: ", self.game_grid.grid_dimensions)
        

    def play_game(self, verbose=True, auto_play=False):

        if verbose: print(self)
        if not verbose: print("Auto-playing game...")
        
        while self.game_state:    
            if auto_play:
                input("Press Enter to continue...")
            
            if verbose:
                print()
                print("Drawing letter...")

            self.game_grid.add_letter(self.draw_rand_letter())
            self.turn_count += 1
            
            if verbose:
                print("Detecting fox...")
            
            found_fox = self.detect_fox(self.game_grid)

            if verbose:
                print(self)

            if found_fox:
                if not verbose: print(self)
                print("Fox detected! Game Over!")
                print("You made it to round ", self.turn_count)
                self.game_state = False
            elif self.check_complete():
                print("Game Over, You won!")
                self.game_state = False
                if not verbose: print(self) 
            else:
                if verbose:
                    print("No fox detected. Keep going!")

    def detect_fox(self, game_grid):
        vertical = ((-1,0),(1,0))
        horizontal = ((0,-1),(0,1))
        dig_up_right = ((-1,-1),(1,1))
        dig_up_left = ((-1,1),(1,-1))

        for i in range(game_grid.grid_dimensions[0]):
            for j in range(game_grid.grid_dimensions[1]):
                if game_grid.value(i, j) == "O":
                    for dim in [horizontal, vertical, dig_up_right, dig_up_left]:

                        forward = game_grid.value(i+dim[0][0], j+dim[0][1]) 
                        backward = game_grid.value(i+dim[1][0], j+dim[1][1])

                        if (forward == "F") and (backward == "X") \
                            or (forward == "X") and (backward == "F"):
                            
                            return True
        return False
        

    def draw_rand_letter(self):
        letter = np.random.choice(self.game_letters)
        self.game_letters.remove(letter)
        return letter
    
    def check_complete(self):
        if self.game_letters == []:
            return True        
        elif self.game_grid.return_next_empty() is None:
            return True
        return False
    
    def print_letters(self):
        return " ".join([f"{letter}: {self.game_letters.count(letter)}, " for letter in set(self.game_letters)])
    
    def restart_game(self):
        self.game_state = True
        self.turn_count = 0
        self.game_letters = self.letter_list[:]
        self.game_grid.clear_grid()
        return None

    def __str__(self) -> str:
        return (
            f"Round: {self.turn_count}\n"
            f"Available Letters: {self.print_letters()}\n"
            f"Game Grid:\n{self.game_grid}\n"
        )


def main():

    game = DontSayFox_game()    
    restart_game = True

    while restart_game:
        print("Starting game...")
        
        game.play_game(verbose=True, auto_play=False) # verbose=True to print steps, auto_play=True to auto-play

        restart = input("Play again? (y/n): ")
        match restart:
            case "n":
                restart_game = False
            case "y":
                restart_game = True
                game.restart_game()
            case "":
                restart_game = True
                game.restart_game()


if __name__ == "__main__":
    main()