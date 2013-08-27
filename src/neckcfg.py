#!/usr/bin/python -t
# -*- coding: utf-8 -*-

"""neckcfg.py

Monday, August 26 2013
"""

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt as qt

from util import TUNINGS


class NeckConfigWidget(QGroupBox):
    """GUI to set the neck tuning, number of frets and handedness.
    """
    def __init__(self, tuning='EADGBE', nFrets=22, lefty=False, parent=None):
        super(NeckConfigWidget, self).__init__('Neck Config', parent)
        tuningLabel = QLabel('Tuning')
        self.tuningCombo = QComboBox()
        activeIdx = 0
        for i, item_tip in enumerate(TUNINGS):
            item, tip = item_tip
            if item == tuning:
                activeIdx = i
            self.tuningCombo.addItem(item)
            self.tuningCombo.setItemData(i, tip, qt.ToolTipRole)
        self.tuningCombo.setCurrentIndex(activeIdx)
        fretsLabel = QLabel('Frets')
        self.fretsSpinBox = QSpinBox()
        self.fretsSpinBox.setValue(nFrets)
        self.fretsSpinBox.setMinimum(2)
        self.fretsSpinBox.setMaximum(24)
        self.leftyCheckBox = QCheckBox('Lefty?')
        self.leftyCheckBox.setChecked(lefty)
        gLayout = QGridLayout()
        gLayout.addWidget(tuningLabel, 1, 0, qt.AlignRight)
        gLayout.addWidget(self.tuningCombo, 1, 1)
        gLayout.addWidget(fretsLabel, 2, 0, qt.AlignRight)
        gLayout.addWidget(self.fretsSpinBox, 2, 1)
        gLayout.addWidget(self.leftyCheckBox, 3, 1)
        vLayout = QVBoxLayout()
        vLayout.addLayout(gLayout)
        vLayout.addStretch(2)
        self.setLayout(vLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = NeckConfigWidget()
    w.show()
    app.exec_()
        
