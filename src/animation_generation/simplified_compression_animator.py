from src.animation_generation.animation_elements.stages_image import plot_stages
from src.compression_simplified import CompressionSimplified
from src.costants import OUTPUT_DIRECTORY
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import tqdm
import os


class CompressionSimplifiedAnimator:

    def __init__(self, compression_stage:CompressionSimplified):

        self.cs = compression_stage
        self.cs.update_state(self.cs.t_max)
        self.x_max = self.cs.t_max / 60 * 1.1
        self.colors = ['blue', 'orange']
        self.end_frame = 100

        self.plot_power = True

        self.__init_values()

    def __init_values(self):

        self.x_values = list()
        self.y_values = list()
        self.y_right_values = list()

    def __append_values(self, i):

        t = self.cs.t_max * float(i) / 100
        self.cs.update_state(t)

        self.x_values.append(t / 60)

        if self.plot_power:

            self.split_axis = True
            self.plot_texts = {

                "y_left": {

                    "legend_label": "Comp Power",
                    "axis_label": 'Compressors Power [kW]'

                },
                "y_right": {

                    "legend_label": "Tank Pressure",
                    "axis_label": 'Tank Pressure [bar]'

                }

            }
            self.y_values.append(self.cs.comp_power)
            self.y_right_values.append(self.cs.tp_points[-1].get_variable("P") * 10)

        else:

            self.split_axis = True
            self.plot_texts = {

                "y_left": {

                    "legend_label": "Curr Efficiency",
                    "axis_label": 'Efficiency [-]'

                },
                "y_right": {

                    "legend_label": "Comp Power",
                    "axis_label": 'Compressors Power [kW]'

                }

            }

            self.y_values.append(self.cs.current_efficiency())
            self.y_right_values.append(self.cs.comp_power())

        self.__update_progress_bar(i)

    def __init_figure(self):

        self.__init_values()

        self.fig, self.main_axes = plt.subplots(figsize=(10,10))
        self.main_axes.set_axis_off()
        return self.fig

    def __generate_power_plot(self, ax):

        p = ax.plot(self.x_values, self.y_values, label=self.plot_texts["y_left"]["legend_label"], zorder=1)
        p[0].set_color(self.colors[0])

        if self.split_axis:

            ax_right = ax.twinx()

        else:

            ax_right = ax

        p_right = ax_right.plot(self.x_values, self.y_right_values, label=self.plot_texts["y_right"]["legend_label"], zorder=2)
        p_right[0].set_color(self.colors[1])

        ax.set_xlim([0, self.x_max])
        ax.set_xlabel('Time [min]', backgroundcolor="white")
        ax.set_ylabel(self.plot_texts["y_left"]["axis_label"], backgroundcolor="white")

        if self.split_axis:

            ax.set_ylim([0, max(self.y_values) * 1.1])
            ax_right.set_ylim([0, max(self.y_right_values) * 1.1])
            ax_right.set_ylabel(self.plot_texts["y_right"]["axis_label"], backgroundcolor="white")

        else:

            ax.set_ylim([min(min(self.y_values), min(self.y_right_values)) * 0.9, max(max(self.y_values), max(self.y_right_values)) * 1.1])

        lns = p + p_right
        labs = [l.get_label() for l in lns]
        ax.legend(lns, labs, loc=4)

    def __update_progress_bar(self, i):

        try:

            i_old = self.progress_bar.n
            self.progress_bar.update(i - i_old)

        except:

            self.progress_bar = tqdm.trange(self.end_frame)

    def generate_frame(self, i=100, plot_img_alone=False):

            if not plot_img_alone:

                self.__append_values(i)

            else:

                self.__init_figure()
                self.main_axes.set_axis_on()

                for i in range(0, 100 + 5, 5):

                    self.__append_values(i)

            plot_stages(self.main_axes, self.cs)
            ax = self.main_axes.inset_axes([0.65, 0.2, 0.35, 0.3])
            self.__generate_power_plot(ax)

            if plot_img_alone:

                plt.show()

    def generate_plot_frame(self, i=100, plot_img_alone=False):

            if not plot_img_alone:

                self.__append_values(i)

            else:

                self.__init_figure()
                self.main_axes.set_axis_on()

                for i in range(0, 100 + 5, 5):

                    self.__append_values(i)

            self.__generate_power_plot(self.main_axes)

            if plot_img_alone:

                plt.show()

    def export_filling_gif(

            self, plot_only=False,
            gif_name="filling", plot_power=True,
            step=1, dpi=300, end_frame=100

    ):

        self.plot_power = plot_power

        self.end_frame = end_frame
        file_name = gif_name + ".gif"
        file_path = os.path.join(OUTPUT_DIRECTORY, "gif", file_name)

        if plot_only:

            func = self.generate_plot_frame

        else:

            func = self.generate_frame

        # noinspection PyTypeChecker
        mpl_animator = ani.FuncAnimation(

            self.__init_figure(), func,
            interval=1, frames=range(0, end_frame, step),
            repeat=False

        )

        mpl_animator.save(file_path, dpi=dpi)
        print("!Completed!")

    def export_frame(self, plot_only=False, i=100, plot_power=True):

        self.plot_power = plot_power

        if plot_only:

            func = self.generate_plot_frame

        else:

            func = self.generate_frame

        func(i=i, plot_img_alone=True)


if __name__ == "__main__":

    cs = CompressionSimplified(n_stages=3, P_max=300)
    animator = CompressionSimplifiedAnimator(cs)
    # animator.export_filling_gif(
    #
    #     gif_name="filling-300bar-3stages",
    #     step=4, dpi=200, end_frame=120
    #
    # )
    animator.export_frame(plot_only=True, plot_power=False)