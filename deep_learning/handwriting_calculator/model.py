import os
from fastai.vision.all import *

from pathway import pathway

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname) # now the working directory is set to the file path

model = pathway(os.getcwd(), "model.pkl")
learner = load_learner(model)

if __name__ == "__main__":
    # roi_folder = pathway(os.getcwd(), "rois")
    # if any([i[0:3] == "roi" for i in os.listdir(roi_folder)]): # test-running this file will work only if there's an available roi for testing
    #     test_roi = pathway(roi_folder, "roi0.png")
    #     print(
    #         learner.predict(test_roi)
    #     )

    roi_border = pathway(os.getcwd(), "rois_bordered")
    for i in os.listdir(roi_border):
        path = pathway(roi_border, i)
        print(
            learner.predict(path)[0]
        )