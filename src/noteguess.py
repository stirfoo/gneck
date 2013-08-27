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
    """Note-labeled button array. Next Note button. Note filters.
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
        hLayout = QHBoxLayout()
        for label, tip, default in [('All', 'Drill all notes', True),
                                    ('Natural', "Don't drill sharps or flats",
                                     False),
                                    ('Markers',
                                     'Drill only open or neck marker notes',
                                     False)]:
            rbut = QRadioButton(label)
            rbut.setToolTip(tip)
            rbut.setChecked(default)
            hLayout.addWidget(rbut)
        hLayout.addStretch(2)
        but = QPushButton("Next Note")
        hLayout.addWidget(but)
        vLayout.addLayout(hLayout)
        vLayout.addStretch(2)
        self.setLayout(vLayout)
    def noteFilter(self):
        for widget in self.children():
            if isinstance(widget, QRadioButton) and widget.isChecked():
                return widget.text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = DummyWidget()
    w = NoteGuessWidget(d)
    d.show()
    app.exec_()
        

