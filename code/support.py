import pygame, sys, os, json
from settings import *

def get_csv_layer(path):
    grid = []
    with open(path) as layout:
        layer = reader(layout, delimiter = ',')
        for row in layer:
            grid.append(list(row))
        return grid

def get_images(path):
    images = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        img = pygame.image.load(full_path).convert_alpha()
        images.append(img)
    return images

def get_animations(path):
    animations = {}
    for file_name in os.listdir(path):
        animations.update({file_name:[]})
        full_path = os.path.join(path, file_name)
    return animations

def get_csv_layer(path):
    grid = []
    with open(path) as layout:
        layer = reader(layout, delimiter = ',')
        for row in layer:
            grid.append(list(row))
        return grid

def write_data(name, data):
    with open(name, "w") as write_save_file:
        json.dump(data, write_save_file)


def read_data(name, data):
    with open(name, 'r') as read_save_file:
        save_json = json.load(read_save_file)
        data.update(save_json)
