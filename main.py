from game import Game
from ImageClassifier import ImageClassifier
import threading
import time
import random

if __name__ == '__main__':

    game = Game()

    class ic_thread(threading.Thread):
        def __init__(self, actionOnFound):
            threading.Thread.__init__(self)
            self.ic = ImageClassifier(actionOnFound)
    
        def run(self):
            self.ic.run()



    def whenPokemonDetected(x):
        val = -1
        match(x):
            case 'bulbasaur_card':
                val = 0
            case 'tepig_card':
                val = 1
            case 'tododile_card':
                val = 2
        game.choose_pokemon(val)

    ic = ic_thread(whenPokemonDetected)
    ic.start()

    game.run()
