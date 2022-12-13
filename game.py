import pygame
import os
import time
import threading
import random
from spritesheet import Spritesheet

# link to tutorial i used:
# https://youtu.be/jO6qQDNa2UY
# followed first ~30minutes, until he tries to add movement, which we don't need

# create game window
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pokéRPS :)")

# init color consts
WHITE = (255,255,255)
SKY_BLUE = (0,200,255)

# framerate we want the game to use
FPS = 30

# load in assets
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
_bulbasaur = pygame.image.load(os.path.join("data", "cards", "bulbasaur_card.png"))   # todo: load actual pokemon, not card
_tepig = pygame.image.load(os.path.join("data", "cards", "tepig_card.png"))           # also will need another image of the pokemons back
_tododile = pygame.image.load(os.path.join("data", "cards", "tododile_card.png"))

#obtaining sprites for bulbasaur
my_spritesheet = Spritesheet('bulba_spritesheet.png')
bulba_animation = [my_spritesheet.parse_sprite('Layer 2.png'), my_spritesheet.parse_sprite('Layer 3.png'),my_spritesheet.parse_sprite('Layer 4.png'),
                   my_spritesheet.parse_sprite('Layer 5.png'),my_spritesheet.parse_sprite('Layer 6.png'),my_spritesheet.parse_sprite('Layer 7.png')
                   ,my_spritesheet.parse_sprite('Layer 8.png') ,my_spritesheet.parse_sprite('Layer 9.png') ,my_spritesheet.parse_sprite('Layer 10.png')
                   ,my_spritesheet.parse_sprite('Layer 11.png') ,my_spritesheet.parse_sprite('Layer 12.png')]



#index for animation array
index = 0
skip = .5




# resizing pokemon
BULBASAUR = pygame.transform.scale(_bulbasaur, (120, 178))
TEPIG = pygame.transform.scale(_tepig, (120, 178))
TODODILE = pygame.transform.scale(_tododile, (120, 178))
    
# mirrors image across x axis
# used for friendly pokemon, once back of pokemon image exists, no longer need this
def flip_image(img):
    return pygame.transform.flip(img, flip_x=True, flip_y=False)

    

class Game():

    def __init__(self):
        # the pokemon that the user wants to play
        self.desired_pokemon = None






    # function to render each frame
    def draw_window(pokemon):

        global index
        global skip
        # get wanted pokemon img
        # for now, just using 0,1,2 for pokemon values, should make enum
        choice = None
        match(pokemon):
            case 0:
                choice = BULBASAUR
            case 1:
                choice = TEPIG
            case 2:
                choice = TODODILE
            case default:
                choice = None

        # blit draws over the screen (img, coords)
        WIN.blit(BACKGROUND, (0,0))

        # draw opp

        if index < 11:
            skip = skip + .5

            if skip % 2 == 0:  #used to artificially slow down the animation
                index = index + 1

            if(index > 10): #if removed, bulbasuar will stop moving, like he would in the games. May remove.
                index = 0

        WIN.blit(bulba_animation[index], (550, 150))
        print(index)

        # draw friendly, if picked
        if not choice == None:
            friendly = flip_image(choice)
            WIN.blit(friendly, (125, 250))

        # changed aren't visible until display is updated
        pygame.display.update()

    def flip_image(img):
        return pygame.transform.flip(img, flip_x=True, flip_y=False)
        

    # maingame loop
    def run(self):
        clock = pygame.time.Clock()

        # condition to allow exiting the game
        run = True
        while(run):
            # ensures the game runs at the desired frames per second
            clock.tick(FPS)

            # get events
            for event in pygame.event.get():
                # if quit event, allow exiting the loop
                if event.type == pygame.QUIT:
                    run = False

            # update the window


            Game.draw_window(self.desired_pokemon)
        pygame.quit()



if __name__ == '__main__':

    game = Game()

    # thread to run async task, just sets Game.desired_pokemon after waiting 5 seconds
    # this simulates a return from imageclassifier
    class thread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
    
        def run(self):
            time.sleep(5)
            val = random.randint(0,2)  # inclusive
            game.desired_pokemon = val
            print("pokemon chosen (card detected): ", val)  

    thread2 = thread();
    thread2.start()


    game.run()
