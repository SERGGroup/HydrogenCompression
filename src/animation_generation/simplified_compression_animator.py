from src.animation_generation.costants import IMG_DIRECTORY, OUTPUT_DIRECTORY
from src.animation_generation.animation_elements.gauge import plot_gauge
from src.compression_simplified import CompressionSimplified
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from PIL import Image
import os


class CompressionSimplifiedAnimator:

    def __init__(self, compression_stage:CompressionSimplified):

        self.cs = compression_stage
        self.cs.update_state(self.cs.t_max)
        self.x_max = self.cs.t_max / 60 * 1.1
        self.y_max = [self.cs.comp_power * 1.1, self.cs.P_max * 1.1]
        self.colors = ['blue', 'orange']

        self.__init_values()

    def __init_values(self):

        self.x_values = list()
        self.y_values = list()
        self.y_right_values = list()

    def __append_values(self, i):

        t = self.cs.t_max * float(i) / 100
        self.cs.update_state(t)

        self.x_values.append(t / 60)
        self.y_values.append(self.cs.comp_power)
        self.y_right_values.append(self.cs.tp_points[-1].get_variable("P") * 10)

    def __calculate_gauge_perc(self, stage=None):



        return max(0, min(perc_gauge, 1))

    def __init_figure(self):

        self.__init_values()
        self.im = Image.open(os.path.join(IMG_DIRECTORY, "prova.png"))
        self.height = self.im.size[1]

        self.fig, self.main_axes = plt.subplots(figsize=(16,10))
        self.main_axes.set_axis_off()
        return self.fig

    def __init_gauges_axes(self):

        ax = self.main_axes.inset_axes([0.25, 0.25, 0.1, 0.1])

        gauge_perc = self.__calculate_gauge_perc()
        plot_gauge(ax, gauge_perc, pointer_color="0")

    def __generate_power_plot(self, ax):

        p = ax.plot(self.x_values, self.y_values, label='Comp Power', zorder=1)
        p[0].set_color(self.colors[0])

        ax_right = ax.twinx()
        p = ax_right.plot(self.x_values, self.y_right_values, label='Tank Pressure', zorder=2)
        p[0].set_color(self.colors[1])

        ax.set_xlim([0, self.x_max])
        ax.set_ylim([0, self.y_max[0]])
        ax_right.set_ylim([0, self.y_max[1]])

        ax.set_xlabel('Time [min]')
        ax.set_ylabel('Compressors Power [kW]\n({})'.format(self.colors[0]))
        ax_right.set_ylabel('Tank Pressure [bar]\n({})'.format(self.colors[1]))

    def generate_frame(self, i=100, plot_img_alone=False):

            if not plot_img_alone:

                self.__append_values(i)

            else:

                self.__init_figure()

                for i in range(0, 100 + 5, 5):

                    self.__append_values(i)

            ax = self.main_axes.inset_axes([0.75, 0.75, 0.3, 0.3])
            self.__generate_power_plot(ax)
            self.__init_gauges_axes()

            if plot_img_alone:

                plt.show()

    def generate_plot_frame(self, i=100, plot_img_alone=False):

            if not plot_img_alone:

                self.__append_values(i)

            else:

                self.__init_figure()

                for i in range(0, 100 + 5, 5):

                    self.__append_values(i)

            self.__generate_power_plot(self.main_axes)

            if plot_img_alone:

                plt.show()

    def export_filling_gif(self, plot_only=False, gif_name="filling", step=1):

        file_name = gif_name + ".gif"
        file_path = os.path.join(OUTPUT_DIRECTORY, file_name)

        if plot_only:

            func = self.generate_plot_frame

        else:

            func = self.generate_frame

        # noinspection PyTypeChecker
        mpl_animator = ani.FuncAnimation(

            self.__init_figure(), func,
            interval=1, frames=range(0, 100 + step, step),
            repeat=False

        )

        mpl_animator.save(file_path, dpi=300)
        print("!Completed!")

    def export_frame(self, plot_only=False, i=100):

        if plot_only:

            func = self.generate_plot_frame

        else:

            func = self.generate_frame

        func(i=i, plot_img_alone=True)


if __name__ == "__main__":

    cs = CompressionSimplified()
    animator = CompressionSimplifiedAnimator(cs)
    animator.export_filling_gif(gif_name="filling", step=2)
    # animator.export_frame()