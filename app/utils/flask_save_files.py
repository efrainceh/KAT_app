import os

from werkzeug.utils import secure_filename


class FlaskSaveFiles():
    
    def __init__(self, app):
        self.app = app
        self.sample_path = ""
        self.reference_path = ""
        self.sample_folder = "Samples"
        self.reference_folder = "References"
        
    def __create_project_dir(self, run_path):
        self.sample_path = os.path.join(run_path, self.sample_folder)
        os.mkdir(self.sample_path)
        self.reference_path = os.path.join(run_path, self.reference_folder)
        os.mkdir(self.reference_path)

    def __save_files(self, path, files):
        self.app.config['UPLOAD_FOLDER'] = path
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(path, filename))

    def save(self, run_path, sample_files, reference_files):
        self.__create_project_dir(run_path)
        self.__save_files(self.sample_path, sample_files)
        self.__save_files(self.reference_path, reference_files)
