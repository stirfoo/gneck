#!/usr/bin/python -t
# -*- coding: utf-8 -*-

"""util.py

Monday, August 26 2013
"""

def listRot(l, n):
    """Return a copy of l rotated n places.

    l -- list
    n -- integer, if positive rotate right

    Return a new list"""
    return l[-n:] + l[:-n]

# all note names, only flats are used internally
NOTES = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
# sharp to flat look-up
SHARP2FLAT = {'A#': 'Bb', 'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab'}
# ASCII to Unicode for notes -> GUI labels.
# This simply keeps all the Unicode characters in one place.
ASC2UNI = {'A#': u'A♯', 'A': 'A', 'Ab': u'A♭',
                        'B': 'B', 'Bb': u'B♭',
           'C#': u'C♯', 'C': 'C',
           'D#': u'D♯', 'D': 'D', 'Db': u'D♭',
                        'E': 'E', 'Eb': u'E♭',
           'F#': u'F♯', 'F': 'F',
           'G#': u'G♯', 'G': 'G', 'Gb': u'G♭'}

# Unicode to ASCII for GUI lables -> notes.
UNI2ASC = dict([[v,k] for k,v in ASC2UNI.items()])
# All available tunings. The first value is displayed in the tuning list
# view. The second value is the tool tip text.
TUNINGS = [('EADG',      'Std 4 string'),
           ('DADG',      'Drop D 4 string'),
           ('BEADG',     'Std 5 string'),
           ('EADGC',     'Std 5 string, high C'),
           ('AC#EAE',    'Open A 5 string'),
           ('FCFAF',     'Open F 5 string'),
           ('GDGBD',     'Open G 5 string'),
           ('EADGBE',    'Std 6 string'),
           ('DADGBE',    'Drop D 6 string'),
           ('DADGAD',    '6 string'),
           ('EAC#EAE',   'Open A 6 string'),
           ('BF#BF#BD#', 'Open B 6 string'),
           ('CGCGCE',    'Open C 6 string'),
           ('DADF#AD',   'Open D 6 string'),
           ('EBEG#BE',   'Open E 6 string'),
           ('CFCFAF',    'Open F 6 string'),
           ('DGDGBD',    'Open G 6 string'),
           ('BEADGBE',   'Std 7 string'),
           ]
# Major scale intervals
MAJ_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
# Major Pentatonic intevals
MAJ_PENT_INTERVALS = [2, 2, 3, 2, 3]
# Major blues intervals
MAJ_BLUES_INTERVALS = [2, 1, 1, 3, 2, 3]
# All available intervals. The keys will be displayed in the scale list view.
INTERVALS = {'Major': listRot(MAJ_INTERVALS, 0),
             'Ionian': listRot(MAJ_INTERVALS, 0),
             'Dorian': listRot(MAJ_INTERVALS, -1),
             'Phrygian': listRot(MAJ_INTERVALS, -2),
             'Lydian': listRot(MAJ_INTERVALS, -3),
             'Mixolydian': listRot(MAJ_INTERVALS, -4),
             'Aeolian': listRot(MAJ_INTERVALS, -5),
             'Locrian': listRot(MAJ_INTERVALS, -6),
             'Major Pentatonic': listRot(MAJ_PENT_INTERVALS, 0),
             'Minor Pentatonic': listRot(MAJ_PENT_INTERVALS, 1),
             'Harmonic Minor': [2, 1, 2, 2, 1, 3, 1],
             'Major Blues': listRot(MAJ_BLUES_INTERVALS, 0),
             'Minor Blues': listRot(MAJ_BLUES_INTERVALS, 1),
             }
