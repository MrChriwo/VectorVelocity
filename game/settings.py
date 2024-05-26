# Screen Settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CAPTION = 'Vector Velocity - Pygame'


# Level Area Settings
__LEVEL_WIDTH_PERCENTAGE__ = 0.75
__LEVEL_HEIGHT_PERCENTAGE__ = 1.0

__obstacle_path__ = "game/assets/obstacles/"


LEVEL_WIDTH = int(SCREEN_WIDTH * __LEVEL_WIDTH_PERCENTAGE__)
LEVEL_HEIGHT = SCREEN_HEIGHT * 2
LEVEL_X = (SCREEN_WIDTH - LEVEL_WIDTH) // 2
LEVEL_Y = -LEVEL_HEIGHT / 2 

# Lane Positions (left, middle, right) related to the level area

LANE_POSITIONS = [LEVEL_X + 100, LEVEL_X + LEVEL_WIDTH // 2, LEVEL_X + LEVEL_WIDTH - 190]

FRAME_RATE = 60