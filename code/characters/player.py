import pygame
from settings import *
from timer import Timer
from characters.npc import NPC

class Player(NPC):
    def __init__(self, game, scene, groups, pos, path, z=2):
        super().__init__(game, scene, groups, pos, path, z)

        # attributes

        # timers
        self.timers = {'jump_buffer':Timer(0.15),'jump':Timer(0.2),'dash':Timer(3600),'melee':Timer(3000),'fall':Timer(6000)}
        self.state = Idle(self)

    def input(self):
        if ACTIONS['Right']: 
            self.direction.x = 1
            self.facing = 1
        elif ACTIONS['Left']:
            self.direction.x = -1
            self.facing = 0
        else:
            self.direction.x = 0 

class Idle:
    def __init__(self, player):
        player.frame_index = 0
        self.previous_facing = player.facing
        player.jump_count = 0
        player.dash_count = 0

    def state_logic(self, player):
        if player.direction.x != 0:
            if player.facing != self.previous_facing:
                return Turn(player)
            else:
                return Run(player)

        if player.on_ground:
            if ACTIONS['Jump']: 
                return Jump(player)
            elif ACTIONS['Attack'] and player.on_ground:
                return LeftHook(player)

        # if SAVE_DATA['Items']['Dash'] and ACTIONS['Dash'] and not player.dash_timer.running:
        #     return Dash(player)

        # if ACTIONS['Attack'] and not player.melee_timer.running:
        #     if player.game.keys[KEY_MAP['Up']] or player.game.controller[PS4_BUTTON_MAP['Up']] or PS4_AXIS_MAP['Up']:
        #         return MeleeUp(player)
        #     else:
        #         return Melee(player)

    def update(self, dt, player):
        player.animate('idle',False)
        player.input()
        player.move(dt, player.max_fall_speed)

class Run(Idle):
    def __init__(self, player):
        Idle.__init__(self, player)

    def state_logic(self, player):

        if player.facing != self.previous_facing:
            return Turn(player)
        
        if player.direction.x == 0:
            return Idle(player)

        if player.direction.y > 0:
            return Fall(player)

        if player.on_ground:
            if ACTIONS['Jump']: 
                return Jump(player)
            elif ACTIONS['Attack'] and player.on_ground:
                return LeftHook(player)

        # if SAVE_DATA['Items']['Dash'] and ACTIONS['Dash'] and player.dash_count == 0 and not player.dash_timer.running:
        #     return Dash(player) 

        # if ACTIONS['Attack'] and not player.melee_timer.running:
        #     if player.game.keys[KEY_MAP['Up']] or player.game.controller[PS4_BUTTON_MAP['Up']] or PS4_AXIS_MAP['Up']:
        #         return MeleeUp(player)
        #     else:
        #         return Melee(player)

    def update(self, dt, player):
        player.animate('run')
        player.input()
        player.move(dt, player.max_fall_speed)

class Turn(Idle):
    def __init__(self, player):
        Idle.__init__(self, player)

    def state_logic(self, player):

        if player.frame_index >= len(player.animations['turn'])-1:
            return Run(player)

        if player.direction.y > 0:
            return Fall(player)

        if player.on_ground:
            if ACTIONS['Jump']: 
                return Jump(player)
            elif ACTIONS['Attack'] and player.on_ground:
                return LeftHook(player)

        # if SAVE_DATA['Items']['Dash'] and ACTIONS['Dash'] and player.dash_count == 0 and not player.dash_timer.running:
        #     return Dash(player)

        # if ACTIONS['Attack'] and not player.melee_timer.running:
        #     return Melee(player)

    def update(self, dt, player):
        player.animate('turn')
        player.input()
        player.move(dt, player.max_fall_speed)

class Fall:
    def __init__(self, player):
        player.frame_index = 0
        ACTIONS['Jump'] = 0

    def state_logic(self, player):

        # if SAVE_DATA['Items']['Wall Climb'] and player.hit_wall and not ACTIONS['Down']:
        #     return WallSlide(player)

        if ACTIONS['Jump']:
            player.timers['jump_buffer'].start()
            ACTIONS['Jump'] = 0

        if player.on_ground:
            if player.timers['jump_buffer'].running:
                ACTIONS['Jump'] = 1
                return Jump(player)
            else:
                return Idle(player)

    def update(self, dt, player):
        player.animate('fall', False)
        player.input()
        player.move(dt, player.max_fall_speed)

class Jump:
    def __init__(self, player):
        player.timers['jump'].start()
        player.frame_index = 0

    def state_logic(self, player):

        if player.direction.y >= 0:
            player.timers['jump'].stop()
            return Fall(player)

        elif not ACTIONS['Jump']:
            player.timers['jump'].stop()
            if player.direction.y < 0:
                player.direction.y = 0      

    def update(self, dt, player):
        player.jump()
        player.animate('jump', False)
        player.input()
        player.move(dt, player.max_fall_speed)

class LeftHook:
    def __init__(self, player):
        player.frame_index = 0
        ACTIONS['Attack'] = 0
        self.combo_pending = False

    def state_logic(self, player):

        if ACTIONS['Attack']:
            self.combo_pending = True
        
        if player.frame_index >= len(player.animations['left_hook'])-1:
            if self.combo_pending:
                return RightHook(player)
            else:
                return Idle(player)

    def update(self, dt, player):
        player.animate('left_hook', False)
        player.input()
        #player.move(dt, player.max_fall_speed)

class RightHook:
    def __init__(self, player):
        player.frame_index = 0
        ACTIONS['Attack'] = 0
        self.combo_pending = False

    def state_logic(self, player):

        if ACTIONS['Attack']:
            self.combo_pending = True
        
        if player.frame_index >= len(player.animations['right_hook'])-1:
            if self.combo_pending:
                return LeftHook(player)
            else:
                return Idle(player)

    def update(self, dt, player):
        player.animate('right_hook', False)
        player.input()
        #player.move(dt, player.max_fall_speed)

        