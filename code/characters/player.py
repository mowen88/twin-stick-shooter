import pygame, pytweening
from pygame.math import Vector2 as vec2
from settings import *
from support import tween
from timer import Timer
from characters.state_machine import BaseState
from characters.npc import NPC


class Player(NPC):
    def __init__(self, game, scene, groups, pos, path, z=2):
        super().__init__(game, scene, groups, pos, path, z)
        # attributes

        # timers
        self.timers = {'jump_buffer':Timer(0.10),'jump':Timer(0.2),'dash':Timer(3600),'attack':Timer(0.8),'melee':Timer(3000),'fall':Timer(6000)}
        self.state = Idle(self)
        self.speed = 120
        self.jump_height = 260

    def input(self):
        if ACTIONS['Right']: 
            self.move_x(1)
        elif ACTIONS['Left']:
            self.move_x(-1)
        else:
            self.move_x(0)

class OnGround(BaseState):
    def __init__(self, player):
        super().__init__(player)
        self.previous_facing = player.facing

    def state_logic(self, player):
        pass

    def update(self, dt, player):
        player.animate(dt, self.state_name, self.animation_loop)
        player.input()
        player.apply_gravity(dt)
        player.movement(dt)

class Idle(OnGround):
    def __init__(self, player):
        super().__init__(player)
        # player.direction.x = 0
        player.jump_count = 0
        player.dash_count = 0
        self.animation_loop = False

    def state_logic(self, player):

        if player.facing != self.previous_facing:
            player.set_state(Turn(player))

        elif player.direction.x != 0:
            player.set_state(Run(player))

        elif ACTIONS['Jump']: 
            player.set_state(Jump(player))

        elif ACTIONS['Attack']:
            player.set_state(LeftHook(player))

class Run(OnGround):
    def __init__(self, player):
        super().__init__(player)

    def state_logic(self, player):

        if player.facing != self.previous_facing:
            player.set_state(Turn(player))

        elif player.direction.x == 0:
            player.set_state(Idle(player))
        
        elif player.direction.y > 0:
            player.set_state(Fall(player))

        elif ACTIONS['Jump']:
            player.set_state(Jump(player))

        elif ACTIONS['Attack']:
            return LeftHook(player)

class Turn(OnGround):
    def __init__(self, player):
        super().__init__(player)

    def state_logic(self, player):

        if player.facing != self.previous_facing:
            return Turn(player)

        elif player.direction.y > 0:
            player.set_state(Fall(player))

        elif ACTIONS['Jump']:
            player.set_state(Jump(player))

        elif ACTIONS['Attack'] and player.on_ground:
            return LeftHook(player)

        elif player.frame_index > len(player.animations[self.state_name])-1:
            player.set_state(Idle(player))

class Land(Turn):
    def __init__(self, player):
        super().__init__(player)
        self.animation_loop = False

class LeftHook(OnGround):
    def __init__(self, player):
        super().__init__(player)
        ACTIONS['Attack'] = 0
        self.combo_pending = False
        #player.direction.x = PLAYER_STATS['attack_lunge_speed']
        self.timer = player.timers['attack']
        self.timer.stop()
        self.timer.start()
        self.initial_speed = 60
        self.direction = vec2(player.facing * self.initial_speed, 0)

    def state_logic(self, player):

        if not self.timer.running:
            if self.combo_pending:
                player.set_state(LeftHook(player))
            else:
                player.set_state(Idle(player))

        elif ACTIONS['Attack']:
            self.combo_pending = True

    def update(self, dt, player):
        tween(self.direction, self.timer, dt, player)
        player.movement(dt)
        player.animate(dt, self.state_name, False)

class Fall(BaseState):
    def __init__(self, player):
        super().__init__(player)
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
                player.set_state(Jump(player))
            else:
                player.set_state(Land(player))

    def update(self, dt, player):
        player.animate(dt, self.state_name, False)
        player.input()
        player.apply_gravity(dt)
        player.movement(dt)

class Jump(BaseState):
    def __init__(self, player):
        super().__init__(player)
        player.timers['jump'].start()

    def state_logic(self, player):

        if player.direction.y >= 0:
            player.timers['jump'].stop()
            player.set_state(Fall(player))

        elif not ACTIONS['Jump']:
            player.timers['jump'].stop()
            if player.direction.y < 0:
                player.direction.y = 0      

    def update(self, dt, player):
        player.jump()
        player.animate(dt, self.state_name, False)
        player.input()
        player.apply_gravity(dt)
        player.movement(dt)



        