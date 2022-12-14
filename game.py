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
pygame.init()

# init color consts
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
SKY_BLUE = (0,200,255)

# framerate we want the game to use
FPS = 30

# load in assets
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
_bulbasaur = pygame.image.load(os.path.join("data", "cards", "bulbasaur_card.png"))
_tepig = pygame.image.load(os.path.join("data", "cards", "tepig_card.png"))
_tododile = pygame.image.load(os.path.join("data", "cards", "tododile_card.png"))

#obtaining sprites for bulbasaur
bulbaFront = Spritesheet('assets/bulba_spritesheet.png')
bulbaF_animation = [bulbaFront.parse_sprite('Layer 2.png'), bulbaFront.parse_sprite('Layer 3.png'),bulbaFront.parse_sprite('Layer 4.png'),
                   bulbaFront.parse_sprite('Layer 5.png'),bulbaFront.parse_sprite('Layer 6.png'),bulbaFront.parse_sprite('Layer 7.png')
                   ,bulbaFront.parse_sprite('Layer 8.png') ,bulbaFront.parse_sprite('Layer 9.png') ,bulbaFront.parse_sprite('Layer 10.png')
                   ,bulbaFront.parse_sprite('Layer 11.png') ,bulbaFront.parse_sprite('Layer 12.png')]

bulbaBack = Spritesheet('assets/bulbaB_spritesheet.png')
bulbaB_animation = [bulbaBack.parse_sprite('Layer 2.png'), bulbaBack.parse_sprite('Layer 3.png'),bulbaBack.parse_sprite('Layer 4.png'),
                   bulbaBack.parse_sprite('Layer 5.png'),bulbaBack.parse_sprite('Layer 6.png'),bulbaBack.parse_sprite('Layer 7.png')
                   ,bulbaBack.parse_sprite('Layer 8.png') ,bulbaBack.parse_sprite('Layer 9.png') ,bulbaBack.parse_sprite('Layer 10.png')
                   ,bulbaBack.parse_sprite('Layer 11.png') ,bulbaBack.parse_sprite('Layer 12.png'),bulbaBack.parse_sprite('Layer 13.png')]

#obtaining sprites for totodile
totoFront = Spritesheet('assets/toto_spritesheet.png')
totoF_animation = [totoFront.parse_sprite('Layer 2.png'), totoFront.parse_sprite('Layer 3.png'),totoFront.parse_sprite('Layer 4.png'),
                   totoFront.parse_sprite('Layer 5.png'),totoFront.parse_sprite('Layer 6.png'),totoFront.parse_sprite('Layer 7.png')
                   ,totoFront.parse_sprite('Layer 8.png') ,totoFront.parse_sprite('Layer 9.png') ,totoFront.parse_sprite('Layer 10.png')
                   ,totoFront.parse_sprite('Layer 11.png')]





font = pygame.font.Font(os.path.join( "assets", "pokemon_fire_red.ttf"), 64)

# resizing pokemon
BULBASAUR = pygame.transform.scale(_bulbasaur, (120, 178))
TEPIG = pygame.transform.scale(_tepig, (120, 178))
TOTODILE = pygame.transform.scale(_tododile, (120, 178))

class Game():

    def __init__(self):
        # the pokemon that the user wants to play
        self.desired_pokemon = None
        self.enemy_pokemon = None
        #index for animation array
        self.index = 0
        self.skip = .5

        self.index1 = 0
        self.skip1 = .5

        # int that increments by 1 for each frame the game draws
        self.global_timer = 0

        # holds time that pokemon was chosen, used for waiting x time then doing something
        self.pokemon_chosen_time = 0

        self.score = 0






    # function to render each frame
    def _draw_window(self, pokemon):

        # get wanted pokemon img
        # for now, just using 0,1,2 for pokemon values, should make enum
        choice = None
        match(pokemon):
            case 0:
                choice = BULBASAUR
            case 1:
                choice = TEPIG
            case 2:
                choice = TOTODILE
            case default:
                choice = None

        # blit draws over the screen (img, coords)
        WIN.blit(BACKGROUND, (0,0))


        # draw your score in the corner
        score = font.render(f"score: {self.score}", True, BLACK)
        WIN.blit(score,(20,0))


        # draw friendly, if picked
        if not choice == None:
            
            if choice == BULBASAUR:

                if self.index1 < 11:
                    self.skip1 = self.skip1 + .5

                    if self.skip1 % 2 == 0:  # used to artificially slow down the animation
                        self.index1 = self.index1 + 1

                    if (self.index1 > 10):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                        self.index1 = 0

                WIN.blit(bulbaB_animation[self.index1], (150, 300))

            # TODO: change to totodileBack animation
            elif choice == TOTODILE:

                if self.index1 < 11:
                    self.skip1 = self.skip1 + .5

                    if self.skip1 % 2 == 0:  # used to artificially slow down the animation
                        self.index1 = self.index1 + 1

                    if (self.index1 > 10):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                        self.index1 = 0

                WIN.blit(bulbaB_animation[self.index1], (150, 300))

            # TODO: change to tepigBack animation
            elif choice == TEPIG:

                if self.index1 < 11:
                    self.skip1 = self.skip1 + .5

                    if self.skip1 % 2 == 0:  # used to artificially slow down the animation
                        self.index1 = self.index1 + 1

                    if (self.index1 > 10):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                        self.index1 = 0

                WIN.blit(bulbaB_animation[self.index1], (150, 300))


        # draw opponent (IF player picked something, and after some delay)
        self._draw_opp()

        # show results of the mtach (IF player AND opp picked, and also after some delay)
        self._draw_results()

        # changed aren't visible until display is updated
        pygame.display.update()


    def _draw_opp(self):

        if self.pokemon_chosen_time == 0:
            return

        # don't do anything for 2 sec after player chooses pokemon
        if self.global_timer - self.pokemon_chosen_time < FPS*2:
            return


        if self.enemy_pokemon == None:
            # choose enemy pokemon if didnt do that already
            val = random.randint(0,2)  # 0-2 int again, same as player's pokemon
            self.enemy_pokemon = val
            if val == 0:
                print("enemy chose: bulbasaur")
            elif val == 1:
                print("enemy chose: tepig")
            else:
                print("enemy chose: totodile")

        # draw opp

        choice = None
        match(self.enemy_pokemon):
            case 0:
                choice = BULBASAUR
            case 1:
                choice = TEPIG
            case 2:
                choice = TOTODILE
            case default:
                choice = None

        if choice == BULBASAUR:

            if self.index < 11:
                self.skip = self.skip + .5

                if self.skip % 2 == 0:  #used to artificially slow down the animation
                    self.index = self.index + 1

                if(self.index > 10): #if removed, bulbasuar will stop moving, like he would in the games. May remove.
                    self.index = 0

            WIN.blit(bulbaF_animation[self.index], (550, 150))

        elif choice == TOTODILE:
            if self.index < 10:
                self.skip = self.skip + .5

                if self.skip % 2 == 0:  # used to artificially slow down the animation
                    self.index = self.index + 1

                if (self.index > 8):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                    self.index = 0

            WIN.blit(totoF_animation[self.index], (550, 150))


        # TODO: change to tepigFront animation
        elif choice == TEPIG:
            if self.index < 10:
                self.skip = self.skip + .5

                if self.skip % 2 == 0:  # used to artificially slow down the animation
                    self.index = self.index + 1

                if (self.index > 9):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                    self.index = 0

            WIN.blit(totoF_animation[self.index], (550, 150))

    def _draw_results(self):
        if self.pokemon_chosen_time == 0 or self.enemy_pokemon == None:
            return

        # don't do anything for 3 sec (2 sec should have already been waited) after opp chooses their pokemon
        req_time = FPS * 5
        if self.global_timer - self.pokemon_chosen_time < req_time:
            return

        # display victory,tie,loss depending on player and enemy chosen pokemon
        result = None
        if self.desired_pokemon == self.enemy_pokemon:
            text = font.render("DRAW", False, BLACK)
            result = 'tie'
        elif (self.desired_pokemon +1)%3 == self.enemy_pokemon:
            text = font.render("LOSE", False, BLACK)
            result = 'lose'
        else:
            text = font.render("WIN", False, BLACK)
            result = 'win'

        WIN.blit(text, (370,30))

        # show the result for 7 seconds, then reset a bunch of stuff (so game repeats)
        # set both pokemon to None, reset time, etc...
        req_time_2 = req_time + (FPS * 7)
        if self.global_timer - self.pokemon_chosen_time < req_time_2:
            return

        if result == 'win':
            self.score += 1
        elif result == 'lose':
            self.score -= 1

        # resetting stuff
        self.desired_pokemon = None
        self.enemy_pokemon = None
        self.pokemon_chosen_time = 0


    def choose_pokemon(self, pokemon):

        # don't do anything while pokemon exists,
        # do not want to change these values in the middle of a turn
        # desired_pokemon is set back to None after turn is over
        if not self.desired_pokemon == None:
            return

        self.desired_pokemon = pokemon
        self.pokemon_chosen_time = self.global_timer
        if pokemon == 0:
            print("you chose: bulbasaur")
        elif pokemon == 1:
            print("you chose: tepig")
        else:
            print("you chose: totodile")

    

    # maingame loop
    def run(self):
        clock = pygame.time.Clock()

        # condition to allow exiting the game
        run = True
        while(run):
            # ensures the game runs at the desired frames per second
            clock.tick(FPS)
            self.global_timer += 1

            # get events
            for event in pygame.event.get():
                # if quit event, allow exiting the loop
                if event.type == pygame.QUIT:
                    run = False

            # update the window
            self._draw_window(self.desired_pokemon)
        pygame.quit()



if __name__ == '__main__':

    game = Game()

    # thread to run async task, just sets Game.desired_pokemon after waiting 5 seconds
    # this simulates a return from imageclassifier
    class thread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
    
        def run(self):
            time.sleep(2)
            val = random.randint(0,2)
            game.choose_pokemon(val)

    thread2 = thread();
    thread2.start()


    game.run()
