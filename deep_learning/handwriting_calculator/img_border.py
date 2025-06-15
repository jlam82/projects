import os
from PIL import Image, ImageOps

from pathway import pathway

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname) # now the working directory is set to the file path

def clear_old_borders(roi_border): # complete clear of the folder
    for i in os.listdir(roi_border):
        if i[0:3] == "roi":
            os.remove(pathway(roi_border, i))

def border_rois(roi_folder, roi_border):
    n = 0 # doing add-assign instead of enumerate() because of bboxes_result.png
    for i in os.listdir(roi_folder):
        if not i == "bboxes_result.png":
            img_path = pathway(roi_folder, i)
            img = Image.open(img_path).convert("1") # load BW image; "1" mode for black and white

            bordered_img = ImageOps.expand(img, border=20, fill="white") # 20 is a good border size in pixels
            bordered_img.save(
                pathway(roi_border, f"roi{n}.png")
            )
            n += 1

if __name__ == "__main__":
    roi_folder = pathway(os.getcwd(), "rois")
    roi_border = pathway(os.getcwd(), "rois_bordered")

    clear_old_borders(roi_border)
    border_rois(roi_folder, roi_border)