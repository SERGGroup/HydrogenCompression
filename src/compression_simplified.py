from REFPROPConnector import ThermodynamicPoint
from sty import ef
import numpy


class CompressionSimplified:

    def __init__(

            self,

            T_IC=35,
            P_max=300,
            P_start=1,
            P_in=30,

            n_stages=3,
            flow_rate=0.002,
            tank_volume=3,

            staging_mode="Standard"

    ):

        self.T_IC = T_IC
        self.P_max = P_max
        self.P_start = P_start
        self.P_in = P_in

        self.n_stages = n_stages
        self.flow_rate = flow_rate
        self.tank_volume = tank_volume

        self.staging_mode = staging_mode

        self.__init_points()
        self.__init_other_values()

    def __init_points(self):

        self.tmp_tp = ThermodynamicPoint(["Hydrogen"], [1])
        self.tp_points = list()

        for i in range(self.n_stages * 2 + 1):

            self.tp_points.append(ThermodynamicPoint(["Hydrogen"], [1]))
            self.tp_points[i].set_variable("P", self.P_in / 10)
            self.tp_points[i].set_variable("T", self.T_IC)

        self.__comp_power_list = list()

        for i in range(self.n_stages):

            self.__comp_power_list.append(0.)

    def __init_other_values(self):

        self.m_start = -1
        self.m_end = -1
        self.t_max = -1

        beta_max = self.P_max / self.P_in
        self.comp_beta_max = numpy.power(beta_max, 1 / self.n_stages)

        self.__calculate_initial_mass()
        self.__calculate_t_max()
        self.update_state(0)

    def __calculate_initial_mass(self):

        self.tmp_tp.set_variable("P", self.P_start / 10)
        self.tmp_tp.set_variable("T", self.T_IC)

        self.m_start = self.tmp_tp.get_variable("rho") * self.tank_volume

    def __calculate_t_max(self):

        if self.m_start == -1:

            self.__calculate_initial_mass()

        self.tmp_tp.set_variable("P", self.P_max / 10)
        self.tmp_tp.set_variable("T", self.T_IC)

        self.m_end = self.tmp_tp.get_variable("rho") * self.tank_volume
        self.t_max = (self.m_end - self.m_start) / self.flow_rate

    def update_state(self, time):

        if time > self.t_max:

            time = self.t_max

        m_tot = time * self.flow_rate + self.m_start
        rho = m_tot / self.tank_volume

        self.__init_points()
        self.tp_points[-1].set_variable("rho", rho)
        self.tp_points[-1].set_variable("T", self.T_IC)

        self.__update_points()

    def __update_points(self):

        P_tank = self.tp_points[-1].get_variable("P")
        P_in = self.tp_points[0].get_variable("P")

        if P_tank > P_in:

            beta_tot = P_tank / P_in

            for n in range(self.n_stages):

                if beta_tot < pow(self.comp_beta_max, n):

                    break

                if n > 0:

                    beta_old = pow(self.comp_beta_max, n)
                    beta_stage = beta_tot / beta_old

                else:

                    beta_stage = beta_tot

                if beta_stage > self.comp_beta_max:

                    beta_stage = self.comp_beta_max

                self.__calculate_compression_stage(n, beta_stage)

    def __calculate_compression_stage(self, n, beta):

        i_0 = 2 * n

        P_in = self.tp_points[i_0].get_variable("P")
        h_in = self.tp_points[i_0].get_variable("h")
        s_in = self.tp_points[i_0].get_variable("s")

        self.tmp_tp.set_variable("P", beta * P_in)
        self.tmp_tp.set_variable("s", s_in)

        h_out_iso = self.tmp_tp.get_variable("h")
        h_out = (h_out_iso - h_in) / self.eta_comp(beta) + h_in

        self.tp_points[i_0 + 1].set_variable("P", beta * P_in)
        self.tp_points[i_0 + 1].set_variable("h", h_out)

        self.tp_points[i_0 + 2].set_variable("P", beta * P_in)
        self.tp_points[i_0 + 2].set_variable("T", self.T_IC)

        self.__comp_power_list[n] = self.flow_rate * (h_out - h_in)

    def stage_P_activation(self, n_stage):

        return pow(self.comp_beta_max, n_stage) * self.P_in

    def stage_P_max(self, n_stage):

        return self.stage_P_activation(n_stage + 1)

    def eta_comp(self, beta):

        return 0.65

    @property
    def comp_power(self):

        return sum(self.__comp_power_list)

    def __str__(self):

        class Formats:

            def __init__(self, n_element):

                table_width = 147
                col_width = int(table_width / n_element)
                actual_table_width = col_width * n_element

                self.__title = (ef.bold + "{:^" + str(actual_table_width) + "}" + ef.rs)
                self.__format_string = "{:^" + str(col_width) + "}"
                self.__format_first_column = ef.bold + "{:<" + str(col_width) + "}" + ef.rs
                self.__number_format_string = "{:.2f}"
                self.__header_format = ef.bold + self.__format_string + ef.rs
                self.__units_format = ef.italic + self.__format_string + ef.rs

            def format_number(self, number):

                try:

                    return self.__format_string.format(self.__number_format_string.format(number))

                except:

                    return self.__format_string.format(str(number))

            def format_header(self, header):
                return self.__header_format.format(header)

            def format_units(self, unit):
                return self.__units_format.format(unit)

            def format_title(self, title):
                return self.__title.format(title)

            def format_first_column(self, element):
                return self.__format_first_column.format(element)

        return "\n\n{}\n\n".format(

            self.__format_points_table(Formats)

        )

    def __format_points_table(self, formats):

        table_name = "POINTS"
        header_list = ["P", "T", "h", "s", "rho"]

        frm = formats(len(header_list) + 1)

        rows_str = ""
        header_string = frm.format_first_column("Point")
        units_string = frm.format_first_column("-")
        counter = 0

        for point in self.tp_points:

            row_str = frm.format_first_column(counter)
            counter += 1

            for element in header_list:

                if point == self.tp_points[0]:

                    header_string += frm.format_header(element)
                    units_string += frm.format_units(point.get_unit(element))

                row_str += frm.format_number(point.get_variable(element))

            rows_str += "\n{}".format(row_str)

        return "\n{}\n\n{}\n{}\n{}".format(

            frm.format_title(table_name),
            header_string,
            units_string,
            rows_str

        )