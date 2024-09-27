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

FONT = '../assets/font/DePixelHalbfett.ttf'
#FONT = '../assets/font/BMSPA___.ttf'
#FONT = '../assets/homespun.ttf'

VOLUME = {'Master Volume':0.5,'Sound Volume':0.5,'Music Volume':0.5}
DEFAULT_VOLUME = {'Master Volume':0.5,'Sound Volume':0.5,'Music Volume':0.5}

COLOURS = {
			'purple':(69,41,63), 'cyan':(143,248,226), 'black':(46,34,47), 'white':(255,255,255), 'olive':(49,54,56),'pale_yellow':(201,204,161),
			'yellow':(202,160,90),'orange':(174,106,71), 'deep_red':(110,39,39), 'red':(179,56,49), 'burgundy':(84,51,68), 'grey':(81,82,98),'green':(22,90,76),
			'pale_green':(142,160,145), 'brown':(110,39,39), 'salmon':(158,69,57), 'dark_pink':(122,48,69), 'lavender':(107,62,117), 'blue':(72,74,119),
			'deep_blue':(50,51,83), 'teal':(11,138,143), 'hot_pink':(240,79,120)
			}

DEADZONE = 0.2
TRIGGER_DEADZONE = 0.5

KEY_MAP = {
			'Left':[pygame.K_LEFT], 'Right':[pygame.K_RIGHT], 'Up':[pygame.K_UP], 'Down':[pygame.K_DOWN],
			'Jump':[pygame.K_z], 'Attack':[pygame.K_x], 'Dash':[pygame.K_c], 'Inventory':[pygame.K_i], 'Pause':[pygame.K_SPACE],
			'Left Click':[1],'Confirm':[pygame.K_SPACE, pygame.K_RETURN], 'Back':[pygame.K_ESCAPE, pygame.K_BACKSPACE],
			'Reset Defaults':[pygame.K_TAB],'Menu Up':[pygame.K_UP, pygame.K_w], 'Menu Down':[pygame.K_DOWN, pygame.K_s],
			'Menu Left':[pygame.K_LEFT, pygame.K_a], 'Menu Right':[pygame.K_RIGHT, pygame.K_d]
			}

DEFAULT_KEY_MAP = {
			'Left':[pygame.K_LEFT], 'Right':[pygame.K_RIGHT], 'Up':[pygame.K_UP], 'Down':[pygame.K_DOWN],
			'Jump':[pygame.K_z], 'Attack':[pygame.K_x], 'Dash':[pygame.K_c], 'Inventory':[pygame.K_i], 'Pause':[pygame.K_SPACE],
			'Left Click':[1],'Confirm':[pygame.K_SPACE, pygame.K_RETURN], 'Back':[pygame.K_ESCAPE, pygame.K_BACKSPACE],
			'Reset Defaults':[pygame.K_TAB],'Menu Up':[pygame.K_UP, pygame.K_w], 'Menu Down':[pygame.K_DOWN, pygame.K_s],
			'Menu Left':[pygame.K_LEFT, pygame.K_a], 'Menu Right':[pygame.K_RIGHT, pygame.K_d]
			}

ACTIONS = {'Menu Up':0, 'Menu Down':0, 'Menu Left':0, 'Menu Right':0, 'Up':0, 'Down':0, 'Left':0, 'Right':0,
			'Jump':0, 'Attack':0, 'Dash':0, 'Inventory':0, 'Pause':0, 'Confirm':0, 'Back':0,'Left Click':0,'Reset Defaults':0}

                  
BUTTON_MAPS = {
			'Mouse':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':4, 'Pause':1, 'Up':0, 'Down':0,'Left':0, 'Right':0,
				'Menu Up':0, 'Menu Down':0,'Menu Left':0, 'Menu Right':0, 'Confirm':1, 'Back':3,'Reset Defaults':6},
			'Nintendo Switch Pro Controller':
				{'Jump':1, 'Attack':0, 'Dash':21, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			'PS4 Controller':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			'Xbox 360 Controller':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':8, 'Pause':7, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			'DualSense Wireless Controller':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			}

DEFAULT_BUTTON_MAPS = {
			'Mouse':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':4, 'Pause':1, 'Up':0, 'Down':0,'Left':0, 'Right':0,
				'Menu Up':0, 'Menu Down':0,'Menu Left':0, 'Menu Right':0, 'Confirm':1, 'Back':3,'Reset Defaults':6},
			'Nintendo Switch Pro Controller':
				{'Jump':1, 'Attack':0, 'Dash':21, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			'PS4 Controller':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			'Xbox 360 Controller':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':8, 'Pause':7, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			'DualSense Wireless Controller':
				{'Jump':0, 'Attack':1, 'Dash':21, 'Inventory':4, 'Pause':6, 'Up':11, 'Down':12,'Left':13, 'Right':14,
				'Menu Up':11, 'Menu Down':12,'Menu Left':13, 'Menu Right':14, 'Confirm':0, 'Back':1,'Reset Defaults':3},
			}

AXIS_PRESSED = {'Left Stick':(0,0),'Right Stick':(0,0),'Left Trigger':0,'Right Trigger':0, 'D-Pad':(0,0)}

BUTTON_NAMES = {
	'Mouse':
		{1:'Left Click',2:'Scroll Btn',3:'Right Click',4:'Scroll Up',5:'Scroll Down',6:'Side Btn 1',7:'Side Btn 2'},
    'Nintendo Switch Pro Controller': 
    	{0:'A', 1:'B', 2:'X', 3:'Y', 4:'-', 5:'Home', 6:'+', 7:'L Stick In', 8:'R Stick In', 9:'L', 20:'ZL',
        10:'R', 11:'Up', 12:'Down', 13:'Left', 14:'Right', 15:'Capture', 21:'ZR'},
    'PS4 Controller':
        {0:'Cross', 1:'Circle', 2:'Square', 3:'Triangle', 4:'Share', 5:'PS Button', 6:'Options', 7:'L3', 8:'R3', 20:'L2',
        9:'L1', 10:'R1', 11:'Up', 12:'Down', 13:'Left', 14:'Right', 15:'Touch Pad Click', 21:'R2'},
    'Xbox 360 Controller':
        {0:'A', 1:'B', 2:'X', 3:'Y', 4:'LB', 5:'RB', 6:'Back', 7:'Start', 8:'L Stick In', 20:'LT',
        9:'R Stick In', 10:'Guide Button', 11:'Up', 12:'Down', 13:'Left', 14:'Right', 21:'RT'},
    'DualSense Wireless Controller':
        {0:'Cross', 1:'Circle', 2:'Square', 3:'Triangle', 4:'Share', 5:'PS Button', 6:'Options', 7:'L3', 8:'R3', 20:'L2',
        9:'L1', 10:'R1', 11:'Up', 12:'Down', 13:'Left', 14:'Right', 15:'Touch Pad Click', 21:'R2'}
}

			