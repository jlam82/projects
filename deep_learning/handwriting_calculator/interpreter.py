import os

from model import learner
from pathway import pathway

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
os.chdir(dirname) # now the working directory is set to the file path

superscript_dict = {
    "**0": r"\u2070", 
    "**1": r"\u00B9",
    "**2": r"\u00B2",
    "**3": r"\u00B3",
    "**4": r"\u2074",
    "**5": r"\u2075",
    "**6": r"\u2076",
    "**7": r"\u2077",
    "**8": r"\u2078",
    "**9": r"\u2079",
}

def interpret(roi_border):
    predictions = []
    for i in os.listdir(roi_border):
        roi_path = pathway(roi_border, i)
        predictions.append(
            learner.predict(roi_path)[0]
        )
    ocr_expr = "".join(predictions)

    return ocr_expr

def translate(ocr_expr):
    expr = ocr_expr # set the final string expression as the ocr expression
    
    expr = expr.replace("--", "=") # first rule 
    expr = expr.replace(")", ")*") # second rule
    for n in range(len(expr)): # third rule; only works for simplified expressions (adding extras "_x" messes up location order)
        if any(["x" == expr[n], "y" == expr[n], "z" == expr[n]]) and expr[n+1].isdigit(): # checks if the right-side of the variable is a number
            expr = expr[:n+1] + "**" + expr[n+1:] # python's end-exclusive endexing bruh
        if expr[n].isdigit() and any(["x" == expr[n+1], "y" == expr[n+1], "z" == expr[n+1]]): # checks if the left-side of the variable is a number
            expr = expr[:n+1] + "*" + expr[n+1:]
    
    return expr

def display(expr):
    raw_expr = repr(expr) # turn the expr into a raw string
    for i in superscript_dict.items():
        raw_expr = raw_expr.replace(*i)

    no_asterisks = "".join(raw_expr.split("*"))
    return no_asterisks

if __name__ == "__main__":
    roi_border = pathway(os.getcwd(), "rois_bordered")
    print(
        display(translate(interpret(roi_border)))
    )