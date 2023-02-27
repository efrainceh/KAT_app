import os
import random
import string
import subprocess
import zipfile
from pathlib import Path
from kat_variables import *
from plots import *


def random_project_name(size):
    symbols = string.ascii_letters + string.digits
    project_name = ""
    while(len(project_name) < size):
        project_name += random.choice(symbols)
    return project_name

def run_KAT_thread(kmer_size, kat_project_name, project_path, runcodes, run_id):
    kat = KAT()
    runcodes[run_id] = kat.run(kmer_size, kat_project_name, project_path)

class KAT():

    def __init__(self):
        self.number_of_inputs = "6"
        self.file_extension = "." + ALLOWED_EXTENSIONS[0]
        self.kat_project_name = ""
        self.project_path = ""

    def run(self, kmer_size, kat_project_name, project_path):
        self.kat_project_name = kat_project_name
        self.project_path = project_path
        input_as_list = [PATH_TO_EXE, self.number_of_inputs, self.kat_project_name, self.project_path, self.file_extension, str(kmer_size)]
        process = subprocess.run(input_as_list)
        self._plot()
        self._zip()
        return process.returncode

    def _plot(self):
        filename = self.kat_project_name + TABLE_EXTENSION
        table_path = os.path.join(self.project_path, RESULTS_FOLDER, filename)
        plt = TablePlot(table_path)
        plt.plot("hits")
        plt.save("_hits")
        plt.plot("percentage")
        plt.save("_percentage")

    def _zip(self):
        dir_path = os.path.join(self.project_path, RESULTS_FOLDER)
        files = [Path(os.path.join(dir_path, file)) for file in os.listdir(dir_path)]
        zip_path = os.path.join(dir_path, self.kat_project_name + ".zip")
        with zipfile.ZipFile(zip_path, mode="w") as archive:
            for file_path in files:
                archive.write(file_path, arcname=file_path.name)

