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
GREEN = (56, 175, 43)
RED = (255,0,0)
YELLOW = (220, 203, 107)
SKY_BLUE = (0,200,255)

# framerate we want the game to use
FPS = 30


# load in assets
BACKGROUND = pygame.image.load(os.path.join("assets", "background.png"))
OVERLAY = pygame.image.load(os.path.join("assets", "overlay.png"))
OVERLAY = pygame.image.load(os.path.join("assets", "overlay.png"))
H1 = pygame.image.load(os.path.join("assets", "r1.png"))
H2 = pygame.image.load(os.path.join("assets", "r2.png"))
H3 = pygame.image.load(os.path.join("assets", "r3.png"))
H4 = pygame.image.load(os.path.join("assets", "r4.png"))
H5 = pygame.image.load(os.path.join("assets", "r5.png"))
H6 = pygame.image.load(os.path.join("assets", "r6.png"))


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

totoBack = Spritesheet('assets/totoB_spritesheet.png')
totoB_animation = [totoBack.parse_sprite('Layer 2.png'), totoBack.parse_sprite('Layer 3.png'),totoBack.parse_sprite('Layer 4.png'),
                   totoBack.parse_sprite('Layer 5.png'),totoBack.parse_sprite('Layer 6.png'),totoBack.parse_sprite('Layer 7.png')
                   ,totoBack.parse_sprite('Layer 8.png') ,totoBack.parse_sprite('Layer 9.png') ,totoBack.parse_sprite('Layer 10.png')
                   ,totoBack.parse_sprite('Layer 11.png')]


#obtaining sprites for tepig
tepigFront = Spritesheet('assets/tepig_spritesheet.png')
tepigF_animation = [tepigFront.parse_sprite('Layer 2.png'), tepigFront.parse_sprite('Layer 3.png'),tepigFront.parse_sprite('Layer 4.png'),
                   tepigFront.parse_sprite('Layer 5.png'),tepigFront.parse_sprite('Layer 6.png'),tepigFront.parse_sprite('Layer 7.png')
                   ,tepigFront.parse_sprite('Layer 8.png')]

tepigBack = Spritesheet('assets/tepigB_spritesheet.png')
tepigB_animation = [tepigBack.parse_sprite('Layer 2.png'), tepigBack.parse_sprite('Layer 3.png'),tepigBack.parse_sprite('Layer 4.png'),
                   tepigBack.parse_sprite('Layer 5.png'),tepigBack.parse_sprite('Layer 6.png'),tepigBack.parse_sprite('Layer 7.png')
                   ,tepigBack.parse_sprite('Layer 8.png')]



font = pygame.font.Font(os.path.join( "assets", "pokemon_fire_red.ttf"), 64)
font_large = pygame.font.Font(os.path.join( "assets", "pokemon_fire_red.ttf"), 128)
font_small = pygame.font.Font(os.path.join( "assets", "pokemon_fire_red.ttf"), 32)

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

        # holds hp of your pokemon
        # like usual, 0 is bulbasaur, 1 is tepig, 2 is totodile
        self.hps = [12] * 3
        self.enemy_hps = [12] * 3
        self.hpslocation = [628] * 3
        self.enemy_hpslocation = [124] * 3


        # easy but unclean way to keep track of if results have been calculated (hp subtracted)
        # otherwise, would repeat subtraction every frame for 2sec in _draw_results()
        self.results_done = False

        # result of the battle, {None = ongoing fight, 'LOSE', 'TIE', 'WIN'}
        self.gameResult = None






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
        WIN.blit(H1, (self.enemy_hpslocation[2], 12))
        WIN.blit(H2, (self.enemy_hpslocation[0], 42))
        WIN.blit(H3, (self.enemy_hpslocation[1], 73))
        WIN.blit(H4, (self.hpslocation[2], 321))
        WIN.blit(H5, (self.hpslocation[0], 351))
        WIN.blit(H6, (self.hpslocation[1], 379))
        WIN.blit(OVERLAY, (0, 0))
        #print('ur hp loco', self.hpslocation[0],self.hpslocation[1],self.hpslocation[2])
        print('en hp loco', self.enemy_hpslocation[0], self.enemy_hpslocation[1], self.enemy_hpslocation[2])
        #coords for health bar for animation
        lHealth1 = 124
        lHealth2 = 124
        lHealth3 = 124
        rHealth1 = 628
        rHealth2 = 628
        rHealth3 = 628


        # check if game is over, if so, draw results and ignore the rest of this function
        if not self.gameResult == None:
            result_text = font_large.render(self.gameResult, True, BLACK)
            WIN.blit(result_text, (350, 100))

            pygame.display.update()
            return


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


            elif choice == TOTODILE:

                if self.index1 < 10:
                    self.skip1 = self.skip1 + .5

                    if self.skip1 % 2 == 0:  # used to artificially slow down the animation
                        self.index1 = self.index1 + 1

                    if (self.index1 > 9):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                        self.index1 = 0

                WIN.blit(totoB_animation[self.index1], (150, 300))


            elif choice == TEPIG:

                if self.index1 < 7:
                    self.skip1 = self.skip1 + .5
                    if self.index > 7:
                        self.index = 0

                    if self.skip1 % 2 == 0:  # used to artificially slow down the animation
                        self.index1 = self.index1 + 1

                    if (self.index1 > 6):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                        self.index1 = 0
                    WIN.blit(tepigB_animation[self.index1], (150, 300))
        #old
            # draw the player pokemon's hp
            # hp_text = font.render(f"{self.hps[self.desired_pokemon]}/12", True, BLACK)
            # WIN.blit(hp_text, (150, 250))


        # reassigning this var to change color of hps
        color = BLACK

        def get_color(i, player=True):
            if player:
                if self.hps[i] > 7:
                    color = GREEN
                elif self.hps[i] > 4:
                    color = YELLOW
                elif self.hps[i] > 1:
                    color = RED
                else:
                    color = BLACK
                return color
            else:
                if self.enemy_hps[i] > 7:
                    color = GREEN
                elif self.enemy_hps[i] > 4:
                    color = YELLOW
                elif self.enemy_hps[i] > 1:
                    color = RED
                else:
                    color = BLACK
                return color

    # NO LONGER NEEDED. REPLACED BY ANIMATION
        # draw hp of all your pokemon
        # hp_label = font_small.render(f"Your pokemon:", True, BLACK)
        # WIN.blit(hp_label, (20,0))
        # bulbasaur_hp = font_small.render(f"bulbasaur: {self.hps[0]}/10", True, get_color(0))
        # WIN.blit(bulbasaur_hp, (20,35))
        # tepig_hp = font_small.render(f"tepig: {self.hps[1]}/10", True, get_color(1))
        # WIN.blit(tepig_hp, (20,60))
        # totodile_hp = font_small.render(f"totodile: {self.hps[2]}/10", True, get_color(2))
        # WIN.blit(totodile_hp, (20,85))

        # draw hp of enemy pokemon
        # enemy_hp_label = font_small.render(f"Enemy pokemon:", True, BLACK)
        # WIN.blit(enemy_hp_label, (640, 0))
        # enemy_bulbasaur_hp = font_small.render(f"bulbasaur:{self.enemy_hps[0]}/10", True, get_color(0, player=False))
        # WIN.blit(enemy_bulbasaur_hp, (640,35))
        # enemy_tepig_hp = font_small.render(f"tepig: {self.enemy_hps[1]}/10", True, get_color(1, player=False))
        # WIN.blit(enemy_tepig_hp, (640,60))
        # enemy_totodile_hp = font_small.render(f"totodile: {self.enemy_hps[2]}/10", True, get_color(2, player=False))
        # WIN.blit(enemy_totodile_hp, (640,85))

        


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


        while True:
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

            # if computer tries to use a dead pokemon, simply try again
            if self.enemy_hps[self.enemy_pokemon] <= 0 and not self.results_done:
                self.enemy_pokemon = None
                continue

            # otherwise we are good
            break

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
            if self.index < 11:
                self.skip = self.skip + .5

                if self.skip % 2 == 0:  # used to artificially slow down the animation
                    self.index = self.index + 1

                if (self.index > 8):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                    self.index = 0

            WIN.blit(totoF_animation[self.index], (550, 150))


        elif choice == TEPIG:
            if self.index < 7:
                self.skip = self.skip + .5
                if self.index > 7:
                    self.index = 0
                if self.skip % 2 == 0:  # used to artificially slow down the animation
                    self.index = self.index + 1

                if (self.index > 6):  # if removed, bulbasuar will stop moving, like he would in the games. May remove.
                    self.index = 0

                WIN.blit(tepigF_animation[self.index], (550, 150))

    #old
        # after pokemon is drawn, also draw its hp
        # hp_text = font.render(f"{self.enemy_hps[self.enemy_pokemon]}/12", True, BLACK)
        # WIN.blit(hp_text,(550, 100))

    def _draw_results(self):
        if self.pokemon_chosen_time == 0 or self.enemy_pokemon == None:
            return

        # don't do anything for 3 sec (2 sec should have already been waited) after opp chooses their pokemon
        req_time = FPS * 3
        if self.global_timer - self.pokemon_chosen_time < req_time:
            return

        # display victory,tie,loss depending on player and enemy chosen pokemon
        result = None
        if self.desired_pokemon == self.enemy_pokemon:
            text = font.render("Fair Trade!", True, BLACK)
            WIN.blit(text, (360,30))
            result = 'tie'
        elif (self.desired_pokemon +1)%3 == self.enemy_pokemon:
            text = font.render("Enemy Resisted!", True, BLACK)
            WIN.blit(text, (300,30))
            result = 'lose'
        else:
            text = font.render("Super Effective!", True, BLACK)
            WIN.blit(text, (300,30))
            result = 'win'

        
        # adjust health from result of the battle
        if result == 'win' and not self.results_done:
            self.hps[self.desired_pokemon] -= 0
            self.enemy_hps[self.enemy_pokemon] -= 6
            self.enemy_hpslocation[self.enemy_pokemon] -= 36
        elif result == 'lose' and not self.results_done:
            self.hps[self.desired_pokemon] -= 6
            self.enemy_hps[self.enemy_pokemon] -= 0
            self.hpslocation[self.desired_pokemon] -= 36
        elif result == 'tie' and not self.results_done:
            self.hps[self.desired_pokemon] -= 3
            self.enemy_hps[self.enemy_pokemon] -= 3
            self.hpslocation[self.enemy_pokemon] -= 18
            self.enemy_hpslocation[self.enemy_pokemon] -= 18
        self.results_done = True

        # normalize hp (don't let it go negative)
        if self.hps[self.desired_pokemon] < 0:
            self.hps[self.desired_pokemon] = 0
        if self.enemy_hps[self.enemy_pokemon] < 0:
            self.enemy_hps[self.enemy_pokemon] = 0

        # show the result for 2 seconds, then reset a bunch of stuff (so game repeats)
        # set both pokemon to None, reset time, etc...
        req_time_2 = req_time + (FPS * 2)
        if self.global_timer - self.pokemon_chosen_time < req_time_2:
            return

        # resetting stuff
        self.desired_pokemon = None
        self.enemy_pokemon = None
        self.pokemon_chosen_time = 0
        self.results_done = False

        # check if one team's hp is all zeros (game over)
        playerDead = True
        enemyDead = True
        for i in range(3):
            # if one pokemon has more than 0 hp, that person is not dead
            if not self.hps[i] == 0:
                playerDead = False
            if not self.enemy_hps[i] == 0:
                enemyDead = False

        if playerDead and enemyDead:
            self.gameResult = 'TIE'
            print('game over, it was a tie')
        elif playerDead:
            self.gameResult = 'LOSE'
            print('game over, you lose.')

        elif enemyDead:
            self.gameResult = 'WIN'
            print('You win!! Congratulations!!')



    def choose_pokemon(self, pokemon):

        # don't do anything while pokemon exists,
        # do not want to change these values in the middle of a turn
        # desired_pokemon is set back to None after turn is over
        if not self.desired_pokemon == None:
            return

        # if desired pokemon is dead, do nothing
        if self.hps[pokemon] <= 0:
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
