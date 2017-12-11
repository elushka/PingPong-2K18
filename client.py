#!/usr/bin/env python
#EC441 Team Brian, Ricky, Erostin

# Do not generate bytecodes in developer mode
import math, sys, socket
sys.dont_write_bytecode = True


import lib.mainwindow as mainwindow
import lib.settings as settings
import pyglet


if __name__ == "__main__":
    mainwindow.MainWindow(width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT)
    pyglet.app.run()
