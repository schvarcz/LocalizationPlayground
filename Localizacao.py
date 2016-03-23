#-*- coding: UTF-8 -*-

from datasets.Joly import *
from localization.IAMethods import *
from localization.PFMethods import *
from drawing.vibes import *
import logging

"""
Implementar o mesmo usando coordenadas polares
Usar o QItersection para a localizacao
Implementar uma versao com SubPavings para localizaçao
Fazer SLAM aqui tbm!
Implementar PF para localizacao e SLAM
"""

logging.root.setLevel(logging.DEBUG)


if __name__ == "__main__":

    dataset = JolyDataset("/home/schvarcz/SLAM/These_Cyril_JOLY/donnees_SLAM_par_Intervalles_scilab/scenar01f")

    localization = IAContractorsLocalization(dataset.landmarks)

    drawing = DrawingVibes()
    drawing.drawLandmarks(dataset.landmarks)
    # logging.debug("Running the dataset.")

    # for idx in range(len(dataset)):

    #     logging.debug("Dataset step %d" % idx)
    #     actualPose = localization.localize(dataset[idx])

    #     # drawing.drawPoses([actualPose])
    #     # drawing.drawTruePoses([dataset.poses[idx]])

    # logging.debug("Dataset is over.")


    # logging.debug("Drawing the entire process.")
    # drawing.clear()
    # drawing.drawLandmarks(dataset.landmarks)
    # drawing.drawPoses(localization.poses)
    # drawing.drawTruePoses(dataset.poses)
    # logging.debug("done.")


