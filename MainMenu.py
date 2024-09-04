"""
Example code showing how to create some of the
different UIWidgets.
"""
import arcade
import arcade.gui
import os
# Set the width and height of your output window, in pixels
WIDTH,HEIGHT = arcade.get_display_size()


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "GUI Widgets Example", fullscreen=True)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.BLACK)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box2 = arcade.gui.UIBoxLayout()
        
        #Create a list of all Level text_ui to scroll through
        self.levellist = []
        self.levelnames = ["Level I","Level II","Level III","Bonus Level"]
        for name in self.levelnames:
            self.ui_text_label = arcade.gui.UITextArea(text=name,
                width=200,
                height=25,
                font_size=20,
                font_name="Arial")
            self.levellist.append(self.ui_text_label)
        self.levelpointer = 0
        self.v_box2.add(self.levellist[self.levelpointer])
        '''
        # Create a UIFlatButton
        ui_flatbutton = arcade.gui.UIFlatButton(text="Flat Button", width=200)
        self.v_box.add(ui_flatbutton.with_space_around(bottom=20))
        
        # Handle Clicks
        @ui_flatbutton.event("on_click")
        def on_click_flatbutton(event):
            print("UIFlatButton pressed", event)
        '''
        # Create a UITextureButton
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")
        ui_texture_button = arcade.gui.UITextureButton(texture=texture)

        # Handle Clicks
        @ui_texture_button.event("on_click")
        def on_click_texture_button(event):
            arcade.close_window()
            os.system('python Game.py')
            arcade.exit()
        self.v_box.add(ui_texture_button.with_space_around(bottom=20))

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_y=-50,
                anchor_y="center_y",
                child=self.v_box2)
        )

    def on_key_press(self, symbol: int, modifiers: int):
        #press right to move right in level selector
        if symbol==65363:
            self.v_box2.remove(self.levellist[self.levelpointer])
            if self.levelpointer<len(self.levellist)-1:
                self.levelpointer += 1
            self.v_box2.add(self.levellist[self.levelpointer])
        #Press left to move left in level selector
        if symbol==65361:
            self.v_box2.remove(self.levellist[self.levelpointer])
            if self.levelpointer>0:
                self.levelpointer -= 1
            self.v_box2.add(self.levellist[self.levelpointer])
        #press Space to start level
        if symbol==32:
            arcade.close_window()
            level_starter('basic',self.levelnames[self.levelpointer])
            arcade.exit()
        #press ESC to exit Menu
        if symbol == 65307:
            arcade.close_window()
            os.system('python MainMenu.py')
            arcade.exit()

    def on_click_start(self, event):
        print("Start:", event)

    def on_draw(self):
        self.clear()
        self.manager.draw()

def level_starter(mode: str, level: str):
    """BasicLevel.py needs following parameters:
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
    targetgoal: int,
    targetcountmax: int,
    enemycountmax: int"""
    if mode=='basic' and level == "Level I":
        os.system('python BasicLevel.py 5 10 0.5 0 3 025 1.5 0 5 2.5 1.5 20 5 5')
    if mode=='basic' and level == "Level II":
        os.system('python BasicLevel.py 5 15 0.5 0.2 3 0.25 1 0.2 4 3 1.5 30 5 7')
    if mode=='basic' and level == "Level III":
        os.system('python BasicLevel.py 5 25 0.5 0.5 3 0.25 0.75 0.5 3 5 1.5 50 5 10')
    if mode=='basic' and level == "Bonus Level":
        os.system('python EnduranceLevel.py 5 30 0.25 1 5 0.25 1 0.5 5 2 3 7 20')
def run():
    window = MyWindow()
    arcade.run()

if __name__ == "__main__":
    run()