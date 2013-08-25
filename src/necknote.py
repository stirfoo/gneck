#!/usr/bin/python -t
#-*- coding: utf-8 -*-

"""necknote.py

Drill the user (me!) on note names at a given neck position.

Saturday, August 24 2013
"""

import sys
from copy import copy
from random import randrange, choice
from itertools import cycle

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt as qt


# all note names
NOTES = ['A', u'B♭', 'B', 'C', u'D♭', 'D', u'E♭', 'E', 'F', u'G♭', 'G', u'A♭']
# sharp to flat lookup
LOOKUP = {u'A♯': u'B♭', u'C♯': u'D♭', u'D♯': u'E♭', u'F♯': u'G♭', u'G♯':
              u'A♭'}


class Neck(QGraphicsPathItem):
    """A graphical representation of a six string guitar neck.

    The neck may have 2 to 24 frets, be left or right-handed, and the tuning
    may be configured.
    """
    # approximate
    markerDia = 0.25
    # The nut width is not drawn to scale because the neck is drawn as a
    # rectangle. It just looks a little better @ 2.0.
    nutWidth = 2.0
    # approximate    
    nutThickness = 0.125
    def __init__(self, tuning=['E', 
                               'A',
                               'D',
                               'G',
                               'B',
                               'E'],
                 nFrets=22, parent=None):
        """Initialize a neck with 22 frets in standard tuning.

        tuning -- A list of open string notes. The default is:
                  ['E', 'A', 'D', 'G', 'B', 'E']
        nFrets -- integer, number of frets, default is 22
        parent -- QGraphicsItem or None, default is None
        """
        super(Neck, self).__init__(parent)
        # a little thicker lines
        self.setPen(QPen(QColor(0, 0, 0), .025))
        if nFrets < 1 or nFrets > 24:
            raise Exception("number of frets must be an integer from"
                            " 2 to 24, not {}".format(repr(nFrets)))
        self.nFrets = nFrets
        self.tuning = tuning
        self._updatePP()
        self.markedNotes = []
        self._createNotes()
    def setFretCount(self, n):
        """Set the number of frets on the neck

        n -- integer between 2 and 24

        Return None.
        """
        self.nFrets = n
        self._updatePP()
        self.markedNotes = []
        self._createNotes()
    def setOrientation(self, bValue):
        """Configure the neck as left or right-handed.

        bValue -- bool, if True, mirror the neck

        Return None.
        """
        if bValue:
            self.setTransform(QTransform().scale(-1, 1))
        else:
            self.setTransform(QTransform().scale(1, 1))
    def _updatePP(self):
        """Create the neck geometry updating this item's QPainterPath.

        Return None.
        """
        self.prepareGeometryChange()
        pp = QPainterPath()
        # frets
        scaleLen = 25.5
        offset = 0.0            # from the previous fret
        self.fretXs = [0.0]
        for n in range(self.nFrets):
            pos = offset + (scaleLen - offset) / 17.817
            self.fretXs.append(pos)
            pp.moveTo(pos, self.nutWidth)
            pp.lineTo(pos, 0.0)
            offset = pos
        # marker dots
        y = self.nutWidth / 2.0
        for n in [3, 5, 7, 9, 12, 15, 17, 19, 21, 24]:
            if n > self.nFrets:
                break
            fretX1 = self.fretXs[n-1]
            fretX2 = self.fretXs[n]
            x = fretX1 + (fretX2 - fretX1) / 2.0
            if n % 12 == 0:
                pp.addEllipse(x-.125, y-.125-.4375, .25, .25)
                pp.addEllipse(x-.125, y-.125+.4375, .25, .25)
            else:
                pp.addEllipse(x-.125, y-.125, .25, .25)
        # strings
        self.stringYs = []
        offset = self.nutWidth * .03
        spacing = (self.nutWidth - (offset * 2)) / 5.0
        x = self.fretXs[-1]
        for n in range(6):
            y = offset + spacing * n
            self.stringYs.append(y)
            pp.moveTo(-self.nutThickness, y)
            pp.lineTo(x, y)
        # outline
        pp.addRect(0, 0, self.fretXs[-1], self.nutWidth)
        # nut
        pp.addRect(-self.nutThickness, 0, self.nutThickness, self.nutWidth)
        self.setPath(pp)
    def _createNotes(self):
        """Create a 6xN array of note names.

        N is self.nFrets (+1 for the open string).

        Return None.
        """
        self.allNotes = [[],    # high E
                         [],
                         [],
                         [],
                         [],
                         []]    # low E
        t = self.tuning[-1::-1]
        for string in range(6):
            i = NOTES.index(t[string])
            notes = NOTES[i:] + NOTES[:i]
            for f, note in enumerate(cycle(notes)):
                if f > self.nFrets:
                    break
                self.allNotes[string].append(note)
    # XXX: wont work, dont know if it's using shape() instead
    def boundingRect(self):
        r = super(Neck, self).boundingRect()
        return r.adjusted(-.125, -.125, .25, .25)
    def paint(self, painter, option, widget):
        """Draw the neck.

        The base class draws the neck geometry. This function draws any marked
        notes.

        Return None.
        """
        super(Neck, self).paint(painter, option, widget)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QColor(0, 0, 0))
        for string, fret in self.markedNotes:
            yc = self.stringYs[string]
            fretX1 = self.fretXs[fret-1]
            fretX2 = self.fretXs[fret]
            xc = fretX1 + (fretX2 - fretX1) / 2.0
            r = self.markerDia / 2.0
            painter.drawEllipse(QPointF(xc, yc), r, r)
    def markRandomNote(self, noteName):
        """Display the given note at a random position on the neck.

        noteName -- string, see: checkNoteName()

        Return None
        """
        while True:
            string = randrange(6)
            startFret = randrange(22) + 1 # +1 don't mark open string notes
            try:
                idx = self.allNotes[string][startFret:].index(noteName)
            except ValueError:
                continue
            self.markedNotes = [(string, idx + startFret)]
            break
    def markAll(self, noteName):
        """Show every position (except open strings) of the given note.

        noteName -- string, see: checkNoteName()
        
        Return None
        """
        noteName = self.checkNoteName(noteName)
        self.markedNotes = []
        for string, stringNotes in enumerate(self.allNotes):
            for fret, note in enumerate(stringNotes[1:]):
                if note == noteName:
                    self.markedNotes.append((string, fret + 1))
    def checkNoteName(self, noteName):
        """Ensure noteName is valid.

        A valid note is one found in the global NOTES or in the keys of the
        global dict LOOKUP.

        Return a valid note name or raise Exception if invalid.
        """
        if noteName not in NOTES:
            name = LOOKUP.get(noteName)
            if name:
                noteName = name
            else:
                raise Exception("Illegal note {}".format(repr(noteName)))
        return noteName
        
        
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
        self.view.neck.setOrientation(value)
        self.view.fitInView(self.view.neck, qt.KeepAspectRatio)
        
            
class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.appWindow = AppWindow()
        self.appWindow.show()
        

if __name__ == '__main__':
    app = App(sys.argv)
    app.exec_()
