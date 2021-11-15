"""
Platformer Game
"""
import arcade
import os
import timeit
import arcade.gui

# Constants

SCREEN_WIDTH = 1280  # 1000
SCREEN_HEIGHT = 720  # 650
SCREEN_TITLE = "Robot Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 8
GRAVITY = 1.7
PLAYER_JUMP_SPEED = 30

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 450
RIGHT_VIEWPORT_MARGIN = 450
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = SPRITE_PIXEL_SIZE * TILE_SCALING * 10
PLAYER_START_Y = SPRITE_PIXEL_SIZE * TILE_SCALING * 4

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# LEVELS
LEVEL_MAX = 4
_level = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class InstructionView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        # Load textures
        self.texture = arcade.load_texture("maps/images/views/gamestart.png")
        self.char = arcade.load_texture("maps/images/person/Person_idle.png")
        self.health = arcade.load_texture("maps/images/person/health_3.png")

        # Load the menu sounds
        self.select_sound = arcade.load_sound("sounds/select.wav")
        self.click_sound = arcade.load_sound("sounds/click.wav")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.selected = 1

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.char.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.29,
                             96, 128)

        arcade.draw_text("Controls:", 850, 440, arcade.csscolor.WHITE, 30)
        arcade.draw_text("Up / Down Keys", 860, 400, arcade.csscolor.WHITE, 25)
        arcade.draw_text("Enter", 860, 360, arcade.csscolor.WHITE, 25)

        #
        if self.selected == 1:
            arcade.draw_text(" Start ", 10, 385, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Start", 30, 400, arcade.csscolor.WHITE, 50)

        if self.selected == 2:
            arcade.draw_text(" Level Select", 10, 185, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Level Select", 30, 200, arcade.csscolor.WHITE, 50)

        if self.selected == 3:
            arcade.draw_text(" Quit ", 30, 35, arcade.csscolor.BLACK, 75)
        else:
            arcade.draw_text("Quit", 30, 50, arcade.csscolor.BLACK, 50)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.ENTER:
            if self.selected == 1:
                arcade.play_sound(self.click_sound)
                game_view = GameView()
                game_view.setup(1)
                self.window.show_view(game_view)
            elif self.selected == 2:
                arcade.play_sound(self.click_sound)
                game_view = LevelSelectView()
                self.window.show_view(game_view)
            elif self.selected == 3:
                arcade.play_sound(self.click_sound)
                arcade.close_window()
            else:
                arcade.play_sound(self.click_sound)
        if key == arcade.key.DOWN:
            self.selected += 1
            arcade.play_sound(self.select_sound)
            if self.selected > 3:
                self.selected = 1
        if key == arcade.key.UP:
            self.selected -= 1
            arcade.play_sound(self.select_sound)
            if self.selected < 1:
                self.selected = 3

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if 385 <= y <= 385 + 75 and 10 <= x <= 200:
            if self.selected != 1:
                self.selected = 1
                arcade.play_sound(self.select_sound)
        elif 185 <= y <= 185 + 75 and 10 <= x <= 325:
            if self.selected != 2:
                self.selected = 2
                arcade.play_sound(self.select_sound)
        if 35 <= y <= 35 + 75 and 10 <= x <= 200:
            if self.selected != 3:
                self.selected = 3
                arcade.play_sound(self.select_sound)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 385 <= y <= 385 + 75 and 10 <= x <= 200:
            arcade.play_sound(self.click_sound)
            game_view = GameView()
            game_view.setup(1)
            self.window.show_view(game_view)
        elif 185 <= y <= 185 + 75 and 10 <= x <= 325:
            arcade.play_sound(self.click_sound)
            game_view = LevelSelectView()
            self.window.show_view(game_view)
        if 35 <= y <= 35 + 75 and 10 <= x <= 200:
            arcade.play_sound(self.click_sound)
            arcade.close_window()


class LevelSelectView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        # Load textures
        self.texture = arcade.load_texture("maps/images/views/gamestart.png")
        self.char = arcade.load_texture("maps/images/person/Person_idle.png")
        self.health = arcade.load_texture("maps/images/person/health_3.png")
        self.arrow_up = arcade.load_texture("maps/images/views/Up Arrow.png")
        self.arrow_down = arcade.load_texture("maps/images/views/Down Arrow.png")

        # Load the menu sounds
        self.select_sound = arcade.load_sound("sounds/select.wav")
        self.click_sound = arcade.load_sound("sounds/click.wav")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.selected = 1
        self.choice = 1

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.char.draw_sized(SCREEN_WIDTH / 1.25, SCREEN_HEIGHT / 3.29,
                             96, 128)

        arcade.draw_text(f" Level", 460, 285, arcade.csscolor.WHITE, 75)

        #
        if self.selected == 1:
            arcade.draw_text("Back", 10, 385, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Back", 30, 400, arcade.csscolor.WHITE, 50)

        if self.selected == 2:
            self.arrow_up.draw_sized(721, 401, 34, 40)
        else:
            self.arrow_up.draw_sized(721, 401, 24, 26)

        if self.selected == 3:
            arcade.draw_text(f"{self.choice}", 695, 283, arcade.csscolor.WHITE, 80)
        else:
            arcade.draw_text(f"{self.choice}", 700, 290, arcade.csscolor.WHITE, 65)

        if self.selected == 4:
            self.arrow_down.draw_sized(721, 277, 34, 40)
        else:
            self.arrow_down.draw_sized(721, 277, 24, 26)

        if self.selected == 5:
            arcade.draw_text(" Quit ", 30, 35, arcade.csscolor.BLACK, 75)
        else:
            arcade.draw_text("Quit", 30, 50, arcade.csscolor.BLACK, 50)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.ENTER:
            if self.selected == 1:
                arcade.play_sound(self.click_sound)
                game_view = InstructionView()
                self.window.show_view(game_view)
            elif self.selected == 2:
                arcade.play_sound(self.click_sound)
                if not self.choice > 4:
                    self.choice += 1
            elif self.selected == 3:
                arcade.play_sound(self.click_sound)
                game_view = GameView()
                game_view.setup(self.choice)
                self.window.show_view(game_view)
            elif self.selected == 4:
                arcade.play_sound(self.click_sound)
                if not self.choice < 2:
                    self.choice -= 1
            elif self.selected == 5:
                arcade.play_sound(self.click_sound)
                arcade.close_window()
            else:
                arcade.play_sound(self.click_sound)
        if key == arcade.key.DOWN:
            self.selected += 1
            arcade.play_sound(self.select_sound)
            if self.selected > 5:
                self.selected = 1
        if key == arcade.key.UP:
            self.selected -= 1
            arcade.play_sound(self.select_sound)
            if self.selected < 1:
                self.selected = 3

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if 385 <= y <= 385 + 75 and 10 <= x <= 200:
            if self.selected != 1:
                self.selected = 1
                arcade.play_sound(self.select_sound)
        if 390 <= y <= 390 + 35 and 700 <= x <= 730:
            if self.selected != 2:
                self.selected = 2
                arcade.play_sound(self.select_sound)
        if 300 <= y <= 300 + 75 and 685 <= x <= 730:
            if self.selected != 3:
                self.selected = 3
                arcade.play_sound(self.select_sound)
        if 267 <= y <= 267 + 30 and 700 <= x <= 730:
            if self.selected != 4:
                self.selected = 4
                arcade.play_sound(self.select_sound)
        if 35 <= y <= 35 + 75 and 10 <= x <= 200:
            if self.selected != 5:
                self.selected = 5
                arcade.play_sound(self.select_sound)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 385 <= y <= 385 + 75 and 10 <= x <= 200:
            arcade.play_sound(self.click_sound)
            game_view = InstructionView()
            self.window.show_view(game_view)
        if 390 <= y <= 390 + 35 and 700 <= x <= 730:
            arcade.play_sound(self.click_sound)
            if not self.choice > 3:
                self.choice += 1
        if 300 <= y <= 300 + 75 and 685 <= x <= 730:
            arcade.play_sound(self.click_sound)
            game_view = GameView()
            game_view.setup(self.choice)
            self.window.show_view(game_view)
        if 267 <= y <= 267 + 35 and 700 <= x <= 730:
            arcade.play_sound(self.click_sound)
            if not self.choice < 2:
                self.choice -= 1
        if 35 <= y <= 35 + 75 and 10 <= x <= 200:
            arcade.play_sound(self.click_sound)
            arcade.close_window()


class LevelOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self, game_view):
        """ This is run once when we switch to this view """
        super().__init__()
        self.game_view = game_view

        # load the menu sounds
        self.select_sound = arcade.load_sound("sounds/select.wav")
        self.click_sound = arcade.load_sound("sounds/click.wav")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.selected = 1

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        if self.selected == 1:
            arcade.draw_text("Next Level", 450, 285, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Next Level", 500, 300, arcade.csscolor.WHITE, 50)

        if self.selected == 2:
            arcade.draw_text("Back To Menu", 400, 115, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Back To Menu", 470, 130, arcade.csscolor.WHITE, 50)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.ENTER:
            if self.selected == 1:
                arcade.play_sound(self.click_sound)
                self.window.show_view(self.game_view)
            elif self.selected == 2:
                arcade.play_sound(self.click_sound)
                game_view = InstructionView()
                self.window.show_view(game_view)
        if key == arcade.key.DOWN:
            self.selected += 1
            arcade.play_sound(self.select_sound)
            if self.selected > 2:
                self.selected = 1
        if key == arcade.key.UP:
            self.selected -= 1
            arcade.play_sound(self.select_sound)
            if self.selected < 1:
                self.selected = 2

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if 285 <= y <= 285 + 75 and 500 <= x <= 750:
            if not self.selected == 1:
                arcade.play_sound(self.select_sound)
                self.selected = 1
        elif 125 <= y <= 195 and 475 <= x <= 850:
            if not self.selected == 2:
                arcade.play_sound(self.select_sound)
                self.selected = 2

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 285 <= y <= 285 + 75 and 500 <= x <= 750:
            arcade.play_sound(self.click_sound)
            self.window.show_view(self.game_view)
        elif 125 <= y <= 195 and 475 <= x <= 850:
            arcade.play_sound(self.click_sound)
            game_view = InstructionView()
            self.window.show_view(game_view)


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("maps/images/views/gameover.png")

        # load menu sounds
        self.select_sound = arcade.load_sound("sounds/select.wav")
        self.click_sound = arcade.load_sound("sounds/click.wav")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.selected = 1

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

        arcade.draw_text("Controls:", 850, 400, arcade.csscolor.WHITE, 30)
        arcade.draw_text("Up / Down Keys", 860, 360, arcade.csscolor.WHITE, 25)
        arcade.draw_text("Enter", 860, 320, arcade.csscolor.WHITE, 25)

        if self.selected == 1:
            arcade.draw_text("Menu", 485, 285, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Menu", 500, 300, arcade.csscolor.WHITE, 50)

        if self.selected == 2:
            arcade.draw_text("Quit", 505, 215, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Quit", 520, 230, arcade.csscolor.WHITE, 50)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.ENTER:
            if self.selected == 1:
                arcade.play_sound(self.click_sound)
                game_view = InstructionView()
                self.window.show_view(game_view)
            elif self.selected == 2:
                arcade.play_sound(self.click_sound)
                arcade.close_window()
            else:
                arcade.play_sound(self.click_sound)
        if key == arcade.key.DOWN:
            self.selected += 1
            arcade.play_sound(self.select_sound)
            if self.selected > 2:
                self.selected = 1
        if key == arcade.key.UP:
            self.selected -= 1
            arcade.play_sound(self.select_sound)
            if self.selected < 1:
                self.selected = 2

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if 285 <= y <= 285 + 75 and 450 <= x <= 450 + 200:
            if not self.selected == 1:
                arcade.play_sound(self.select_sound)
                self.selected = 1
        elif 230 <= y <= 230 + 75 and 500 <= x <= 500 + 200:
            if not self.selected == 2:
                arcade.play_sound(self.select_sound)
                self.selected = 2

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 285 <= y <= 285 + 75 and 450 <= x <= 450 + 200:
            arcade.play_sound(self.click_sound)
            game_view = InstructionView()
            self.window.show_view(game_view)
        elif 230 <= y <= 230 + 75 and 500 <= x <= 500 + 200:
            arcade.play_sound(self.click_sound)
            arcade.close_window()


class PlayerCharacter(arcade.Sprite):
    """ Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---
        main_path = "maps/images/person/Person"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        # self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer for the game
        """

        # Call the parent class and set up the window
        super().__init__()

        # Set the path to start with this program
        self.health_texture = arcade.load_texture("maps/images/person/health_1.png")
        self.tutorial_num = 0
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # --- Variables for our statistics
        # Time for on_update
        self.processing_time = 0
        # Time for on_draw
        self.draw_time = 0
        # Variables used to calculate frames per second
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.debug = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.do_touch_list = None
        self.ladder_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.end_of_map = 0

        # Level
        self.level = 1

        # Keep track of the score
        self.score = 0
        # Keep track of tutorial text
        if self.level == 1:
            self.tutorial_num = 0
            self.tutorial = ""
        else:
            self.tutorial_num = 3
            self.tutorial = ""

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/collect.wav")
        self.jump_sound = arcade.load_sound("sounds/jump.wav")
        self.game_over = arcade.load_sound("sounds/dead.wav")

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        # Updates the self.level variable to the game level
        self.level = level

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 3

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()

        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'

        moving_platforms_layer_name = 'Moving Platforms'
        foreground_layer_name = "Foreground"
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'
        # Name of the layer that has items we shouldn't touch
        dont_touch_layer_name = "Don't Touch"
        do_touch_layer_name = "Do Touch"

        # Map name
        map_name = f"maps/level_{level}.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      platforms_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Moving Platforms
        moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, TILE_SCALING)
        for sprite in moving_platforms_list:
            self.wall_list.append(sprite)
            # -- Foreground
            # -- Foreground
            self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                                foreground_layer_name,
                                                                TILE_SCALING)
        # -- Background objects
        self.background_list = arcade.tilemap.process_layer(my_map, "Background", TILE_SCALING)

        # -- Background objects
        self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders",
                                                        TILE_SCALING,
                                                        use_spatial_hash=True)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)
        # -- Don't Touch Layer
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            dont_touch_layer_name,
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)

        # -- Do Touch Layer
        self.do_touch_list = arcade.tilemap.process_layer(my_map,
                                                          do_touch_layer_name,
                                                          TILE_SCALING,
                                                          use_spatial_hash=True)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(arcade.csscolor.BLACK)  # my_map.background_color

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY,
                                                             ladders=self.ladder_list)

    def on_draw(self):
        """ Render the screen. """

        # Start timing how long this takes
        start_time = timeit.default_timer()
        # --- Calculate FPS
        fps_calculation_freq = 60
        # Once every 60 frames, calculate our FPS
        if self.frame_count % fps_calculation_freq == 0:
            # Do we have a start time?
            if self.fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            # Reset the timer
            self.fps_start_timer = timeit.default_timer()
        # Add one to our frame count
        self.frame_count += 1

        # Clear the screen to the background color
        arcade.start_render()

        # Stop the draw timer, and calculate total on_draw time.
        self.draw_time = timeit.default_timer() - start_time

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.ladder_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.dont_touch_list.draw()
        self.do_touch_list.draw()
        self.foreground_list.draw()

        # Change the health texture to math the player's health
        if self.score == 3:
            self.health_texture = arcade.load_texture("maps/images/person/health_3.png")
        elif self.score == 2:
            self.health_texture = arcade.load_texture("maps/images/person/health_2.png")
        elif self.score == 1:
            self.health_texture = arcade.load_texture("maps/images/person/health_1.png")
        else:
            pass

        # Draw our health on the screen, scrolling it with the character
        self.health_texture.draw_sized(self.player_sprite.center_x + 1.5, self.player_sprite.center_y + 16,
                                       25, 10)
        if self.level == 1:
            # Keep track of tutorial text
            if self.tutorial_num == 0:
                self.tutorial = "Use A and D keys to move"
            elif self.tutorial_num == 1:
                self.tutorial = "Use W or Up key to jump"
            elif self.tutorial_num == 2:
                self.tutorial = "Find the the computer to finish the level"
            else:
                self.tutorial = ""

        # Draw tutorial text
        tutorial_text = f"{self.tutorial}"
        arcade.draw_text(tutorial_text, 20 + self.view_left, 550 + self.view_bottom, arcade.csscolor.WHITE, 25)

        # This draws tutorial text based on which level you're playing
        if self.level == 1:
            arcade.draw_text("Don't Touch Marked Objects", 1200, 235, arcade.csscolor.RED, 25)
        elif self.level == 2:
            arcade.draw_text("Coloured Buttons react with same coloured objects", 1200, 235, arcade.csscolor.BLUE, 25)

        # Triggered when self.debug is true
        if self.debug:
            # Draw hit boxes.
            self.player_sprite.draw_hit_box(arcade.color.RED, 3)

            # Display timings
            output = f"Processing time: {self.processing_time:.3f}"
            arcade.draw_text(output, 10 + self.view_left, 620 + self.view_bottom,
                             arcade.csscolor.RED, 18)

            output = f"Drawing time: {self.draw_time:.3f}"
            arcade.draw_text(output, 10 + self.view_left, 600 + self.view_bottom,
                             arcade.csscolor.RED, 18)

            if self.fps is not None:
                output = f"FPS: {self.fps:.0f}"
                arcade.draw_text(output, 10 + self.view_left, 580 + self.view_bottom,
                                 arcade.csscolor.RED, 18)

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                if self.tutorial_num == 1:
                    self.tutorial_num += 1
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            if self.tutorial_num == 0:
                self.tutorial_num += 1
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            if self.tutorial_num == 0:
                self.tutorial_num += 1
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.F3 and not self.debug:
            self.debug = True
        elif key == arcade.key.F3 and self.debug:
            self.debug = False
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Start timing how long this takes
        start_time = timeit.default_timer()

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.coin_list.update_animation(delta_time)
        self.background_list.update_animation(delta_time)
        self.player_list.update_animation(delta_time)

        # Update walls, used with moving platforms
        self.wall_list.update()

        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:

            # Figure out how many points this coin is worth
            if 'Type' not in coin.properties:
                print("Warning, collected an item without a Type property.")
            else:
                trigger = int(coin.properties['Type'])
                print("Triggered:", trigger)
                for wall in self.wall_list:
                    if "Type" not in wall.properties:
                        pass
                    else:
                        if int(wall.properties['Type']) == trigger:
                            wall.remove_from_sprite_lists()

            # Remove the coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        # Track if we need to change the viewport
        changed_viewport = False

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
            self.score -= 1
            if self.score <= 0:
                view = GameOverView()
                self.window.show_view(view)

            # Set the camera to the start
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)
            self.score -= 1
            if self.score <= 0:
                view = GameOverView()
                self.window.show_view(view)

        # See if the user got to the end of the level
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.do_touch_list):
            # Advance to the next level
            if self.level == 1:
                self.tutorial_num += 1
            self.level += 1

            # Load the next level
            if self.level > LEVEL_MAX:
                view = GameOverView()
                self.level = LEVEL_MAX
                self.window.show_view(view)
            else:
                view = LevelOverView(self)
                self.setup(self.level)
                self.left_pressed = False
                self.right_pressed = False
                self.up_pressed = False
                self.down_pressed = False
                self.window.show_view(view)

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        # Stop the draw timer, and calculate total on_draw time.
        self.processing_time = timeit.default_timer() - start_time


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    # window.setup(window.level)
    arcade.run()


if __name__ == "__main__":
    main()
