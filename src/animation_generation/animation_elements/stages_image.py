from src.animation_generation.animation_elements.gauge import plot_gauge
from src.compression_simplified import CompressionSimplified
from src.costants import IMG_DIRECTORY
import matplotlib.pyplot as plt
import os


HW_ratios = {

    "": 0.4317,
    "Last": 1.2,
    "First": 0.4317

}

start_x_movement = 0.73

def plot_stages(

        axis, cs: CompressionSimplified

):
    activation_list = list()
    perc_list = list()

    n_stages = cs.n_stages
    P_tank = cs.tp_points[-1].get_variable("P") * 10

    for stage in range(n_stages):

        is_active = (P_tank >= cs.stage_P_activation(stage))

        if is_active:

            P_max = cs.stage_P_max(stage)
            P_min = cs.stage_P_activation(stage)

            perc_gauge = (P_tank - P_min) / (P_max - P_min)

        else:

            perc_gauge = 0.

        activation_list.append(is_active)
        perc_list.append(max(0., min(1., perc_gauge)))

    __plot_stages(axis, n_stages, activation_list, perc_list)


def __plot_stages(

        axis, n_stages,
        activation_list,
        perc_list

):
    axis.set_axis_off()
    best_height = __calculate_best_height(axis, n_stages)
    start_x = 0

    if n_stages > 1:

        start_x += __add_stage(

            axis, is_active=activation_list[0], perc=perc_list[0],
            stage_type="First", height=best_height

        )

    for stage in range(1, n_stages - 1):

        start_x += __add_stage(

            axis, is_active=activation_list[stage], perc=perc_list[stage],
            prev_is_active=activation_list[stage-1],
            start_x=start_x, height=best_height

        )

    if n_stages>2:
        pre_active = activation_list[-2]
    else:
        pre_active = False

    __add_stage(

        axis, is_active=activation_list[-1], perc=perc_list[-1],
        prev_is_active=pre_active, start_x=start_x,
        stage_type="Last", height=best_height

    )


def __add_stage(

        axis, is_active, perc,
        prev_is_active=True,
        start_x=0, stage_type="",
        height=0.5

):

    ax = axis.inset_axes([start_x, 0, HW_ratios[stage_type]*height, height])
    ax.set_axis_off()

    if is_active:

        active_name = "Active"
        prev_active_name = ""

    else:

        active_name = "Inactive"
        prev_active_name = ""

        if not stage_type == "First" and not prev_is_active:
            prev_active_name = "-Inactive"

    img = plt.imread(os.path.join(IMG_DIRECTORY, "stages", "{}Stage-{}{}.png".format(stage_type, active_name, prev_active_name)))
    ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')

    __add_gauge(ax, perc, stage_type=stage_type)

    return start_x_movement * HW_ratios[stage_type] * height


def __add_gauge(ax, perc=0., stage_type=""):

    figW, figH = ax.get_figure().get_size_inches()
    _, _, w, h = ax.get_position().bounds
    axis_ratio = (figH * h) / (figW * w)

    if stage_type == "Last":

        position = [0.18, 0.88, 0.1 * axis_ratio, 0.1]

    else:

        position = [0.48, 0.88, 0.1 * axis_ratio, 0.1]

    gauge_ax = ax.inset_axes(position)
    gauge_ax.set_axis_off()
    plot_gauge(

        gauge_ax, perc,
        pointer_color='0.5',
        noise_sigma=0.02

    )


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
    cs = CompressionSimplified()
    cs.update_state(5000)
    plot_stages(ax, cs)
    plt.show()
