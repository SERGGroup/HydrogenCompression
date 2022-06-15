from src.animation_generation.animation_elements.gauge import plot_gauge
from src.animation_generation.costants import IMG_DIRECTORY
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
import os


HW_ratios = {

    "": 0.4317,
    "Last": 1.2,
    "First": 0.4317

}

start_x_movement = 0.7615


def plot_stages(

        axis, n_stages,
        activation_list

):
    axis.set_axis_off()
    best_height = __calculate_best_height(axis, n_stages)
    start_x = 0

    if n_stages > 1:

        start_x += __add_stage(

            axis, is_active=activation_list[0],
            stage_type="First", height=best_height

        )

    for stage in range(1, n_stages - 1):

        start_x += __add_stage(

            axis, is_active=activation_list[stage],
            start_x=start_x, height=best_height

        )

    __add_stage(

        axis, is_active=activation_list[- 1],
        start_x=start_x, stage_type="Last",
        height=best_height

    )


def __add_stage(

        axis, is_active,
        start_x=0, stage_type="",
        height=0.5

):

    ax = axis.inset_axes([start_x, 0, HW_ratios[stage_type]*height, height])
    ax.set_axis_off()

    if is_active:

        active_name = "Active"

    else:

        active_name = "Inactive"

    img = plt.imread(os.path.join(IMG_DIRECTORY, "stages", "{}Stage-{}.png".format(stage_type, active_name)))
    ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')

    return start_x_movement * HW_ratios[stage_type] * height


def __calculate_best_height(axis, n_stages):

    figW, figH = axis.get_figure().get_size_inches()
    _, _, w, h = axis.get_position().bounds

    axis_ratio = (figH * h) / (figW * w)
    overall_ratio = HW_ratios["First"] * (n_stages - 1) + HW_ratios["Last"]

    if axis_ratio < overall_ratio:

        return 1 / overall_ratio

    else:

        return 1


if __name__ == "__main__":

    fig, ax = plt.subplots(figsize=(6, 6))
    plot_stages(ax, 3, [True,True,True, True, True, True])
    plt.show()
