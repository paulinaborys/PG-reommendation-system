import pandas as pd

class DataLoader:
    def __init__(self, course, path):
        self.course = course
        self.path = path

    def load_enrolment_data(self):
        # Load enrolment data from self.path based on self.course
        files_path_enrolment = self.path + self.course + '/'
        all_enrolment_data = [files_path_enrolment + 'enrolment.csv']
        df_enrolment = pd.concat(
            map(pd.read_csv, all_enrolment_data), ignore_index=True)
        
        # Return the loaded DataFrame
        return df_enrolment

    def load_diploma_data(self):
        # Load diploma data from self.path based on self.course
        files_path_diploma = self.path + self.course + '/'
        all_diploma_data = [files_path_diploma + 'diploma.csv']
        df_diploma = pd.concat(
                map(pd.read_csv, all_diploma_data), ignore_index=True)
        
        # Return the loaded DataFrame
        return df_diploma
