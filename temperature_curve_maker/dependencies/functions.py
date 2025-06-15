from PIL import Image, ImageTk
import numpy as np

def only_floats(input_text):
    """
    Validation callback function.
    """
    if input_text == ".":
        return True
    try:
        float(input_text)
        return True
    except ValueError:
        return False
    
def height_resize(img, new_height=24):
    """
    Helper function for to_toolbar_icon().

    Resize an image to exactly the new height,
    proportionally resizing the width as well.

    Expects a PIL Image class to be passed to the
    img argument.
    """
    width, height = img.size
    new_width = int(new_height/height*width)

    return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

def to_transparent(img, threshold=240):
    """
    Helper function for to_toolbar_icon().

    Converts a regular RGB image file to a RGBA one,
    then turns all white pixels with the threshold range
    to transparent ones.
    """
    img = img.convert("RGBA")
    data = np.array(img)

    r, g, b, a = data.T # transposed to seperate channels
    white_areas = (r >= threshold) & (g >= threshold) & (b >= threshold) # create a mask of white pixels
    
    data[..., 3][white_areas.T] = 0 # set alpha channel to 0 for white pixels (note the transpose back to original shape)

    return Image.fromarray(data)

def to_toolbar_icon(img):
    """
    Takes a PIL Image instance, resizes it, then
    converts to an ImageTk instance ready to be used
    for the toolbar.
    """
    img = height_resize(img) # resize the image
    img = to_transparent(img) # turn white pixels transparent

    return ImageTk.PhotoImage(img)

def get_pid_levels(array):
    """
    Transforms an array, where the column vectors are
    of time and temperature, into just selected temperatures where
    PID regions are to be created
    """
    origin = np.array(["0", "20"], dtype=object)
    array = np.vstack((origin, array)) # first stack the origin on top
    float_array = np.where(array == "", np.nan, array).astype(float) # now this is the proper type cast

    selected_temp = np.where(np.diff(float_array[:, 1]) > 0)[0] # don't forget the origin added changes the shape

    return float_array[selected_temp+1, 1]
    
if __name__ == "__main__":
    # only_floats()
    print(only_floats("3.1415"))
    print(only_floats("Hello world!"))
    # print(
    #     get_pid_levels(
    #         np.array(
    #             [[0, 0, 0, 0, 0, 0, 0, 0],
    #              [20, 100, 100, 200, 200, 150, 150, 20]]
    #         ).T
    #     )
    # )