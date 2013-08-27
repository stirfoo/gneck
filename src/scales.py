#!/usr/bin/python -t
# -*- coding: utf-8 -*-

"""scales.py

Monday, August 26 2013
"""

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt as qt

from util import INTERVALS, ASC2UNI, UNI2ASC


class ScaleWidget(QGroupBox):
    """Select key and scale widget
    """
    def __init__(self, parent=None):
        super(ScaleWidget, self).__init__('Scales', parent)
        keyLabel = QLabel('Key')
        self.keyComboBox = QComboBox()
        for noteName in [ASC2UNI[x] for x in
                         "Ab A A# Bb B C C# Db D D#"
                         " Eb E F F# Gb G G#".split()]:
            self.keyComboBox.addItem(noteName)
        self.scaleListView = QListWidget()
        for scale in sorted(INTERVALS.keys()):
            self.scaleListView.addItem(scale)
        self.scaleListView.setCurrentRow(0)
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()
        hLayout.addWidget(keyLabel)
        hLayout.addWidget(self.keyComboBox)
        hLayout.addStretch(1)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.scaleListView)
        self.setLayout(vLayout)
    def curScale(self):
        return str(self.scaleListView.currentItem().text())
    def curKey(self):
        return str(UNI2ASC[unicode(self.keyComboBox.currentText())])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ScaleWidget()
    w.show()
    app.exec_()
    
