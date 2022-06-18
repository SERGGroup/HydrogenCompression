from src.compression_simplified import CompressionSimplified
from src.data_IO.excel_exporter import export_to_excel
from src.costants import OUTPUT_DIRECTORY
import tqdm, os


class ExportDict():

    def __init__(self, cs: CompressionSimplified):

        self.cs = cs
        self.export_prop_list = ["T", "P", "h", "s", "rho"]

        self.export_dict = {

            "time": list(),

            "comp_power": list(),
            "H2_amount": list(),

            "eta": list(),
            "eta_chemical": list()

        }

        for i in range(self.cs.n_stages):
            self.export_dict.update({

                "comp_{}_power".format(i + 1): list(),
                "IC_{}_power".format(i + 1): list()

            })

        for prop in self.export_prop_list:

            for i in range(len(self.cs.tp_points)):

                self.export_dict.update({"{}_{}".format(prop, i + 1): list()})

    def append_values_to_dict(self, i):

        t = self.cs.t_max * float(i) / 100
        self.cs.update_state(t)

        self.export_dict["time"].append(self.cs.time)

        self.export_dict["comp_power"].append(self.cs.comp_power)
        self.export_dict["H2_amount"].append(self.cs.flow_rate * self.cs.time)
        self.export_dict["eta"].append(self.cs.current_efficiency(consider_chemichal_power=False))
        self.export_dict["eta_chemical"].append(self.cs.current_efficiency(consider_chemichal_power=True))

        for i in range(self.cs.n_stages):
            self.export_dict["comp_{}_power".format(i + 1)].append(self.cs.comp_power_list[i])
            self.export_dict["IC_{}_power".format(i + 1)].append(self.cs.IC_power_list[i])

        for prop in self.export_prop_list:

            for i in range(len(self.cs.tp_points)):

                self.export_dict["{}_{}".format(prop, i + 1)].append(self.cs.tp_points[i].get_variable(prop))


@export_to_excel(

    excel_dir_path=os.path.join(OUTPUT_DIRECTORY, "excel"),
    excel_name="compression_analysis"

)
def compression_analysis(P_max=300, n_stages=3, step=2):

    ed = ExportDict(CompressionSimplified(

        P_max=P_max,
        n_stages=n_stages

    ))

    pbar = tqdm.tqdm(total=100)

    for i in range(0, 100 + step, step):

        ed.append_values_to_dict(i)
        pbar.update(step)

    pbar.close()
    return ed.export_dict


if __name__ == "__main__":

    compression_analysis()
