#!/usr/bin/python -t
# -*- coding: utf-8 -*-

"""noteguess.py

Monday, August 26 2013
"""

import os
import sys
import re

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt as qt

from util import ASC2UNI


class NoteGuessWidget(QGroupBox):
    """Note-labeled button array + Update button.
    """
    def __init__(self, parent=None):
        super(NoteGuessWidget, self).__init__('Note Drill', parent)
        vLayout = QVBoxLayout(self)
        gLayout = QGridLayout()
        gLayout.setSpacing(0)
        for col, label in enumerate([ASC2UNI.get(x, None) for x in
                                     "A# _ C# D# _ F# G#".split()]):
            if label is None:
                continue
            but = QPushButton(label)
            gLayout.addWidget(but, 0, col)
        for col, label in enumerate('A B C D E F G'.split()):
            but = QPushButton(label)
            gLayout.addWidget(but, 1, col)
        for col, label in enumerate([ASC2UNI.get(x, None) for x in
                                     "Ab Bb _ Db Eb _ Gb".split()]):
            if label is None:
                continue
            but = QPushButton(label)
            gLayout.addWidget(but, 2, col)
        vLayout.addLayout(gLayout)
        but = QPushButton("Next Note")
        vLayout.addWidget(but, 0, qt.AlignHCenter)
        vLayout.addStretch(2)
        self.setLayout(vLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = DummyWidget()
    w = NoteGuessWidget(d)
    d.show()
    app.exec_()
        

