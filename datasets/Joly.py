#!/usr/bin/python3
import logging, os, sys

class JolyData():
    """ A class to represent the data of the Joli's datasets """
    def __init__(self, time, omega, V, Xreel, V_true, omega_true, z_gis, z_elev):
        self.time = time
        self.omega = omega
        self.V = V
        self.Xreel = Xreel
        self.pose = Xreel[0:3]
        self.V_true = V_true
        self.omega_true = omega_true
        self.z_gis = z_gis
        self.z_elev = z_elev

    def __repr__(self):
        return "{0}".format(self.time)


class JolyDataset():
    """ Loads the dataset of the Thesis of Joli Cyrill """
    def __init__(self,path):
        logging.debug("Loading dataset path: %s ..." % path)
        self.path = path
        self.load()
        logging.debug("... dataset loaded.")
        logging.debug("\n\n"+str(self)+"\n\n")


    def load(self):
        self.time = self.__loadfile__("time.csv")
        self.omega = self.__loadfile__("omega.csv")
        self.V = self.__loadfile__("V.csv")
        self.Xreel = list(zip(*self.__loadfile__("Xreel.csv")))
        self.landmarks = self.__loadfile__("landmarks.csv")
        self.V_true = self.__loadfile__("V_true.csv")
        self.omega_true = self.__loadfile__("omega_true.csv")
        self.z_gis = list(zip(*self.__loadfile__("z_gis.csv")))
        self.z_elev = list(zip(*self.__loadfile__("z_elev.csv")))

        self.Xreel = [self.Xreel[idx] for idx in range(0,len(self.Xreel),100)]
        self.poses = [ Xreel[0:3] for Xreel in self.Xreel]

        assert len(self.time) == len(self.omega)     , "The dataset is inconsistent"
        assert len(self.time) == len(self.V)         , "The dataset is inconsistent"
        assert len(self.time) == len(self.Xreel)     , "The dataset is inconsistent"
        assert len(self.time) == len(self.V_true)    , "The dataset is inconsistent"
        assert len(self.time) == len(self.omega_true), "The dataset is inconsistent"
        assert len(self.time) == len(self.z_gis)     , "The dataset is inconsistent"
        assert len(self.time) == len(self.z_elev)    , "The dataset is inconsistent"
        assert len(self.landmarks) == len(self.z_gis[0])     , "The dataset is inconsistent"
        assert len(self.landmarks) == len(self.z_elev[0])    , "The dataset is inconsistent"
        self.values = [JolyData(self.time[idx], self.omega[idx], self.V[idx], self.Xreel[idx], self.V_true[idx], self.omega_true[idx], self.z_gis[idx], self.z_elev[idx]) for idx in range(len(self.time))]

    def numLandmarks(self):
        return len(self.landmarks)

    def __len__(self):
        return len(self.time)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, idx):
        return self.values[idx]

    def __setitem__(self, idx, value):
        self.values[idx] = value

    def __repr__(self):
        return "Path: {0}\nLength: {1}\n# Landmarks: {2}".format(self.path, len(self), self.numLandmarks())

    def __loadfile__(self,filename):
        ret = [ [float(col) for col in line.split(",")] for line in open(self.path+os.path.sep+filename,"r").readlines()]
        if len(ret[0]) == 1:
            ret = [r[0] for r in ret]
        return ret


def showHelp():
    print (
    """
./Joly.py pathToCSVDataset
    """)
if __name__ == "__main__":

    logging.root.setLevel(logging.DEBUG)
    if len(sys.argv) == 2:
        dataset = JolyDataset(sys.argv[1])
    else:
        showHelp()
