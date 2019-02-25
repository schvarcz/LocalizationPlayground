#-*- coding: UTF-8 -*-

from datasets.Joly import *
from localization.IAMethods import *
from localization.PFMethods import *
from drawing.vibes import *
import logging, time

"""
Implementar uma versao com SubPavings para localizaçao
Implementar PF para localizacao e SLAM
Implementar o mesmo usando coordenadas polares
Usar o QItersection para a localizacao
Fazer SLAM aqui tbm!
"""

logging.root.setLevel(logging.DEBUG)


if __name__ == "__main__":

    dataset = JolyDataset("/home/schvarcz/SLAM/These_Cyril_JOLY/donnees_SLAM_par_Intervalles_scilab/scenar01f")

    drawing = DrawingVibes()

    localization = IAContractorsLocalization(dataset.landmarks)

    localization = IASubpavingLocalization(dataset.landmarks)


    logging.debug("Running the dataset.")

    # draw  ing.drawLandmarks(dataset.landmarks)
    for idx in range(len(dataset)):

        logging.debug("Dataset step %d" % idx)
        actualPose = localization.localize(dataset[idx])

        logging.debug("Drawing step %d" % idx)
        logging.debug(actualPose)
        # drawing.drawPose(actualPose)
        # drawing.drawTruePoses([dataset.poses[idx]])
        time.sleep(2)

    logging.debug("Dataset is over.")

    logging.debug("Drawing the entire process.")
    drawing.clear()
    drawing.drawLandmarks(dataset.landmarks)
    drawing.drawPoses(localization.poses)
    drawing.drawTruePoses(dataset.poses)
    logging.debug("done.")
