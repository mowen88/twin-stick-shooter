import pygame

TILESIZE = 16
FPS = 60

RES = WIDTH, HEIGHT = pygame.math.Vector2(400, 224)
HALF_WIDTH, HALF_HEIGHT = RES/2
ASPECT_RATIO = (WIDTH/HEIGHT)

LAYERS = ['background',
		  'objects',
		  'player',
		  'particles',
		  'blocks',
		  'foreground']

#FONT = '../assets/EndlessBossBattleRegular.ttf'
FONT = '../assets/font/homespun.ttf'
#FONT = '../assets/homespun.ttf'

COLOURS = {
			'purple':(69,41,63), 'cyan':(143,248,226), 'black':(46,34,47), 'white':(255,255,255), 'green':(0,255,0), 'pale_yellow':(201,204,161),
			'yellow':(202,160,90),'orange':(174,106,71), 'red':(139,64,73), 'burgundy':(84,51,68), 'grey':(81,82,98),'green':(99,120,125),
			'pale_green':(142,160,145), 'brown':(110,39,39), 'salmon':(158,69,57)
			}

DEADZONE = 0.2
TRIGGER_DEADZONE = 0.5

KEY_MAP = {
			'Left':[pygame.K_LEFT], 'Right':[pygame.K_RIGHT], 'Up':[pygame.K_UP], 'Down':[pygame.K_DOWN],
			'Attack':[pygame.K_x], 'Dash':[pygame.K_c], 'Inventory':[pygame.K_i], 'Pause':[pygame.K_SPACE],
			'OK':[pygame.K_SPACE, pygame.K_RETURN], 'Back':[pygame.K_ESCAPE, pygame.K_BACKSPACE],
			'Menu Up':[pygame.K_UP, pygame.K_w], 'Menu Down':[pygame.K_DOWN, pygame.K_s],
			'Menu Left':[pygame.K_LEFT, pygame.K_a], 'Menu Right':[pygame.K_RIGHT, pygame.K_d]
			}

ACTIONS = {'Menu Up':0, 'Menu Down':0, 'Menu Left':0, 'Menu Right':0, 'Up':0, 'Down':0, 'Left':0, 'Right':0,
			'Attack':0, 'Dash':0, 'Inventory':0, 'Pause':0, 'OK':0, 'Back':0}

                  
BUTTON_MAPS = {
			'Nintendo Switch Pro Controller':
				{'Attack':21, 'Dash':1, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'OK':21, 'Back':20},
			'PS4 Controller':
				{'Attack':0, 'Dash':0, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'OK':21, 'Back':20},
			'Xbox 360 Controller':
				{'Attack':	0, 'Dash':1, 'Inventory':8, 'Pause':7, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'OK':0, 'Back':20},
			'DualSense Wireless Controller':
				{'Attack':1, 'Dash':21, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'OK':0, 'Back':0},
			}

DEFAULT_BUTTON_MAPS = {
			'Nintendo Switch Pro Controller':
				{'Attack':21, 'Dash':1, 'Inventory':4, 'Pause':6},
			'PS4 Controller':
				{'Attack':0, 'Dash':0, 'Inventory':4, 'Pause':6},
			'Xbox 360 Controller':
				{'Attack':	21, 'Dash':1, 'Inventory':8, 'Pause':6},
			'DualSense Wireless Controller':
				{'Attack':1, 'Dash':0, 'Inventory':4, 'Pause':6},
			}


AXIS_PRESSED = {'Left Stick':(0,0),'Right Stick':(0,0),'Left Trigger':0,'Right Trigger':0, 'D-Pad':(0,0)}

BUTTON_NAMES = {
    'Nintendo Switch Pro Controller': 
    	{0:'A', 1:'B', 2:'X', 3:'Y', 4:'-', 5:'Home', 6:'+', 7:'L Stick In', 8:'R Stick In', 9:'L', 20:'ZL',
        10:'R', 11:'Up', 12:'Down', 13:'Left', 14:'Right', 15:'Capture', 21:'ZR'},
    'PS4 Controller':
        {0:'Cross', 1:'Circle', 2:'Square', 3:'Triangle', 4:'Share', 5:'PS Button', 6:'Options', 7:'L3', 8:'R3', 20:'L2',
        9:'L1', 10:'R1', 11:'Up', 12:'Down', 13:'Left', 14:'Right', 15:'Touch Pad Click', 21:'R2'},
    'Xbox 360 Controller':
        {0:'A', 1:'B', 2:'X', 3:'Y', 4:'LB', 5:'RB', 6:'Back', 7:'Start', 8:'L Stick In', 20:'LT',
        9:'R Stick In', 10:'Guide Button', 16:'Up', 17:'Down', 18:'Left', 19:'Right', 21:'RT'},
    'DualSense Wireless Controller':
        {0:'Cross', 1:'Circle', 2:'Square', 3:'Triangle', 4:'Share', 5:'PS Button', 6:'Options', 7:'L3', 8:'R3', 20:'L2',
        9:'L1', 10:'R1', 11:'Up', 12:'Down', 13:'Left', 14:'Right', 15:'Touch Pad Click', 21:'R2'}
}

			