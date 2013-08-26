#!/usr/bin/python -t
# -*- coding: utf-8 -*-

"""neck.py

Sunday, August 25 2013
"""

from random import randrange
from itertools import cycle

from PyQt4.QtCore import QPointF
from PyQt4.QtGui import (QGraphicsPathItem, QBrush, QPen, QTransform, QColor,
                         QPainterPath)
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
    def __init__(self, tuning=['E', 'A', 'D', 'G', 'B', 'E'], nFrets=22,
                 parent=None):
        """Initialize a neck with 22 frets in standard tuning.

        tuning -- A list of open string notes. Index 0 is the heaviest
                  string. The default is: ['E', 'A', 'D', 'G', 'B', 'E']
        nFrets -- integer, number of frets between 2 and 24, default is 22
        parent -- QGraphicsItem or None, default is None
        """
        super(Neck, self).__init__(parent)
        # a little thicker lines
        self.setPen(QPen(QColor(0, 0, 0), .025))
        if nFrets < 2 or nFrets > 24:
            raise Exception("number of frets must be an integer from"
                            " 2 to 24, not {}".format(repr(nFrets)))
        self.tuning = tuning
        self.setFretCount(nFrets)
    def setFretCount(self, n):
        """Set the number of frets on the neck

        n -- integer between 2 and 24

        Raise Exception if n not 2 to 24. Return None.
        """
        if n < 2 or n > 24:
            raise Exception("number of frets must be an integer from"
                            " 2 to 24, not {}".format(repr(n)))
        self.nFrets = n
        self.markedNotes = []
        self._createNotes()
        self._updatePP()
    def setLeftHanded(self, bValue):
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
            d = self.markerDia
            r = d / 2.0
            dy = self.nutWidth / 4.0
            if n % 12 == 0:
                pp.addEllipse(x-r, y-r-dy, d, d)
                pp.addEllipse(x-r, y-r+dy, d, d)
            else:
                pp.addEllipse(x-r, y-r, d, d)
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
        """Create a 6xN array of all note names on the neck.

        N is self.nFrets (+1 for the open string).

        Return None.
        """
        # index 0 is the bottom (lightest) string
        self.allNotes = [[], [], [], [], [], []]
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
        # round, solid black note markers
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setPen(QColor(0, 0, 0))
        for string, fret in self.markedNotes:
            yc = self.stringYs[string]
            fretX1 = self.fretXs[fret-1]
            fretX2 = self.fretXs[fret]
            xc = (fretX1 + fretX2) / 2.0
            r = self.markerDia / 2.0
            painter.drawEllipse(QPointF(xc, yc), r, r)
    def markRandomNote(self, noteName):
        """Display the given note at a random position on the neck.

        noteName -- string, see: checkNoteName()

        Does not call update. Return None.
        """
        while True:
            string = randrange(6)
            startFret = randrange(1, self.nFrets)
            try:
                idx = self.allNotes[string][startFret:].index(noteName)
            except ValueError:
                continue
            self.markedNotes = [(string, idx + startFret)]
            break
    def markAll(self, noteName):
        """Show every position (except open strings) of the given note.

        noteName -- string, see: checkNoteName()
        
        Does not call update. Return None.
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
        
