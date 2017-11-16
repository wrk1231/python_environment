# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class side_by_side():
    def __init__(self, *frames):
        self.frames = frames

    def _repr_html_(self):
        width = 100. / len(self.frames)

        s = ""
        for f in self.frames:
            s += "<div style='float: left; border-left : 5px solid #6699cc;'>%s</div>" % f._repr_html_()

        return s

 