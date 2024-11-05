import random

class TwentyChallenge:
    
    def __init__(self, l = 20, n=999):
        self.array = [""] * l
        self.n = n
        self.game_state = True


    def generate_number(self):
        return random.randint(1, self.n)
    
    def check_win(self):
        return all([val != "" for val in self.array])

    def check_order(self):
        values = [val for val in self.array if val != ""]
        return all([values[i] < values[i+1] for i in range(len(values)-1)])

    def game_loop(self):
        while self.game_state:
            number = self.generate_number()
            print(self)
            print("The number is: ", number)
            array_loc = input("Enter the location for the number: ")
            if array_loc.lower() in ("q","quit","exit"):
                self.game_state = False
                print("Thanks for playing!")
            elif array_loc.isdigit() and 0 <= int(array_loc)-1 < len(self.array)-1 and self.array[int(array_loc)-1] == "":
                self.array[int(array_loc)-1] = number

            if not self.check_order():
                print("Sorry, the numbers are out of order, you lose!")
                self.game_state = False
            if self.check_win():
                print("You've won!")
                self.game_state = False

            if not self.game_state:
                print("Would you like to play again? (y/n)")
                response = input()
                if response.lower() in ("y", "yes"):
                    self.array = [""] * len(self.array)
                    self.game_state = True


    def __str__(self):
        return_str = "_" * 12 + "\n"
        for i, val in enumerate(self.array):
            return_str += "| "+ str(i+1) + " | "+ str(val) + "\n"
        return_str += "_" * 12 + "\n"
        return return_str



def main():
    print("Welcome to the Twenty Number Challenge!")
    TwentyChallenge().game_loop()

if __name__ == "__main__":
    main()