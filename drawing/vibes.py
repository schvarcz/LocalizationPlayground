from vibes import *
import logging

class DrawingVibes():
    """ A class to wrap the vibes calls (if I need to change to another GUI) """
    def __init__(self):
        vibes.beginDrawing()
        vibes.newFigure("Localization2")
        vibes.setFigureProperties({'x':100,'y':100,'width': 1000, 'height':600})

    def drawLandmarks(self,landmarks):
        for landmark in landmarks:
            vibes.drawCircle(landmark[0], landmark[1], .1,"red[red]")

    def drawPose(self, pose, colorIn="black[cyan]", colorMaybe="black[yellow]"):
        if type(pose) == list:
            logging.debug("Drawing box separator.")
            poses_in, poses_maybe = pose
            for pose_in in poses_in:
                vibes.drawBox(pose_in[0].lb(), pose_in[0].ub(), pose_in[1].lb(), pose_in[1].ub(),colorIn)
            for pose_maybe in poses_maybe:
                vibes.drawBox(pose_maybe[0].lb(), pose_maybe[0].ub(), pose_maybe[1].lb(), pose_maybe[1].ub(),colorMaybe)
        else:
            logging.debug("Drawing box contractor.")
            logging.debug(pose)
            vibes.drawBox(pose[0].lb(), pose[0].ub(), pose[1].lb(), pose[1].ub(),colorIn)

    def drawPoses(self, poses, colorIn="black[cyan]", colorMaybe="black[yellow]"):
        for pose in poses:
            self.drawPose(pose,colorIn,colorMaybe)

    def drawTruePoses(self,poses):
        for pose in poses:
            vibes.drawCircle(pose[0], pose[1], 0.1,"black[black]")

    def clear(self):
        vibes.clearFigure()
