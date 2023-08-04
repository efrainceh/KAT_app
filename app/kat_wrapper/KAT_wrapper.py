import os
import shutil
import subprocess
import zipfile

from pathlib import Path

from app.utils import TablePlot
from app.kat_wrapper import ALLOWED_EXTENSIONS, EXECUTABLE_FILENAME, REFERENCES_FOLDER, RESULTS_FOLDER, SAMPLES_FOLDER, TABLE_EXTENSION


class KAT():

    def __init__(self):

        self.number_of_inputs = "6"
        self.file_extension = "." + ALLOWED_EXTENSIONS[0]
        self.kat_project_name = ""
        self.project_folder_path = ""

    def run(self, kmer_size, kat_runname, project_folder_path):

        self.kat_runname = kat_runname
        self.project_folder_path = project_folder_path
        path_to_exe = os.path.abspath(EXECUTABLE_FILENAME)
        input_as_list = [path_to_exe, self.number_of_inputs, kat_runname, project_folder_path, self.file_extension, str(kmer_size)]
        process = subprocess.run(input_as_list)
        self._plot()
        self._zip()
        self._clean_up()

        return process.returncode

    def _plot(self):

        filename = self.kat_runname + TABLE_EXTENSION
        table_path = os.path.join(self.project_folder_path, RESULTS_FOLDER, filename)
        plt = TablePlot(table_path)
        plt.plot(column="hits")
        plt.save(suffix="_hits")
        plt.plot(column="percentage")
        plt.save(suffix="_percentage")

    def _zip(self):

        results_folder_path = os.path.join(self.project_folder_path, RESULTS_FOLDER)
        files = [Path(os.path.join(results_folder_path, file)) for file in os.listdir(results_folder_path)]
        zip_path = os.path.join(results_folder_path, self.kat_runname + ".zip")

        with zipfile.ZipFile(zip_path, mode="w") as archive:

            for file_path in files:
                
                archive.write(file_path, arcname=file_path.name)

    def _clean_up(self):

        # Delete sample and reference folders
        samples_folder_path = os.path.join(self.project_folder_path, SAMPLES_FOLDER)
        self._delete_folder(samples_folder_path)
        references_folder_path = os.path.join(self.project_folder_path, REFERENCES_FOLDER)
        self._delete_folder(references_folder_path)

        # Delete alignment files(.txt) and table (.csv). These are now all in the zip file
        results_folder_path = os.path.join(self.project_folder_path, RESULTS_FOLDER)
        files = os.listdir(results_folder_path)

        for file in files:
            
            if file.endswith(".txt") or file.endswith(".csv"):
                file_path = os.path.join(results_folder_path, file)
                os.remove(file_path) 

    def _delete_folder(self, folder):

        if os.path.exists(folder) and os.path.isdir(folder):
            
            shutil.rmtree(folder)