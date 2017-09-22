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
    "i": (0, "lead upper"),
    "o": (0, "rear upper"),
    "J": (0, "body jab"),
    "K": (0, "body cross"),
    "L": (0, "body lead hook"),
    ":": (0, "body rear hook"),
    "I": (0, "body lead upper"),
    "O": (0, "body rear upper"),
    "landed-j": (1, "jab"),
    "landed-k": (1, "cross"),
    "landed-l": (1, "lead hook"),
    "landed-;": (1, "rear hook"),
    "landed-i": (1, "lead upper"),
    "landed-o": (1, "rear upper"),
    "landed-J": (1, "body jab"),
    "landed-K": (1, "body cross"),
    "landed-L": (1, "body lead hook"),
    "landed-:": (1, "body rear hook"),
    "landed-I": (1, "body lead upper"),
    "landed-O": (1, "body rear upper"),
}

def start(fighter, round, start_offset, time_scale):
    state = {}
    state['fighter'] = fighter
    state['round'] = round
    state['start_time'] = datetime.datetime.now()
    state['stats'] = []
    state['paused'] = False
    state['pause_elapsed_seconds'] = 0
    state['pointer'] = 0
    state['time_scale'] = time_scale
    state['start_offset'] = start_offset * time_scale

    print banner
    print "-----------------------------"
    print "Recording..."

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                onQuit(state)
                return

            if event.type == KEYDOWN:
                if event.key == K_q:
                    onQuit(state)
                    return

                if event.key == K_p:
                    onTogglePause(state)
                    break

                if event.key == K_BACKSPACE:
                    onTimeTravel(state)
                    break

                if state['paused'] and not timeTraveling(state):
                    print "Paused (p to resume)"
                    break

                key = event.unicode
                pressed_keys = pygame.key.get_pressed()

                if pressed_keys[pygame.K_SPACE]:
                    key = 'body-' + key

                if pressed_keys[pygame.K_f]:
                    key = 'landed-' + key

                if key in key_map:
                    punch_type = key_map[key]
                    onKeyPress(state, punch_type)

def onQuit(state):
    string_stats = []
    for stat in state['stats']:
        string_stats.append(",".join(stat))

    joined = "\n".join(string_stats)
    print joined

    path = "./stats/{}-round-{}.csv".format(state['fighter'], state['round'])
    fo = open(path, "a")
    fo.write(joined)

    pygame.quit()
    exit()

def onTogglePause(state):
    if state['paused']:
        resume(state)
    else:
        pause(state)

def resume(state):
    state['paused'] = False
    elapsed_time_seconds = (datetime.datetime.now() - state['pause_start']).total_seconds()
    state['pause_elapsed_seconds'] += elapsed_time_seconds
    print "Resumed"
    return

def pause(state):
    state['paused'] = True
    state['pause_start'] = datetime.datetime.now()
    print "Paused"

def onTimeTravel(state):
    state['pointer'] = max(state['pointer'] - 1, 0);
    time_in_past = (len(state['stats'])) - state['pointer'];
    print "{} {} in the past".format(time_in_past, "punches" if time_in_past > 1 else "punch")

def onTimeTravelForward(state):
    state['pointer'] += 1
    time_in_past = (len(state['stats'])) - state['pointer'];

    if time_in_past > 0:
        print "Rewrote Stat"
        print "{} {} left to go".format(time_in_past, "punches" if time_in_past > 1 else "punch")
    else:
        print "Up to date"

def timeTraveling(state):
    diff = max(len(state['stats']), 0) - state['pointer']
    return diff > 0

def onKeyPress(state, punch_type):
    if timeTraveling(state):
        diff = state['stats'][state['pointer']][0]
        stat = [diff, state['round'], state['fighter'], str(punch_type[0]), punch_type[1]]
        state['stats'][state['pointer']] = stat

        print stat
        onTimeTravelForward(state)
    else:
        now = datetime.datetime.now()
        diff = (now - state['start_time']).total_seconds() + state['start_offset']
        pause_adjusted = diff - state['pause_elapsed_seconds']
        time_scale_adjusted = pause_adjusted / state['time_scale']
        rounded = int(round(time_scale_adjusted))

        stat = [str(rounded), state['round'], state['fighter'], str(punch_type[0]), punch_type[1]]
        state['stats'].append(stat)
        state['pointer'] += 1
        print stat


def main():
    if len(sys.argv) < 3:
        print "smartstats.py fighter round start_offset time_scale"
        exit()

    fighter = sys.argv[1]
    round = sys.argv[2]
    offset = int(sys.argv[3])
    time_scale = int(sys.argv[4]) if len(sys.argv) >= 5 else 1

    pygame.init()
    screen = pygame.display.set_mode((200, 200))

    start(fighter, round, offset, time_scale)

if __name__ == "__main__":
    main()
