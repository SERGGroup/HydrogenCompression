from datetime import date, datetime
from tkinter import filedialog
import tkinter as tk
import pandas as pd
import os


def export_to_excel(

        excel_dir_path="",
        excel_name="result.xlsx",
        add_date_time=False,
        sheet_name='data'

):

    def new_func(func):

        def new_wrapper(*args, **kwargs):

            if not os.path.isdir(excel_dir_path):

                root = tk.Tk()
                root.withdraw()

                excel_dir = filedialog.askdirectory()

            else:

                excel_dir = excel_dir_path

            if add_date_time:

                today = date.today()
                now = datetime.now()
                today_str = today.strftime("%d %b")
                now_str = now.strftime("%H.%M")

                new_excel_name = "{}_{}_{}".format(today_str, now_str, excel_name)

            else:

                new_excel_name = excel_name

            if ".xlsx" not in new_excel_name:
                new_excel_name = new_excel_name + ".xlsx"

            if os.path.isdir(excel_dir):
                output_file = os.path.join(excel_dir, new_excel_name)

                result_dict = func(*args, **kwargs)

                df = pd.DataFrame(result_dict)
                writer = pd.ExcelWriter(output_file, engine="openpyxl", mode="a")
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                writer.save()

        return new_wrapper

    return new_func
