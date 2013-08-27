#!/usr/bin/python -t
#-*- coding: utf-8 -*-

"""necknote.py

Drill the user (me!) on note names at a given neck position or display
selected scales.

Saturday, August 24 2013
"""

import re
import sys
from random import choice

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt as qt

from util import UNI2ASC, INTERVALS, NOTES, SHARP2FLAT
from neck import Neck
from noteguess import NoteGuessWidget
from neckcfg import NeckConfigWidget
from scales import ScaleWidget

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
    def fitNeck(self):
        self.fitInView(self.neck, qt.KeepAspectRatio)
    def sizeHint(self):
        return QSize(1600, 200)
    def resizeEvent(self, e):
        """Fit the neck into the view.
        """
        super(View, self).resizeEvent(e)
        self.fitNeck()
        

class AppWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setWindowTitle("GNeck")
        self.widget = QWidget(self)
        self.scene = Scene(self)
        self.view = View(self.scene)
        self.gLayout = QGridLayout(self.widget)
        self.gLayout.addWidget(self.view, 0, 0, 1, 3)
        self.gLayout.setRowStretch(0, 1)
        self.gLayout.addWidget(self._createNeckCfgWidget(), 1, 0)
        self.gLayout.addWidget(self._createScaleWidget(), 1, 1)
        self.gLayout.addWidget(self._createNoteGuessWidget(), 1, 2)
        self.setCentralWidget(self.widget)
    def _createNeckCfgWidget(self):
        w = NeckConfigWidget()
        self.connect(w.tuningCombo, SIGNAL('activated(const QString&)'),
                     self.onTuningChanged)
        self.connect(w.fretsSpinBox, SIGNAL("valueChanged(int)"),
                     self.onFretCountChanged)
        self.connect(w.leftyCheckBox, SIGNAL("toggled(bool)"),
                     self.onLeftyChanged)
        return w
    def _createScaleWidget(self):
        w = ScaleWidget()
        self.scaleWidget = w    # for Scale/Key change
        self.connect(w.keyComboBox, SIGNAL('activated(const QString&)'),
                     lambda keyName
                     : self.onScaleKeyChanged(UNI2ASC[unicode(keyName)]))
        self.connect(w.scaleListView,
                     SIGNAL('currentTextChanged(const QString&)'),
                     self.onScaleChanged)
        return w
    def _createNoteGuessWidget(self):
        w = NoteGuessWidget()
        for button in [x for x in w.children() if isinstance(x, QPushButton)]:
            txt = button.text()
            if txt == 'Next Note':
                self.connect(button, SIGNAL('pressed()'), self.onNextNote)
            else:
                self.connect(button, SIGNAL('pressed()'),
                             lambda noteName=UNI2ASC[unicode(txt)]
                             : self.onNoteGuessPress(noteName))
        return w
    def onTuningChanged(self, tuning):
        t = [SHARP2FLAT.get(x, x)
             for x in re.findall(r'[A-G][#b]?', str(tuning))]
        self.view.neck.setTuning(t)
        self.view.neck.updateAll()
        self.view.fitNeck()
    def onLeftyChanged(self, bValue):
        """Change the orientation of the neck.

        value -- True to show a left-handed neck, False otherwise

        Called when Lefty check box is clicked.
        """
        self.view.neck.setLeftHanded(bValue)
        self.view.fitNeck()
    def onScaleKeyChanged(self, keyName):
        self.view.neck.markScale(self.scaleWidget.curScale(), str(keyName))
        self.scene.update()
    def onScaleChanged(self, scaleName):
        self.view.neck.markScale(str(scaleName), self.scaleWidget.curKey())
        self.scene.update()
    def onNextNote(self):
        """Display the next random note on the fretboard
        """
        self.curNote = choice(NOTES)
        self.view.neck.markRandomNote(self.curNote)
        self.scene.update()
    def onNoteGuessPress(self, noteName):
        """Check if the user guessed the right note.

        note -- string label of the button pressed (Unicode)

        If note matches the current note displayed on the neck, call
        nextNote(), else show all the positions of the current note on the
        neck.

        Called when a Note button is pressed.
        """
        if SHARP2FLAT.get(noteName, noteName) == self.curNote:
            self.onNextNote()
        else:
            self.view.neck.markAll(self.curNote)
            self.scene.update()
    def onFretCountChanged(self, frets):
        """Update the number of frets on the neck.

        value -- integer

        Called when the Fret spin box is changed.
        """
        self.view.neck.setFretCount(frets)
        self.view.neck.updateAll()
        self.view.fitNeck()
        
            
class App(QApplication):
    def __init__(self, argv):
        super(App, self).__init__(argv)
        self.appWindow = AppWindow()
        self.appWindow.show()
        

if __name__ == '__main__':
    app = App(sys.argv)
    app.exec_()
