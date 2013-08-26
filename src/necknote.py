#!/usr/bin/python -t
#-*- coding: utf-8 -*-

"""necknote.py

Drill the user (me!) on note names at a given neck position.

Saturday, August 24 2013
"""

import sys
from random import choice

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt as qt

from neck import NOTES, LOOKUP, Neck


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)
        
        
class View(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(View, self).__init__(parent)
        self.setRenderHints(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setScene(scene)
        self.neck = Neck()
        self.scene().addItem(self.neck)
    def sizeHint(self):
        return QSize(1600, 200)
    def resizeEvent(self, e):
        """Fit the neck into the view.
        """
        super(View, self).resizeEvent(e)
        self.fitInView(self.neck, qt.KeepAspectRatio)
        

class AppWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setWindowTitle("GNeck")
        self.widget = QWidget(self)
        self.scene = Scene(self)
        self.view = View(self.scene, self.widget)
        self.vLayout = QVBoxLayout(self.widget)
        self.gLayout = QGridLayout()
        self.vLayout.addWidget(self.view)
        self.vLayout.addLayout(self.gLayout)
        self.makeButtons()
        self.setCentralWidget(self.widget)
        self.nextNote()
    def makeButtons(self):
        """Create and connect all the buttons.
        
        A#      C#  D#      F#  G#
        A   B   C   D   E   F   G
        Ab  Bb      Db  Eb      Gb
        Next Note Frets 22 Lefty x
        """
        self.gLayout.setSpacing(0)
        for col, label in enumerate([u'A♯', '', u'C♯', u'D♯', '', u'F♯',
                                     u'G♯']):
            but = QPushButton(label)
            if label == '':
                continue
            self.gLayout.addWidget(but, 0, col)
            # self.gLayout.setColumnStretch(col, 1)
            self.connect(but, SIGNAL('pressed()'),
                         lambda note=label : self.onPress(note))
        for col, label in enumerate('A B C D E F G'.split()):
            but = QPushButton(label)
            self.gLayout.addWidget(but, 1, col)
            self.connect(but, SIGNAL('pressed()'),
                         lambda note=label : self.onPress(note))
        for col, label in enumerate([u'A♭', u'B♭', '', u'D♭', u'E♭', '',
                                     u'G♭']):
            but = QPushButton(label)
            if label == '':
                continue
            self.gLayout.addWidget(but, 2, col)
            self.connect(but, SIGNAL('pressed()'),
                         lambda note=label : self.onPress(note))
        hLayout = QHBoxLayout()
        self.vLayout.addLayout(hLayout)
        but = QPushButton("Next Note")
        spinBox = QSpinBox()
        spinBox.setValue(self.view.neck.nFrets)
        spinBox.setMinimum(2)
        spinBox.setMaximum(24)
        self.connect(spinBox, SIGNAL("valueChanged(int)"), self.onSpin)
        leftyCheckBox = QCheckBox()
        self.connect(leftyCheckBox, SIGNAL("toggled(bool)"), self.onLefty)
        hLayout.addStretch(1)
        hLayout.addWidget(but)
        hLayout.addWidget(QLabel("Frets"))
        hLayout.addWidget(spinBox)
        hLayout.addWidget(QLabel("Lefty"))
        hLayout.addWidget(leftyCheckBox)
        self.connect(but, SIGNAL('pressed()'), self.nextNote)
    def nextNote(self):
        """Display the next random note on the fretboard
        """
        self.curNote = choice(NOTES)
        self.view.neck.markRandomNote(self.curNote)
        self.scene.update()
    def onPress(self, note):
        """Check if the user guessed the right note.

        note -- string lable of the button pressed

        If note matches the current note displayed on the neck, call
        nextNote(), else show all the positions of the current note on the
        neck.

        Called when a Note button is pressed.
        """
        if LOOKUP.get(note, note) == self.curNote:
            self.nextNote()
        else:
            self.view.neck.markAll(self.curNote)
            self.scene.update()
    def onSpin(self, value):
        """Update the number of frets on the neck.

        value -- integer

        Called when the Fret spin box is changed.
        """
        self.view.neck.setFretCount(value)
        self.view.fitInView(self.view.neck, qt.KeepAspectRatio)
    def onLefty(self, value):
        """Change the orientation of the neck.

        value -- True to show a left-handed neck, False otherwise

        Called when Lefty check box is clicked.
        """
        self.view.neck.setLeftHanded(value)
        self.view.fitInView(self.view.neck, qt.KeepAspectRatio)
        
            
class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.appWindow = AppWindow()
        self.appWindow.show()
        

if __name__ == '__main__':
    app = App(sys.argv)
    app.exec_()
