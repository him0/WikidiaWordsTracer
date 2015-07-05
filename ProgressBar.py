#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


class ProgressBar(object):

    def __init__(self, maxValue=0, maxLength=30):
        self.__maxValue = maxValue
        self.__maxLength = maxLength
        self.value = 0
        self.display()

    def display(self):
        progress = self.value / self.__maxValue
        sys.stderr.write('\r\033[K' + self.getProgressbarString(progress))

    def getProgressbarString(self, progress):
        barLength = int(self.__maxLength * progress)

        bar = ""
        bar += '[' + '=' * barLength
        bar += ('>' if barLength < self.__maxLength else '')
        bar += ' ' * (self.__maxLength - barLength)
        bar += '] %.1f%%' % (progress * 100.)

        return(bar)

    def update(self):
        sys.stderr.flush()
        self.value = self.value + 1
        self.display()
        sys.stderr.flush()
        if self.value == self.__maxValue - 1:
            #sys.stderr.write('\n')#終了したら改行
            sys.stderr.flush()

if __name__ == "__main__":
    import time

    bar = ProgressBar(150)
    for x in range(0,150):
        time.sleep(0.05)
        bar.update()
