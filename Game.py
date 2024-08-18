"""
Basic "Hello, World!" program in Arcade

This program is designed to demonstrate the basic capabilities
of Arcade. It will:
- Create a game window
- Fill the background with white
- Draw some basic shapes in different colors
- Draw some text in a specified size and color
"""

# Import arcade allows the program to run in Python IDLE
import arcade
import math
from random import randint
import random
import numpy as np
from pathlib import Path
# Set the width and height of your output window, in pixels
WIDTH = 700
HEIGHT = 700
# Classes


class ArcadeBasic(arcade.Window):
    """Main game window"""
    def __init__(self, width: int, height: int, title: str):
        """Initialize the window to a specific size

        Arguments:
            width {int} -- Width of the window
            height {int} -- Height of the window
            title {str} -- Title for the window
        """
        # Call the parent class constructor
        super().__init__(width, height, title)
        
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

    def setup(self):
        arcade.set_background_color(color=(0,0,0))
        player_image = Path.cwd() / "playercirc.png"
        self.player = arcade.Sprite(
            filename=player_image, center_x=WIDTH // 2, center_y=HEIGHT // 2
        )
        self.player.xvel=0
        self.player.yvel=0
        #set initial speed of player
        self.player.speed = 5
        #initialize movement key press booleans
        self.player.keyw = False
        self.player.keya = False
        self.player.keys = False
        self.player.keyd = False
        #inital spawn intervall of targets
        self.targetspawnintervall = 3
        #initialize target hit count
        self.targethitcount = 0
        #setup frame counter
        self.frames = 0
        #is game over?
        self.finished = False
        #remove all targets
        for target in self.targets:
            target.remove_from_sprite_lists()
        
        arcade.schedule(function_pointer=self.add_target,interval=self.targetspawnintervall)
    '''
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.player.center_x = arcade.clamp(x, 0, WIDTH)
        self.player.center_y = arcade.clamp(y, 0, HEIGHT)
    '''
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol==114:
            arcade_game.setup()
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
                np.savetxt(statfile,[str(self.frames)+","+str(self.targethitcount)],fmt='%s')
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
        
        #Target collision
        check_hit = arcade.check_for_collision_with_list(sprite=self.player, sprite_list=self.targets)
        for target in check_hit:
            target.remove_from_sprite_lists()
            self.targethitcount +=1
            #make game go brrr
            if self.player.speed<= 20:
                self.player.speed += 0.3
            if self.targetspawnintervall>=0.5:
                self.targetspawnintervall -= 0.2
            
        if self.targethitcount>=50:
            self.player.speed = 0
            self.targetspawnintervall = 100000
            #remove all targets
            for target in self.targets:
                target.remove_from_sprite_lists()
                self.finished = True
        #update frame counter
        if self.finished == False:
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
        if len(self.targets)<5:
            self.targets.append(target)
        
        
        
        #unschedule last target
        arcade.unschedule(function_pointer=self.add_target)
        #schedule next target
        arcade.schedule(function_pointer=self.add_target,interval=random.uniform(self.targetspawnintervall-0.5,self.targetspawnintervall+0.5))
            
    def on_draw(self):
        #Called once per frame
        arcade.start_render()
        
        #draw player
        self.player.draw()
        
        #draw targets
        self.targets.draw()
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
            start_x=100,
            start_y=50,
            font_size=28,
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
                text="You did it!",
                start_x=WIDTH/2,
                start_y=HEIGHT/2,
                font_size=40,
                color=arcade.color.WHITE,
            )
            arcade.draw_text(
                text="Press 'R' to play again",
                start_x=WIDTH/2,
                start_y=HEIGHT/2-40,
                font_size=25,
                color=arcade.color.WHITE,
            )
            arcade.draw_text(
                text="Press 'T' to save stats",
                start_x=WIDTH/2,
                start_y=HEIGHT/2-80,
                font_size=25,
                color=arcade.color.WHITE,
            )

# Run the program
if __name__ == "__main__":
    arcade_game = ArcadeBasic(WIDTH, HEIGHT, "Arcade Basic Game")
    arcade_game.setup()
    arcade_game.run()