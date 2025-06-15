import matplotlib.pyplot as plt
import numpy as np

def update(ax, xlim=[0, 1]):
    diff = xlim[1] - xlim[0]

    xlim = np.array(xlim).astype(float) # have to specify what datatype otherwise insert won't work
    xticks = np.insert(xlim, 1, np.median(xlim)) # create xticks from the xlims with the mean value included
    
    xlabels = xticks.copy().astype(str)
    xlabels[1] = f"{diff}hr"

    ax.set_xticks(xticks, xlabels, fontsize=12)

    ax_xticks = ax.xaxis.get_major_ticks() # get the ax-specific xticks variable
    ax_xticks[0].label1.set_visible(False)
    ax_xticks[-1].label1.set_visible(False) # remove tick numbers from either end

# def update(ax, xs, ys):
#     diff = xlim[1] - xlim[0]

#     xlim = np.array(xlim).astype(float) # have to specify what datatype otherwise insert won't work
#     xticks = np.insert(xlim, 1, np.median(xlim)) # create xticks from the xlims with the mean value included
    
#     xlabels = xticks.copy().astype(str)
#     xlabels[1] = f"{diff}hr"

#     ax.set_xticks(xticks, xlabels, fontsize=12)

#     ax_xticks = ax.xaxis.get_major_ticks() # get the ax-specific xticks variable
#     ax_xticks[0].label1.set_visible(False)
#     ax_xticks[-1].label1.set_visible(False) # remove tick numbers from either end

if __name__ == "__main__":
    from itertools import accumulate

    # time_intervals = [
    #     0, 12, 1, 12, 10
    # ]

    # temps = [
    #     20, 260, 260, 500, 500
    # ]

    fig, ax = plt.subplots()
    update(ax)

    plt.show()