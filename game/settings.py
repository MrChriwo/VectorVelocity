# Screen Settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FRAME_RATE = 60
CAPTION = 'Vector Velocity - Pygame'

# Level Area Settings
LEVEL_WIDTH_PERCENTAGE = 0.75
LEVEL_HEIGHT_PERCENTAGE = 1.0
LEVEL_WIDTH = int(SCREEN_WIDTH * LEVEL_WIDTH_PERCENTAGE)
LEVEL_HEIGHT = SCREEN_HEIGHT * 2
LEVEL_X = (SCREEN_WIDTH - LEVEL_WIDTH) // 2
LEVEL_Y = -LEVEL_HEIGHT / 2 

LANE_POSITIONS = [LEVEL_X + 100, LEVEL_X + LEVEL_WIDTH // 2, LEVEL_X + LEVEL_WIDTH - 190]

# Asset Paths 
OBSTACLE_ASSET_PATH = "game/assets/obstacles/"
PLAYER_ASSET_PATH = "game/assets/ship.png"
BACKGROUND_ASSET_PATH = "game/assets/bg.jpg"
SOUNDS_ASSET_PATH = "game/assets/sounds/"

# difficulty settings
MAXIMUM_SPEED = 25.75
COIN_SPEEDUP_FACTOR = 20
SCORE_SPEEDUP_FACTOR = 200

MAXIMUM_OBSTACLE_SPAWN_COUNT = 8
MAINIMUM_OBSTACLE_SPAWN_RATE = 0.375
COIN_SPAWN_RATE_MULTIPLIER = 1.0125

OBSTACLE_SPAWN_RATE_DECREASE = 0.125
OBSTACLE_Y_OFFSET_DECREASE = 118
COIN_Y_OFFSET_DECREASE = 30