import cv2
import os

from pathway import pathway

def clear_old_rois(roi_folder):
    for i in os.listdir(roi_folder):
        if i[0:3] == "roi":
            os.remove(pathway(roi_folder, i)) # https://www.w3schools.com/python/python_file_remove.asp

def get_rois(img_path, roi_folder):
    image = cv2.imread(img_path)
    thresh, image_bw = cv2.threshold( # a bit of preprocessing
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), # grayscaling
        127,
        255,
        cv2.THRESH_BINARY
    )

    contours, hierarchy = cv2.findContours(
        image_bw, # the preprocessed image
        cv2.RETR_CCOMP,
        cv2.CHAIN_APPROX_SIMPLE
    )
    contours_poly = [None]*len(contours)
    bboxes = [] # bounding boxes list

    for n, i in enumerate(contours): # search for bounding boxes
        if hierarchy[0][n][3] == -1:
            contours_poly[n] = cv2.approxPolyDP(i, 3, True)
            bboxes.append(cv2.boundingRect(contours_poly[n]))

    bboxes.sort(key=lambda i: i[0]) # sorts based on the x-positions of the bboxes; https://www.w3schools.com/python/ref_list_sort.asp

    for n, i in enumerate(bboxes):
        x, y, w, h = i
        inverted = 255-image_bw
        roi = inverted[y:y+h, x:x+w]
        cv2.imwrite(
            pathway(roi_folder, f"roi{n}.png"),
            roi
        )

    bboxes_result = image.copy() # copy image for what's next
    for i in range(len(bboxes)): # draws the bounding boxes on the (copied) input image:
        color = (0, 255, 0)
        cv2.rectangle(
            bboxes_result, 
            (int(bboxes[i][0]), int(bboxes[i][1])), 
            (int(bboxes[i][0] + bboxes[i][2]), int(bboxes[i][1] + bboxes[i][3])), 
            color, 
            2
        )
    cv2.imwrite(
        pathway(roi_folder, "bboxes_result.png"),
        bboxes_result
    )

if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname) # now the working directory is set to the file path

    img_path = pathway(os.getcwd(), "img.png")
    roi_folder = pathway(os.getcwd(), "rois")

    get_rois(img_path, roi_folder)