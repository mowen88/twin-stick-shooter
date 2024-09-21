import pygame, math
from pygame.math import Vector2 as vec2
from entities import Entity
from settings import *

class InputManager:
    def __init__(self, game):
        self.game = game
        self.compatible_joysticks = list(BUTTON_NAMES.keys())
        self.joystick = None
        self.joystick_name = None
        self.control_type = self.update_control_type()
        self.axis_flags = AXIS_PRESSED.copy()
        self.bind_mode = False
        self.new_bind = {'Keyboard':0,'Xbox 360 Controller':-1,'DualSense Wireless Controller':-1}
        self.mouse_pos = vec2()
        pygame.mouse.set_visible(False)

    def update_control_type(self):
        self.control_type = self.joystick.get_name() if self.joystick is not None else'Keyboard'

    def add_joystick(self, joy_index):
        self.joystick = pygame.joystick.Joystick(joy_index)
        self.joystick.init()
        self.joystick_name = self.joystick.get_name()
        self.update_control_type()
        print(f'{self.joystick.get_name()}, index {self.joystick.get_instance_id()}, power level: {self.joystick.get_power_level()} is connected')

    def remove_joystick(self):
        if self.joystick is not None:
            self.joystick.quit()
        self.joystick = None
        self.update_control_type()
        AXIS_PRESSED = {'Left Stick':(0,0),'Right Stick':(0,0),'Left Trigger':0,'Right Trigger':0, 'D-Pad':(0,0)}

    def get_hats(self):

        if not (self.game.block_input or self.bind_mode) and self.joystick:
          pass

    def get_triggers(self):

        if not self.game.block_input:
        
            triggers = {'Left Trigger': 20, 'Right Trigger': 21}
            button_map = BUTTON_MAPS[self.joystick_name]

            for trigger, trigger_id in triggers.items():
                # Get the current trigger value (from axis)
                current_value = AXIS_PRESSED[trigger]
                new_trigger_value = 1 if current_value > TRIGGER_DEADZONE else 0
                # Trigger pressed logic
                if self.axis_flags[trigger] == 0 and new_trigger_value == 1:
                    if self.bind_mode: self.new_bind[self.joystick_name] = trigger_id

                    for action, value in button_map.items():
                        if trigger_id == value:
                            ACTIONS[action] = 1

                # Trigger released logic
                if self.axis_flags[trigger] == 1 and new_trigger_value == 0:
                    for action, value in button_map.items():
                        if trigger_id == value:
                            ACTIONS[action] = 0

                self.axis_flags[trigger] = new_trigger_value


    def get_input(self, events):

        print(self.bind_mode)

        for event in events:

            if event.type == pygame.QUIT:
                self.game.quit()

            if self.joystick:
                
                if event.type == pygame.JOYDEVICEREMOVED:
                    self.remove_joystick()

                button_map = BUTTON_MAPS[self.joystick_name]

                if event.type == pygame.JOYBUTTONDOWN:
                    if self.bind_mode: self.new_bind[self.joystick_name] = event.button
                    #self.new_bind = self.update_binding(event.button, guid)
                    for action, value in button_map.items():
                        if value == event.button:
                            ACTIONS[action] = 1

                if event.type == pygame.JOYBUTTONUP:
                    for action, value in button_map.items():
                        if value == event.button:
                            ACTIONS[action] = 0

                # if event.type == pygame.JOYHATMOTION:
                #     self.direction = (event.value[0], -event.value[1])

                if event.type == pygame.JOYHATMOTION:
                    self.update_control_type(self.joystick_name)
                    direction = event.value
                    AXIS_PRESSED['D-Pad'] = direction

                if event.type == pygame.JOYAXISMOTION:
                    # Get left stick axes
                    ls_x = self.joystick.get_axis(0)
                    ls_y = self.joystick.get_axis(1)
                    ls_x = ls_x if abs(ls_x) > DEADZONE else 0
                    ls_y = ls_y if abs(ls_y) > DEADZONE else 0
                    left_stick = (ls_x, ls_y)

                    # Get right stick axes
                    rs_x = self.joystick.get_axis(2)
                    rs_y = self.joystick.get_axis(3)
                    rs_x = rs_x if abs(rs_x) > DEADZONE else 0
                    rs_y = rs_y if abs(rs_y) > DEADZONE else 0 
                    right_stick = (rs_x, rs_y)     

                    # Normalize trigger values
                    lt_normalised = (self.joystick.get_axis(4) + 1) / 2
                    left_trigger = lt_normalised if lt_normalised > DEADZONE else 0
                    rt_normalised = (self.joystick.get_axis(5) + 1) / 2
                    right_trigger = rt_normalised if rt_normalised > DEADZONE else 0

                    AXIS_PRESSED.update({'Left Stick':left_stick,'Right Stick':right_stick,
                                        'Left Trigger':left_trigger,'Right Trigger':right_trigger})
                self.get_triggers()

            else:
                self.mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.JOYDEVICEADDED:
                    self.add_joystick(event.device_index)
                    self.cursor_pos = vec2()

                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0: val = 4
                    else: val = 5
                    if self.bind_mode: self.new_bind['Keyboard'] = val
                    
                    for action, value in KEY_MAP.items():
                        if val in value:
                            ACTIONS[action] = 1 

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bind_mode: self.new_bind['Keyboard'] = event.button#MOUSE_BUTTON_NAMES[event.button]
                    
                    for action, value in KEY_MAP.items():
                        if event.button in value:
                            ACTIONS[action] = 1      

                if event.type == pygame.MOUSEBUTTONUP:
                    #print(event.button)
                    for action, value in KEY_MAP.items():
                        if event.button in value:
                            ACTIONS[action] = 0

                if event.type == pygame.KEYDOWN:
                    if self.bind_mode: self.new_bind['Keyboard'] = event.key

                    for action, value in KEY_MAP.items():
                        if event.key in value:
                            ACTIONS[action] = 1

                if event.type == pygame.KEYUP:
                    for action, value in KEY_MAP.items():
                        if event.key in value:
                            ACTIONS[action] = 0

                

                
