""""Level creating file for basic mode
needs following parameters:
playerspeed: float,
playermaxspeed: float,
playeracc: float,
targetspawnintervalrandomness: float,
targetspawninterval: float,
targetspawnacc: float,
targetspawnintervalmin: float,
enemyspawnintervalrandomness: float,
enemyspawninterval: float,
enemyvel: float,
enemyvelrandomness: float,
targetcountmax: int,
enemycountmax: int
"""

# Import arcade allows the program to run in Python IDLE
import arcade
import math
from random import randint
import random
import numpy as np
from pathlib import Path
import os
import sys
# Set the width and height of your output window, in pixels
WIDTH,HEIGHT = arcade.get_display_size()
# Classes
class EnduranceLevel(arcade.Window):
    """Main game window"""
    def __init__(self, width: int, height: int, title: str, fullscreen: bool):
        """Initialize the window to a specific size

        Arguments:
            width {int} -- Width of the window
            height {int} -- Height of the window
            title {str} -- Title for the window
        """
        # Call the parent class constructor
        super().__init__(width, height, title, fullscreen)
        
        #maximum number of circles in swive (length), higher==longer
        self.swivelength=20
        #how many circles it takes for the swive to dissapear (linear)
        self.swivefade=20
        #each 1/density circle is being generated, maximum of 1
        self.swivedensity=1
        #initialize array for past positions
        self.pastpos=[]
        #list for target sprites
        self.targets = arcade.SpriteList()
        #list for enemy sprites
        self.enemies = arcade.SpriteList()
        self.enemyvel = []

    def setup(self, playerspeed: float, playermaxspeed: float, playeracc: float, targetspawnintervalrandomness: float, targetspawninterval: float, targetspawnacc: float, targetspawnintervalmin: float, enemyspawnintervalrandomness: float, enemyspawninterval: float, enemyvel: float, enemyvelrandomness: float, targetcountmax: int, enemycountmax: int):
        arcade.set_background_color(color=(0,0,0))
        player_image = Path.cwd() / "playercirc.png"
        self.player = arcade.Sprite(
            filename=player_image, center_x=WIDTH // 2, center_y=HEIGHT // 2
        )
        self.player.xvel=0
        self.player.yvel=0
        #set initial and max speed of player
        self.player.speed = playerspeed
        self.maxplayerspeed = playermaxspeed
        self.playeracc = playeracc
        #initialize movement key press booleans
        self.player.keyw = False
        self.player.keya = False
        self.player.keys = False
        self.player.keyd = False
        #set target spawninterval and randomness and acc and min
        self.targetspawnintervalrandomness = targetspawnintervalrandomness
        self.targetspawninterval = targetspawninterval
        self.targetspawnacc = targetspawnacc
        self.targetspawnintervalmin = targetspawnintervalmin
        #initialize target hit count
        self.targethitcount = 0
        #nitial enemy spawn interval and randomness
        self.enemyspawnintervalrandomness = enemyspawnintervalrandomness
        self.enemyspawninterval = enemyspawninterval
        #initial enemy hit count
        self.enemyhitcount = 0
        #setup frame counter
        self.frames = 0
        #set max amount of targets to be on screen
        self.targetcountmax = targetcountmax
        #set max amount of enemies to be on screen
        self.enemycountmax = enemycountmax
        #enemy velocity and deviance
        self.enemyvelo = enemyvel
        self.enemyvelrandomness = enemyvelrandomness
        
        #is game won?
        self.finished = False
        #is game lost?
        self.lost = False
        #remove all targets
        for target in self.targets:
            target.remove_from_sprite_lists()    
        #remove all enemies
        for enemy in self.enemies:
            enemy.remove_from_sprite_lists()
        #setup array with coordinates of edge screen and 50 further out
        self.outofbounds = []
        #lower edge
        self.outofbounds += list(zip(np.linspace(-50,WIDTH+50,WIDTH+101),np.linspace(-50,-50,WIDTH+101)))
        #upper edge
        self.outofbounds += list(zip(np.linspace(-50,WIDTH+50,WIDTH+101),np.linspace(HEIGHT+50,HEIGHT+50,WIDTH+101)))
        #left edge
        self.outofbounds += list(zip(np.linspace(-50,-50,HEIGHT+99),np.linspace(-49,HEIGHT+49,HEIGHT+99)))
        #right edge
        self.outofbounds += list(zip(np.linspace(WIDTH+50,WIDTH+50,HEIGHT+99),np.linspace(-49,HEIGHT+49,HEIGHT+99)))
        #schedule targets
        arcade.schedule(function_pointer=self.add_target,interval=self.targetspawninterval)
        #schedule enemys
        arcade.schedule(function_pointer=self.add_enemy,interval=self.enemyspawninterval)
    '''
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.player.center_x = arcade.clamp(x, 0, WIDTH)
        self.player.center_y = arcade.clamp(y, 0, HEIGHT)
    '''
    
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == 65307:
            arcade.close_window()
            os.system('python MainMenu.py')
            arcade.exit()
        '''if symbol==114:
            arcade.close_window()
            os.system('python EnduranceGame.py')
            arcade.exit()
            #Needs to be given parameters'''
        if symbol==119:
            self.player.keyw = True
        if symbol==97:
            self.player.keya = True
        if symbol==115:
            self.player.keys = True
        if symbol==100:
            self.player.keyd = True
        
        return super().on_key_press(symbol, modifiers)
    
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol==116:
            with open('GameStats.csv','a') as statfile:
                np.savetxt(statfile,[str(round(self.frames/60,3))+","+str(self.targethitcount)+","+str(self.finished)],fmt='%s')
        if symbol==119:
            self.player.keyw = False
        if symbol==97:
            self.player.keya = False
        if symbol==115:
            self.player.keys = False
        if symbol==100:
            self.player.keyd = False
        return super().on_key_release(symbol, modifiers)
    
    def on_update(self, delta_time: float):
        #PLAYER MOVEMENT
        if self.player.keyw == True and self.player.keys == True:
            self.player.yvel = 0
        if self.player.keyw == True and self.player.keys == False:
            self.player.yvel = self.player.speed
        if self.player.keyw == False and self.player.keys == True:
            self.player.yvel = -self.player.speed
        if self.player.keyw == False and self.player.keys == False:
            self.player.yvel = 0
        if self.player.keya == True and self.player.keyd == True:
            self.player.xvel = 0
        if self.player.keya == True and self.player.keyd == False:
            self.player.xvel = -self.player.speed
        if self.player.keya == False and self.player.keyd == True:
            self.player.xvel = self.player.speed
        if self.player.keya == False and self.player.keyd == False:
            self.player.xvel = 0
            
        self.player.center_x += self.player.xvel
        self.player.center_y += self.player.yvel
        #BORDER CONTROL  
        if self.player.center_x<0:
            self.player.center_x=0
        if self.player.center_x>WIDTH:
            self.player.center_x=WIDTH
        if self.player.center_y<0:
            self.player.center_y=0
        if self.player.center_y>HEIGHT:
            self.player.center_y=HEIGHT
        
        #Enemy movement
        i=0
        for enemy in self.enemies:
            if enemy.center_x<=-55:
                self.enemyvel[i][0] = -self.enemyvel[i][0]
            if enemy.center_x>=WIDTH+55:
                self.enemyvel[i][0] = -self.enemyvel[i][0]
            if enemy.center_y<=-55:
                self.enemyvel[i][1] = -self.enemyvel[i][1]
            if enemy.center_y>=HEIGHT+55:
                self.enemyvel[i][1] = -self.enemyvel[i][1]
            enemy.center_x += self.enemyvel[i][0]
            enemy.center_y += self.enemyvel[i][1]
            #enemy rotation
            if self.enemyvel[i][0]>0:
                enemy.angle = math.atan(self.enemyvel[i][1]/self.enemyvel[i][0])*180/np.pi-90
            if self.enemyvel[i][0]<0:
                enemy.angle = math.atan(self.enemyvel[i][1]/self.enemyvel[i][0])*180/np.pi+90
            i += 1
        
        #Target collision
        check_targethit = arcade.check_for_collision_with_list(sprite=self.player, sprite_list=self.targets)
        for target in check_targethit:
            target.remove_from_sprite_lists()
            self.targethitcount +=1
            #make game go brrr
            if self.player.speed<= self.maxplayerspeed:
                self.player.speed += self.playeracc
            if self.targetspawninterval>=self.targetspawnintervalmin:
                self.targetspawninterval -= self.targetspawnacc
        
        #Enemy collision
        check_enemyhit = arcade.check_for_collision_with_list(sprite=self.player,sprite_list=self.enemies)
        if len(check_enemyhit)>0:
            self.finished = True
        #game end condition check
        if self.finished == True:
            arcade.unschedule(function_pointer=self.add_target)
            arcade.unschedule(function_pointer=self.add_enemy)
            self.targetspawninterval = 100000
            self.enemyspawninterval = 100000
            #remove all targets
            for target in self.targets:
                target.remove_from_sprite_lists()
            #remove all enemies
            for enemy in self.enemies:
                enemy.remove_from_sprite_lists()
        #update frame counter
        if self.finished == False and self.lost == False:
            self.frames += 1
        
    def add_target(self,dt: float):
        targetimage = Path.cwd() / "target.png"
        target = arcade.Sprite(
            filename = targetimage,
            scale=0.5,
            center_x = randint(50,WIDTH-50),
            center_y = randint(200,HEIGHT-50),
            flipped_diagonally=random.choice([True,False]),
            flipped_horizontally=random.choice([True,False]),
            flipped_vertically=random.choice([True,False])
        )
        #append target to list if not more than 5 on screen
        if len(self.targets)<self.targetcountmax:
            self.targets.append(target)
        
        #unschedule last target
        arcade.unschedule(function_pointer=self.add_target)
        #schedule next target
        arcade.schedule(function_pointer=self.add_target,interval=random.uniform(self.targetspawninterval-self.targetspawnintervalrandomness,self.targetspawninterval+self.targetspawnintervalrandomness))
    
    def add_enemy(self, dt:float):
        enemyimage = Path.cwd() / "enemy.png"
        pos = random.choice(self.outofbounds)
        enemy = arcade.Sprite(
            filename = enemyimage,
            scale = 1,
            center_x = pos[0],
            center_y = pos[1]
        )
        xvel = 0
        yvel = 0
        if enemy.center_x<0:
            xvel = random.uniform(self.enemyvelo-self.enemyvelrandomness,self.enemyvelo+self.enemyvelrandomness)
        elif enemy.center_x>0:
            xvel = random.uniform(-(self.enemyvelo+self.enemyvelrandomness),-(self.enemyvelo-self.enemyvelrandomness))
        if enemy.center_y<0:
            yvel = random.uniform(self.enemyvelo-self.enemyvelrandomness,self.enemyvelo+self.enemyvelrandomness)
        elif enemy.center_y>0:
            yvel = random.uniform(-(self.enemyvelo+self.enemyvelrandomness),-(self.enemyvelo-self.enemyvelrandomness))
        #append to enemy SpriteList if not more than 10 present
        if len(self.enemies)<self.enemycountmax:
            self.enemies.append(enemy)
            self.enemyvel += [[xvel,yvel]]
        
        #unschedule last target
        arcade.unschedule(function_pointer=self.add_enemy)
        #schedule next target
        arcade.schedule(function_pointer=self.add_enemy,interval=random.uniform(self.enemyspawninterval-self.enemyspawnintervalrandomness,self.enemyspawninterval+self.enemyspawnintervalrandomness))
    
    def on_draw(self):
        #Called once per frame
        arcade.start_render()
        
        #draw player
        self.player.draw()
        
        #draw targets
        self.targets.draw()
        #draw enemies
        self.enemies.draw()
        #saving past steps into array
        
        if len(self.pastpos)<=self.swivelength:
            self.pastpos = self.pastpos + [(self.player.center_x,self.player.center_y)]
        elif len(self.pastpos)>=self.swivelength:
            self.pastpos.pop(0)
            self.pastpos = self.pastpos + [(self.player.center_x,self.player.center_y)]
            
            
        skipcount=0
        circount=0
        opastep=100/self.swivefade
        #flip array for correct usage
        pastposflip = np.flip(self.pastpos,0)
        for (x,y) in pastposflip:
            skipcount+=self.swivedensity
            if skipcount<1:
                continue
            elif skipcount>=1:
                arcade.draw_circle_filled(
                    center_x=x,
                    center_y=y,
                    radius = 20,
                    color=(255,0,255,100-circount*opastep),
                    num_segments=50
                )
                skipcount=0
            circount+=1
            
            
        # Draw an orange caption along the bottom in 60-point font
        arcade.draw_text(
            text="Targets Hit: "+str(self.targethitcount),
            start_x=0,
            start_y=50,
            font_size=28,
            color=arcade.color.WHITE,
        )
        arcade.draw_text(
            text="'ESC' to exit",
            start_x=0,
            start_y=HEIGHT-30,
            font_size=24,
            color=arcade.color.WHITE,
        )
        arcade.draw_text(
            text="Frames passed: "+str(self.frames)+" aka "+str(round(self.frames/60,3))+"s",
            start_x=100,
            start_y=100,
            font_size=28,
            color=arcade.color.WHITE,
        )
        if self.finished==True:
            arcade.draw_text(
                text="You suck!",
                start_x=WIDTH/3,
                start_y=HEIGHT/2,
                font_size=40,
                color=arcade.color.WHITE,
            )
            '''
            arcade.draw_text(
                text="Press 'R' to play again",
                start_x=WIDTH/3,
                start_y=HEIGHT/2-40,
                font_size=25,
                color=arcade.color.WHITE,
            )'''
            arcade.draw_text(
                text="Press 'T' to save stats",
                start_x=WIDTH/3,
                start_y=HEIGHT/2-80,
                font_size=25,
                color=arcade.color.WHITE,
            )

# Run the program
if __name__ == "__main__":
    arcade_game = EnduranceLevel(WIDTH, HEIGHT, "Arcade Basic Game", True)
    arcade_game.setup(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8]),float(sys.argv[9]),float(sys.argv[10]),float(sys.argv[11]),int(sys.argv[12]),int(sys.argv[13]))
    arcade_game.run()