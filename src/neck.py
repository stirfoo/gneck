#!/usr/bin/python -t
# -*- coding: utf-8 -*-

"""neck.py

Sunday, August 25 2013
"""

from math import sin, asin, degrees
from random import randrange
from itertools import cycle

from PyQt4.QtCore import QPointF, QRectF
from PyQt4.QtGui import (QGraphicsPathItem, QBrush, QPen, QTransform, QColor,
                         QPainterPath)
from PyQt4.QtCore import Qt as qt

from util import NOTES, SHARP2FLAT, INTERVALS, listRot


class Neck(QGraphicsPathItem):
    """A graphical representation of a six string guitar neck.

    The neck may have 2 to 24 frets, be left or right-handed, and the tuning
    may be configured. The number of strings will be derived from the tuning.
    """
    # NOTE: all these are fudged for aesthetics
    markerDia = 0.25
    nutThickness = 0.1875
    stringSpacing = .375
    stringEdgeOffset = .06      # y distance from edge of neck to string
    def __init__(self, tuning="E A D G B E".split(), nFrets=22, parent=None):
        """Initialize a neck.

        tuning -- A list of open string notes. Index 0 is the heaviest
                  string. The default is: ['E', 'A', 'D', 'G', 'B', 'E']
                  Use b for flat and # for sharp, e.g. A#, Bb.
                  B#, Cb, E#, and Fb are illegal.
        nFrets -- integer, number of frets between 2 and 24, default is 22
        parent -- QGraphicsItem or None, default is None
        """
        super(Neck, self).__init__(parent)
        # a little thicker lines
        self.setPen(QPen(QColor(0, 0, 0), .025))
        self.markedNotes = []
        self.setTuning(tuning)
        self.setFretCount(nFrets)
        self.updateAll()
    def setTuning(self, tuning):
        """Configure the string tuning.

        tuning -- list of notes names as strings, from heaviest to lightest
                  string. 

        Does not call update(). Return None.
        """
        result = []
        self.nStrings = len(tuning)
        if self.nStrings < 2 or self.nStrings > 7:
            raise Exception("tuning must have 4 to 7 notes")
        for noteName in tuning:
            try:
                result.append(self.checkNoteName(noteName))
            except:
                raise Exception("Illegal note name"
                                " in tuning: {}".format(repr(noteName)))
        self.tuning = result
    def setFretCount(self, n):
        """Set the number of frets on the neck

        n -- integer between 2 and 24

        Raise Exception if n not 2 to 24. Return None.
        """
        if n < 2 or n > 24:
            raise Exception("number of frets must be an integer from"
                            " 2 to 24, not {}".format(repr(n)))
        self.nFrets = n
    def updateAll(self):
        self.markedNotes = []
        self._createNotes()
        self._updatePP()
        self.update()
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
        stringSpan = (self.nStrings - 1) * self.stringSpacing
        nutWidth = stringSpan + self.stringEdgeOffset * 2
        # frets
        scaleLen = 25.5
        offset = 0.0            # previous fret x coordinate
        self.fretXs = [0.0]
        for n in range(self.nFrets):
            pos = offset + (scaleLen - offset) / 17.817
            self.fretXs.append(pos)
            pp.moveTo(pos, nutWidth)
            pp.lineTo(pos, 0.0)
            offset = pos
        # marker dots
        y = nutWidth / 2.0
        for n in [3, 5, 7, 9, 12, 15, 17, 19, 21, 24]:
            if n > self.nFrets:
                break
            fretX1 = self.fretXs[n-1]
            fretX2 = self.fretXs[n]
            x = fretX1 + (fretX2 - fretX1) / 2.0
            d = self.markerDia
            r = d / 2.0
            dy = nutWidth / 4.0
            if n % 12 == 0:
                pp.addEllipse(x-r, y-r-dy, d, d)
                pp.addEllipse(x-r, y-r+dy, d, d)
            else:
                pp.addEllipse(x-r, y-r, d, d)
        # strings
        self.stringYs = []
        endX = self.fretXs[-1]
        for n in range(self.nStrings):
            y = self.stringEdgeOffset + self.stringSpacing * n
            self.stringYs.append(y)
            pp.moveTo(-self.nutThickness - self.fretXs[1] / 2.0, y)
            pp.lineTo(endX, y)
        # outline
        pp.addRect(0, 0, self.fretXs[-1], nutWidth)
        # nut
        pp.addRect(-self.nutThickness, 0, self.nutThickness, nutWidth)
        # partial headstock, to allow room for open note display
        # upper curve
        r = 2.0
        d = self.fretXs[1] / 2.0
        rectL = -self.nutThickness - r
        rect = QRectF(rectL, -r*2.0, r*2.0, r*2.0)
        ra = asin(d / r)
        da = degrees(ra)
        pp.arcMoveTo(rect, 270.0)
        pp.arcTo(rect, 270.0, -da)
        # lower curve
        rect = QRectF(rectL, nutWidth, r*2.0, r*2.0)
        pp.arcMoveTo(rect, 90.0)
        pp.arcTo(rect, 90.0, da)
        # x coordinate of open string note markers
        self.openX = (-self.nutThickness - sin(ra) * r) / 2.0
        self.setPath(pp)
    def _createNotes(self):
        """Create a MxN array of all note names on the neck.

        M is self.nStrings
        N is self.nFrets (+1 for the open string).

        Return None.
        """
        # index 0 is the bottom (lightest) string
        self.allNotes = [[] for n in range(self.nStrings)]
        t = self.tuning[-1::-1]
        for string in range(self.nStrings):
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
        for string, fret, root in self.markedNotes:
            if root:
                # mark root notes different color
                painter.setBrush(QBrush(QColor(255, 0, 0)))
                painter.setPen(QColor(255, 0, 0))
            else:
                painter.setBrush(QBrush(QColor(0, 0, 0)))
                painter.setPen(QColor(0, 0, 0))
            if fret == 0:
                # special case for open notes
                x = self.openX
            else:
                x = (self.fretXs[fret-1] + self.fretXs[fret]) / 2.0
            r = self.markerDia / 2.0
            painter.drawEllipse(QPointF(x, self.stringYs[string]), r, r)
    def markRandomNote(self, noteName):
        """Mark the note for display on the neck.

        noteName -- see: checkNoteName()

        Does not call update. Return None.
        """
        noteName = self.checkNoteName(noteName)
        while True:
            string = randrange(self.nStrings)
            # try to get a little more even distibution of the note palcement
            if randrange(10) % 2 == 0:
                startFret = 0
            else:
                startFret = randrange(self.nFrets)
            try:
                # find the first noteName on string, starting at startFret
                idx = self.allNotes[string][startFret:].index(noteName)
            except ValueError:
                continue
            self.markedNotes = [(string, idx + startFret, False)]
            break
    def markAll(self, noteName):
        """Mark every position of noteName for display.

        noteName -- see: checkNoteName()
        
        Does not call update. Return None.
        """
        noteName = self.checkNoteName(noteName)
        self.markedNotes = []
        for string, stringNotes in enumerate(self.allNotes):
            for fret, note in enumerate(stringNotes):
                if note == noteName:
                    self.markedNotes.append((string, fret, False))
    def markScale(self, scaleName, keyName):
        """Mark the scale in the given key.

        scaleName -- a key found in ScaleNeck.intervals
        keyName -- see: checkNoteName()

        Does not call update(). Raise Exception if either scaleName or keyName
        is unknown. Return None.
        """
        try:
            keyName = self.checkNoteName(keyName)
        except:
            raise Exception('Unknown key name: {}'.format(repr(keyName)))
        intervals = INTERVALS.get(scaleName, None)
        if intervals is None:
            raise Exception('Unknown scale name: {}'.format(repr(scaleName)))
        self.markedNotes = []
        idx = NOTES.index(keyName)
        shiftedNotes = listRot(NOTES, -idx)
        notes = [shiftedNotes[0]]
        i = 0
        for ii in intervals[:-1]:
            i = i + ii
            notes.append(shiftedNotes[i])
        self.markedNotes = []
        for name in notes:
            noteName = self.checkNoteName(name)
            for string, stringNotes in enumerate(self.allNotes):
                for fret, note in enumerate(stringNotes):
                    if note == noteName:
                        self.markedNotes.append((string, fret,
                                                 note == keyName))
    def checkNoteName(self, noteName):
        """Ensure noteName is valid.

        A valid note is one found in the global NOTES or in the keys of the
        global dict SHARP2FLAT.

        Return a valid note name or raise Exception if invalid.
        """
        if noteName not in NOTES:
            noteName = SHARP2FLAT.get(noteName)
            if noteName is None:
                raise Exception("Illegal note {}".format(repr(noteName)))
        return noteName
    
# class ScaleNeck(Neck):
#     # 1 is 1 fret, 2 is 2, etc.
#     majIntervals = [2, 2, 1, 2, 2, 2, 1]
#     majPentIntervals = [2, 2, 3, 2, 3]
#     majBluesIntervals = [2, 1, 1, 3, 2, 3]
#     intervals = {'Major': listRot(majIntervals, 0),
#                  'Ionian': listRot(majIntervals, 0),
#                  'Dorian': listRot(majIntervals, -1),
#                  'Phrygian': listRot(majIntervals, -2),
#                  'Lydian': listRot(majIntervals, -3),
#                  'Mixolydian': listRot(majIntervals, -4),
#                  'Aeolian': listRot(majIntervals, -5),
#                  'Locrian': listRot(majIntervals, -6),
#                  'Major Pentatonic': listRot(majPentIntervals, 0),
#                  'Minor Pentatonic': listRot(majPentIntervals, 1),
#                  'Harmonic Minor': [2, 1, 2, 2, 1, 3, 1],
#                  'Major Blues': listRot(majBluesIntervals, 0),
#                  'Minor Blues': listRot(majBluesIntervals, 1),
#                  }
#     def markScale(self, scaleName, keyName):
#         """Mark the scale in the given key.

#         scaleName -- a key found in ScaleNeck.intervals
#         keyName -- see: checkNoteName()

#         Does not call update(). Raise Exception if either scaleName or keyName
#         is unknown. Return None.
#         """
#         try:
#             keyName = self.checkNoteName(keyName)
#         except:
#             raise Exception('Unknown key name: {}'.format(repr(keyName)))
#         intervals = self.intervals.get(scaleName, None)
#         if intervals is None:
#             raise Exception('Unknown scale name: {}'.format(repr(scaleName)))
#         self.markedNotes = []
#         idx = NOTES.index(keyName)
#         shiftedNotes = listRot(NOTES, -idx)
#         notes = [shiftedNotes[0]]
#         i = 0
#         for ii in intervals[:-1]:
#             i = i + ii
#             notes.append(shiftedNotes[i])
#         self.markedNotes = []
#         for name in notes:
#             noteName = self.checkNoteName(name)
#             for string, stringNotes in enumerate(self.allNotes):
#                 for fret, note in enumerate(stringNotes[1:]):
#                     if note == noteName:
#                         self.markedNotes.append((string, fret + 1,
#                                                  note == keyName))
#     def paint(self, painter, option, widget):
#         """Draw the neck.

#         This method differs from Neck.paint() in that self.markedNotes has an
#         extra root note value in each tuple. They are drawn a different color.

#         Return None.
#         """
#         super(Neck, self).paint(painter, option, widget)
#         for string, fret, root in self.markedNotes:
#             if root:
#                 # mark root notes different color
#                 painter.setBrush(QBrush(QColor(255, 0, 0)))
#                 painter.setPen(QColor(255, 0, 0))
#             else:
#                 painter.setBrush(QBrush(QColor(0, 0, 0)))
#                 painter.setPen(QColor(0, 0, 0))
#             fretX1 = self.fretXs[fret-1]
#             fretX2 = self.fretXs[fret]
#             r = self.markerDia / 2.0
#             painter.drawEllipse(QPointF((fretX1 + fretX2) / 2.0,
#                                         self.stringYs[string]),
#                                 r, r)
