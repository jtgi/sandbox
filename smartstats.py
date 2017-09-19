# -*- coding: utf-8 -*-
import sys, tty, time, datetime, termios
import sys
import time
import random

import pygame
from pygame.locals import *

banner = """
    #### ##   ## ######## ####### ########      #### ######## ######## ########   ####
   ###   ### ###       ##       ##   ###       ###      ###         ##    ###    ###
   ###   #######  #######  ######    ###       ###      ###    #######    ###    ###
   ###   ## # ##  ###  ##  ##  ##    ###       ###      ###    ###  ##    ###    ###
#####    ##   ##  ###  ##  ##   ##   ###    #####       ###    ###  ##    ### ####
"""

key_map = {
    "j": (0, "jab"),
    "k": (0, "cross"),
    "l": (0, "lead hook"),
    ";": (0, "rear hook"),
    "u": (0, "lead upper"),
    "i": (0, "rear upper"),
    "body-j": (0, "body jab"),
    "body-k": (0, "body cross"),
    "body-l": (0, "body lead hook"),
    "body-;": (0, "body rear hook"),
    "body-u": (0, "body lead upper"),
    "body-i": (0, "body rear upper"),
    "landed-j": (1, "jab"),
    "landed-k": (1, "cross"),
    "landed-l": (1, "lead hook"),
    "landed-;": (1, "rear hook"),
    "landed-u": (1, "lead upper"),
    "landed-i": (1, "rear upper"),
    "landed-body-j": (1, "body jab"),
    "landed-body-k": (1, "body cross"),
    "landed-body-l": (1, "body lead hook"),
    "landed-body-;": (1, "body rear hook"),
    "landed-body-u": (1, "body lead upper"),
    "landed-body-i": (1, "body rear upper"),
}

def start(fighter, round, start_offset):
    data = {}
    data['fighter'] = fighter
    data['round'] = round
    data['start_offset'] = int(start_offset)
    data['start_time'] = datetime.datetime.now()
    data['stats'] = []

    print banner
    print "-----------------------------"
    print "Recording..."

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                onQuit(data)

            if event.type == KEYDOWN:
                if event.key == K_q:
                    onQuit(data)

                key = event.unicode
                pressed_keys = pygame.key.get_pressed()

                if pressed_keys[pygame.K_SPACE]:
                    key = 'body-' + key

                if pressed_keys[pygame.K_f]:
                    key = 'landed-' + key

                if key in key_map:
                    punch_type = key_map[key]
                    onKeyPress(data, punch_type)

def onQuit(data):
    joined = "\n".join(data['stats'])
    print joined

    path = "./stats/{}-round-{}.csv".format(data['fighter'], data['round'])
    fo = open(path, "a")
    fo.write(joined)

    pygame.quit()
    exit()

def onKeyPress(data, punch_type):
    now = datetime.datetime.now()
    diff = str(int(round((now - data['start_time']).total_seconds())))

    stat = "{},{},{},{},{}".format(diff, data['round'], data['fighter'], punch_type[0], punch_type[1])
    print stat

    data['stats'].append(stat)

def main():
    if len(sys.argv) < 3:
        print "smartstats.py fighter round [start_offset]"
        exit()

    fighter = sys.argv[1]
    round = int(sys.argv[2])
    offset = int(sys.argv[3]) if len(sys.argv) >= 4 else 0

    pygame.init()
    screen = pygame.display.set_mode((100, 50))

    start(fighter, round, offset)

if __name__ == "__main__":
    main()
