from src.animation_generation.costants import IMG_DIRECTORY, OUTPUT_DIRECTORY
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_gauge(

        ax, perc, pointer_color="0.8",
        min_pos=225, max_pos=-45

):

    plt.axis('off')
    img = plt.imread(os.path.join(IMG_DIRECTORY, "gauge_base.png"))
    pos = (max_pos - min_pos) * perc + min_pos

    ax.arrow(

        0.5, 0.5,
        0.25 * np.cos(np.radians(pos)),
        0.25 * np.sin(np.radians(pos)),
        width=0.025, head_width=0.06,
        head_length=0.1, fc=pointer_color, ec=pointer_color,

    )

    circle = plt.Circle((0.5, 0.5), 0.035, color=pointer_color)
    ax.add_patch(circle)

    ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')


if __name__ == "__main__":

    fig, ax = plt.subplots(figsize=(6, 6))
    plot_gauge(ax, 1)
    plt.show()