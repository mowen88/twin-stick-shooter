import pygame, pytweening
from pygame.math import Vector2 as vec2
from settings import *
from timer import Timer
from characters.npc import NPC

class Player(NPC):
    def __init__(self, game, scene, groups, pos, path, z=2):
        super().__init__(game, scene, groups, pos, path, z)
        # attributes

        # timers
        self.timers = {'jump_buffer':Timer(0.15),'jump':Timer(0.2),'dash':Timer(3600),'attack':Timer(0.8),'melee':Timer(3000),'fall':Timer(6000)}
        self.state = Idle(self)
        self.speed = 120

    def input(self):
        if ACTIONS['Right']: 
            self.direction.x = 1
            self.facing = 1
        elif ACTIONS['Left']:
            self.direction.x = -1
            self.facing = -1
        else:
            self.direction.x = 0 

class Idle:
    def __init__(self, player):
        player.direction.x = 0
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
        player.animate(dt, 'idle', False)
        player.input()
        player.apply_gravity(dt)
        player.direction.x *= player.speed
        player.movement(dt)

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


    def update(self, dt, player):
        player.animate(dt, 'run')
        player.input()
        player.apply_gravity(dt)
        player.direction.x *= player.speed
        player.movement(dt)

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


    def update(self, dt, player):
        player.animate(dt, 'turn')
        player.input()
        player.apply_gravity(dt)
        player.direction.x *= player.speed
        player.movement(dt)

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
        player.animate(dt, 'fall', False)
        player.input()
        player.apply_gravity(dt)
        player.direction.x *= player.speed
        player.movement(dt)

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
        player.animate(dt, 'jump', False)
        player.input()
        player.apply_gravity(dt)
        player.direction.x *= player.speed
        player.movement(dt)

class LeftHook:
    def __init__(self, player):
        player.frame_index = 0
        ACTIONS['Attack'] = 0
        self.combo_pending = False
        self.speed = 40
        #player.direction.x = PLAYER_STATS['attack_lunge_speed']
        self.timer = player.timers['attack']
        self.timer.stop()
        self.timer.start()

    def tween(self, dt, player):
        self.timer.update(dt)
        if self.timer.running:
            progress = self.timer.counter / self.timer.duration
            tween_progress = pytweening.easeOutQuad(1 - progress)
            target_direction = vec2(player.facing * self.speed, 0)

            player.direction.x = target_direction.x * tween_progress
            player.direction.y = target_direction.y * tween_progress

        player.hitbox.centerx += player.direction.x * dt
        player.rect.centerx = player.hitbox.centerx 
        player.collisions('x')
    
        player.hitbox.centery += player.direction.y * dt
        player.rect.centery = player.hitbox.centery
        player.collisions('y')

        player.update_raycasts()

    def state_logic(self, player):

        if ACTIONS['Attack']:
            self.combo_pending = True
        
        if not self.timer.running:
            if self.combo_pending:
                return RightHook(player)
            else:
                return Idle(player)

    def update(self, dt, player):
        self.tween(dt, player)
        player.animate(dt, 'left_hook', False)

class RightHook(LeftHook):
    def __init__(self, player):
        super().__init__(player)

    def state_logic(self, player):

        if ACTIONS['Attack']:
            self.combo_pending = True
        
        if not self.timer.running:
            if self.combo_pending:
                return RightHook(player)
            else:
                return Idle(player)

    def update(self, dt, player):
        self.tween(dt, player)
        player.animate(dt, 'right_hook', False)

        