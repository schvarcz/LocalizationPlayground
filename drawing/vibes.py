from vibes import *

class DrawingVibes():
    """ A class to wrap the vibes calls (if I need to change to another GUI) """
    def __init__(self):
        vibes.beginDrawing()
        vibes.newFigure("Localization2")
        vibes.setFigureProperties({'x':100,'y':100,'width': 1000, 'height':600})

    def drawLandmarks(self,landmarks):
        for landmark in landmarks:
            vibes.drawCircle(landmark[0], landmark[1], .1,"red[red]")

    def drawPoses(self,poses):
        for pose in poses:
            vibes.drawBox(pose[0].lb(), pose[0].ub(), pose[1].lb(), pose[1].ub(),"black[cyan]")

    def drawTruePoses(self,poses):
        for pose in poses:
            vibes.drawCircle(pose[0], pose[1], 0.1,"black[black]")

    def clear(self):
        vibes.clearFigure()
