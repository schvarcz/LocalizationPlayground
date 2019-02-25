from pyibex import *
import logging, sys
import numpy as np

class IAContractorsLocalization():
    """ Perfoms the robot's localization using contractors over the distance function """
    def __init__(self, landmarks, initialPose=IntervalVector([[0,0]]*3)):
        self.poses = [initialPose]
        self.landmarks = landmarks
        self.__lastData__ = None

    def localize(self,data):
        if self.__lastData__ == None:
            self.__lastData__ = data
        dt = data.time-self.__lastData__.time

        #Movement model
        self.__lastPose__ = self.poses[-1]
        dth = Interval(data.omega-.2,data.omega+.2)
        v = Interval(data.V-.2,data.V+.2)
        dt = Interval(dt-.1,dt+.1)


        logging.debug("Contracting by movement.")
        actualPose = self.__cstate__(self.__lastPose__, dth, v, dt)


        #Contracting by landmarks
        logging.debug("Contracting by landmarks.")
        for idx in range(self.numLandmarks()):
            gis = Interval(data.z_gis[idx]-0.2,data.z_gis[idx]+0.2)

            landmark = IntervalVector([
                [self.landmarks[idx][0],self.landmarks[idx][0]],
                [self.landmarks[idx][1],self.landmarks[idx][1]]])

            actualPose = self.__cmarks__(actualPose, landmark, gis)
            # if actualPose.is_empty():
            #     actualPose = IntervalVector([[float("-inf"),float("inf")]]*3)


        logging.debug("Robot's pose"+str(actualPose))
        self.poses.append(actualPose)
        self.__lastData__ = data
        return actualPose


    def numLandmarks(self):
        return len(self.landmarks)


    def actualPose(self):
        return self.poses[-1]


    def __cstate__(self, lastPose, dth, v, dt):
        actualPose = lastPose.copy()
        actualPose[2] = lastPose[2] + dth*dt
        actualPose[0] = lastPose[0] + cos(actualPose[2])*v*dt
        actualPose[1] = lastPose[1] + sin(actualPose[2])*v*dt
        return actualPose


    def __cmarks__(self, pose, landmark, gis):
        fx=Function("x", "mx", "d", "gis", "th","mx - x - d*cos(gis+th)")
        fy=Function("y", "my", "d", "gis", "th","my - y - d*sin(gis+th)")

        d = sqrt(sqr(landmark[0]-pose[0]) + sqr(landmark[1]-pose[1]))

        Cx = CtcFwdBwd(fx,Interval(0))
        bx = IntervalVector(5)
        bx[0],bx[1],bx[2],bx[3], bx[4] = pose[0], landmark[0], d, gis, pose[2]
        Cx.contract(bx)
        pose[0],landmark[0], d , gis, pose[2] = bx[0],bx[1],bx[2],bx[3], bx[4]

        Cy = CtcFwdBwd(fy,Interval(0))
        by = IntervalVector(5)
        by[0],by[1],by[2],by[3], by[4] = pose[1], landmark[1], d, gis, pose[2]
        Cy.contract(by)
        pose[1], landmark[1], d , gis, pose[2] = by[0], by[1], by[2], by[3], by[4]

        return pose


class IASubpavingLocalization():

    """ Perfoms the robot's localization using subpavings over the tangent function """
    def __init__(self, landmarks, initialPose=IntervalVector([[float(-100),float(100)]]*3)):
        self.poses = [[[initialPose],[initialPose]]]
        self.landmarks = landmarks
        self.__lastData__ = None


    def localize(self,data):
        if self.__lastData__ == None:
            self.__lastData__ = data
        dt = data.time-self.__lastData__.time

        #Movement model
        self.__lastPose__ = self.poses[-1]
        dth = Interval(data.omega-.2,data.omega+.2)
        v = Interval(data.V-.2,data.V+.2)
        dt = Interval(dt-.1,dt+.1)
        th_error = Interval(np.deg2rad(10),np.deg2rad(10))


        logging.debug("Subpaving by movement.")
        actualPose = self.__cstate__(self.__lastPose__, dth, v, dt)

        #Contracting by landmarks
        logging.debug("Subpaving by landmarks.")
        for idx in range(1):#self.numLandmarks()):
            gis = Interval(data.z_gis[idx],data.z_gis[idx])

            landmark = IntervalVector([
                [self.landmarks[idx][0],self.landmarks[idx][0]],
                [self.landmarks[idx][1],self.landmarks[idx][1]]])

            actualPose = self.__cmarks__(actualPose, landmark, gis, th_error)

        logging.debug("Robot's pose"+str(actualPose))
        self.poses.append(actualPose)
        self.__lastData__ = data
        return actualPose


    def numLandmarks(self):
        return len(self.landmarks)


    def actualPose(self):
        return self.poses[-1]

    def __cstate__(self, lastPose, dth, v, dt):
        set_return = []
        for boxes_set in lastPose:
            boxes_return = []
            for box in boxes_set:
                actualBox = box.copy()
                actualBox[2] = box[2] + dth.mid()*dt.mid()
                actualBox[0] = box[0] + cos(actualBox[2])*v*dt
                actualBox[1] = box[1] + sin(actualBox[2])*v*dt
                boxes_return.append(actualBox)
            set_return.append(boxes_return)
        return set_return


    """ Not working for the unknow initialPose """
    def __cmarks__(self, pose, landmark, gis, th_error):
        f1=Function("x", "y", "th", "mx", "my", "gis", "th_error", "(mx-x)*sin(th-gis+th_error)-(my-y)*cos(th-gis+th_error)")
        sep1 = SepFwdBwd(f1,Interval(0,float("inf")))

        f2=Function("x", "y", "th", "mx", "my", "gis", "th_error", "(my-y)*cos(th-gis-th_error)-(mx-x)*sin(th-gis-th_error)")
        sep2 = SepFwdBwd(f2,Interval(0,float("inf")))

        sep = (sep1 & sep2)

        boxes_in_ret, boxes_out_ret, boxes_maybe_ret = [[],]*3
        logging.debug("Starting to contract")
        logging.debug(pose)
        for set_boxes in pose:
            for box in set_boxes:

                # logging.debug("Starting SIVIA")
                b = IntervalVector([box[0], box[1], Interval(0,0), landmark[0], landmark[1], gis, th_error])
                boxes_in, boxes_out, boxes_maybe = pySIVIA(b,sep,0.1,draw_boxes=True)

                logging.debug(box)
                for box in boxes_in:
                    if not box.is_empty():
                        v = IntervalVector(3)
                        v[0], v[1], v[2] = box[0], box[1], box[2]
                        boxes_in_ret.append(v)
                        # logging.debug(v)


                for box in boxes_out:
                    if not box.is_empty():
                        v = IntervalVector(3)
                        v[0], v[1], v[2] = box[0], box[1], box[2]
                        boxes_out_ret.append(v)
                        # logging.debug(v)


                for box in boxes_maybe:
                    if not box.is_empty():
                        v = IntervalVector(3)
                        v[0], v[1], v[2] = box[0], box[1], box[2]
                        boxes_maybe_ret.append(v)
                        # logging.debug(v)

                # logging.debug(boxes_in)
                # logging.debug("comp")
                # logging.debug(boxes_in[0])
                # logging.debug(IntervalVector(boxes_in[0]))


        return boxes_in_ret, boxes_maybe_ret



if __name__ == "__main__":
    pass
