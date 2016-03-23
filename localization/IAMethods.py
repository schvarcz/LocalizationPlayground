from pyIbex import *
import logging

class IAContractorsLocalization():
    """ Perfoms the robot's localization using contractors over the tangent function """
    def __init__(self, landmarks, initialPose=IntervalVector([[0,0], [0,0]])):
        self.poses = [initialPose]
        self.landmarks = landmarks
        self.__lastData__ = None

    def localize(self,data):
        if self.__lastData__ == None:
            self.__lastData__ = data
        dt = data.time-self.__lastData__.time

        #Movement model
        self.__lastPose__ = self.poses[-1]
        actualPose = IntervalVector([[float("-inf"),float("inf")],[float("-inf"),float("inf")]])

        th = Interval(data.pose[2]-.02,data.pose[2]+.02)
        v = Interval(data.V-.3,data.V+.3)


        logging.debug("Contracting by movement.")
        actualPose, self.poses[-1] = self.__cstate__(self.__lastPose__, actualPose, th, v, dt)


        #Contracting by landmarks
        logging.debug("Contracting by landmarks.")
        for idx in range(self.numLandmarks()):
            gis = Interval(data.z_gis[idx]-0.02,data.z_gis[idx]+0.02)

            landmark = IntervalVector([
                [self.landmarks[idx][0],self.landmarks[idx][0]], 
                [self.landmarks[idx][1],self.landmarks[idx][1]]])

            d = Interval(0,float("inf"))
            actualPose, l = self.__cmarkss__(actualPose, landmark, d, gis, th)

            # actualPose, l = self.__cmarks__(actualPose, landmark, gis, th)

        logging.debug("Robot's pose"+str(actualPose))
        self.poses.append(actualPose)
        self.__lastData__ = data
        return actualPose

    def numLandmarks(self):
        return len(self.landmarks)

    def actualPose(self):
        return self.poses[-1]

    def __cstate__(self, lastPose, actualPose, th, v, dt):
        fx = Function("x1", "x", "v", "th", "x1 - x - %f*v*cos(th)" % dt)
        fy = Function("y1", "y", "v", "th", "y1 - y - %f*v*sin(th)" % dt)
        Cx = CtcFwdBwd(fx, Interval(0,0))
        Cy = CtcFwdBwd(fy, Interval(0,0))
        bx = IntervalVector(4)
        bx[0],bx[1],bx[2],bx[3] = actualPose[0], lastPose[0], v, th
        Cx.contract(bx)
        actualPose[0], lastPose[0] = bx[0],bx[1]

        by = IntervalVector(4)
        by[0],by[1],by[2],by[3] = actualPose[1], lastPose[1], v, th
        Cy.contract(by)
        actualPose[1], lastPose[1] = by[0],by[1]
        
        return actualPose, lastPose


    """ Not working for the unknow initialPose """
    def __cmarks__(self, pose, landmark, gis, th):
        f=Function("x", "mx", "y", "my", "gis", "th","(my - y)/(mx - x) - tan(gis+th)")
        C = CtcFwdBwd(f,Interval(0))
        b = IntervalVector(6)
        b[0], b[1], b[2], b[3], b[4], b[5] = pose[0], landmark[0], pose[1], landmark[1],  gis, th
        C.contract(b)
        pose[0], landmark[0], pose[1], landmark[1],  gis, th = b[0], b[1], b[2], b[3], b[4], b[5]

        return pose, landmark


    def __cmarkss__(self, pose, landmark, d, gis, th):
        fx=Function("x", "mx", "d", "gis", "th","mx - x - d*cos(gis+th)")
        fy=Function("y", "my", "d", "gis", "th","my - y - d*sin(gis+th)")

        Cx = CtcFwdBwd(fx,Interval(0))
        bx = IntervalVector(5)
        bx[0],bx[1],bx[2],bx[3], bx[4] = pose[0], landmark[0], d, gis, th
        Cx.contract(bx)
        pose[0], landmark[0], d, gis, th = bx[0],bx[1],bx[2],bx[3], bx[4]

        Cy = CtcFwdBwd(fy,Interval(0))
        by = IntervalVector(5)
        by[0],by[1],by[2],by[3], by[4] = pose[1], landmark[1], d, gis, th
        Cy.contract(by)
        pose[1], landmark[1], d , gis, th = by[0], by[1], by[2], by[3], by[4]

        return pose, landmark


    def __cmarkss__(self, pose, landmark, d, gis, th):
        CtcPolar
        fx=Function("x", "mx", "d", "gis", "th","mx - x - d*cos(gis+th)")
        fy=Function("y", "my", "d", "gis", "th","my - y - d*sin(gis+th)")

        Cx = CtcFwdBwd(fx,Interval(0))
        bx = IntervalVector(5)
        bx[0],bx[1],bx[2],bx[3], bx[4] = pose[0], landmark[0], d, gis, th
        Cx.contract(bx)
        pose[0], landmark[0], d, gis, th = bx[0],bx[1],bx[2],bx[3], bx[4]

        Cy = CtcFwdBwd(fy,Interval(0))
        by = IntervalVector(5)
        by[0],by[1],by[2],by[3], by[4] = pose[1], landmark[1], d, gis, th
        Cy.contract(by)
        pose[1], landmark[1], d , gis, th = by[0], by[1], by[2], by[3], by[4]

        return pose, landmark


