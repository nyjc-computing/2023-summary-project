# Import statements
from game import Game

if __name__ == "__main__":
    # Generates an instance of the game
    play = Game()
    # Runs the introduction of the game
    play.intro()
    # Continues running the game if it hasn't ended
    while play.end == False:
        play.run()
