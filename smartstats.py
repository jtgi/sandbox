# -*- coding: utf-8 -*-
import sys, tty, time, datetime, termios

data = {}
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

punch_map = {
  "d": (0, "jab"),
  "s": (0, "cross"),
  "f": (0, "lead hook"),
  "a": (0, "rear hook"),
  "c": (0, "lead upper"),
  "x": (0, "rear upper"),
  "D": (0, "body jab"),
  "S": (0, "body cross"),
  "F": (0, "body lead hook"),
  "A": (0, "body rear hook"),
  "C": (0, "body lead upper"),
  "X": (0, "body rear upper"),
  "k": (1, "jab"),
  "l": (1, "cross"),
  "j": (1, "lead hook"),
  ";": (1, "rear hook"),
  "m": (1, "lead upper"),
  ",": (1, "rear upper"),
  "K": (1, "body jab"),
  "L": (1, "body cross"),
  "J": (1, "body lead hook"),
  ":": (1, "body rear hook"),
  "M": (1, "body lead upper"),
  "<": (1, "body rear upper"),
}

def onKeyPress(c):
  if c == 'q':
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    joined = "\n".join(data['stats'])
    print joined

    filename = "{}-round-{}.csv".format(data['fighter'], data['round'])
    fo = open(filename, "a")
    fo.write(joined)

    exit()
  else:
    now = datetime.datetime.now()
    diff = now - data['start_time']
    min, sec = divmod(diff.days * 86400 + diff.seconds, 60)

    if sec + data['start_offset'] > 60:
      min = min + 1

    sec = (sec + data['start_offset']) % 60
    seconds = "{}.{}".format(min, sec)

    if str(c) in punch_map:
      stat = "{},{},{},{},{}".format(seconds, data['round'], data['fighter'], punch_map[str(c)][0], punch_map[str(c)][1])
      print stat
      data['stats'].append(stat)

def main():
  data['fighter'] = raw_input("Fighter: ")
  data['round'] = raw_input("Round: ")
  data['start_offset'] = int(raw_input("Start offset (s): "))
  data['start_time'] = datetime.datetime.now()
  data['stats'] = []
  #data['stats'] = ["Time,Round,Fighter,Landed,Punch"]

  tty.setraw(fd)

  while True:
    ch = sys.stdin.read(1)
    onKeyPress(ch)

if __name__ == "__main__":
      main()
