import pandas as pd
import numpy as np
import math

class DataProcessor:
    def __init__(self, namespace):
        self.namespace = namespace
        
    
    def unify_received_points(self, df: pd.DataFrame) -> pd.DataFrame:
        points_recived_in_enrolment_percentage = []
        for ind in df.index:
            if df[self.namespace.points_received_in_enrolment][ind] >= 1000:
                points_recived_in_enrolment_percentage.append(105)
                continue 
            if df[self.namespace.start_year_enrolment_course[0]][ind] >=2020 :
                points_recived_in_enrolment_percentage.append((df[self.namespace.points_received_in_enrolment][ind]/220) * 100)
            
            elif df[self.namespace.start_year_enrolment_course[0]][ind] == 2018 or df[self.namespace.start_year_enrolment_course[0]][ind] == 2019:
                points_recived_in_enrolment_percentage.append((df[self.namespace.points_received_in_enrolment][ind]/125) * 100)

            else :
                points_recived_in_enrolment_percentage.append((df[self.namespace.points_received_in_enrolment][ind]/100) * 100)

        df['points_recived_in_enrolment_percentage'] = points_recived_in_enrolment_percentage
        return df
    

    def success_measure(self, df_enrolment, df_diploma):
        df_enrolment_copy = df_enrolment.copy()
        df_diploma_copy = df_diploma.copy()

        df_enrolment_without_duplicates = df_enrolment_copy.drop_duplicates( subset=[self.namespace.person_identification_number_enrolment], keep='last')

        df_diploma_copy['duplicated'] = df_diploma_copy[self.namespace.person_identification_number_diploma].duplicated()
        df_diploma_copy['success_on_diploma']=np.where(df_diploma_copy[self.namespace.date_of_exam].notna(), 100, 0)

        df_diploma_copy.rename(columns = {self.namespace.person_identification_number_diploma:self.namespace.person_identification_number_enrolment}, inplace = True)
        result_of_success = pd.merge(df_enrolment_without_duplicates, df_diploma_copy, on=self.namespace.person_identification_number_enrolment)

        result_of_success['success'] = np.where((result_of_success[self.namespace.start_year_enrolment_course[1]]==result_of_success[self.namespace.start_year_diploma_course[1]]) & (result_of_success['success_on_diploma'] == 100), 100, 0)

      
        labels = ["{:.2f} - {:.2f}".format(i + 0.01, i + 10.00) for i in range(0, 110, 10)]
        labels[-1] = "> 100"
        result_of_success['enrolmment_points'] = pd.cut(result_of_success.points_recived_in_enrolment_percentage, range(0, 111, 10), right=True, labels=labels)

        # Normalize by counting candidates in the specific range of enromment_points
        width = pd.value_counts(result_of_success['enrolmment_points'], sort=False)   
        count_of_candidates = []
        for index, value in width.items():
            count_of_candidates.append(value)
            if value != 0:
                width[index] = math.log(value, 10) * 0.2
            else:
                width[index] = 0
    
        result_of_success = result_of_success.groupby('enrolmment_points')['success'].mean()
        result_of_success=result_of_success.reset_index()

        return result_of_success, width, count_of_candidates

    
    def avg_measure(self, df_enrolment, df_diploma):

        df_enrolment_copy = df_enrolment.copy()
        df_diploma_copy = df_diploma.copy()

        df_enrolment_without_duplicates = df_enrolment_copy.drop_duplicates( subset=[self.namespace.person_identification_number_enrolment], keep='last')
        
        df_diploma_copy['duplicated'] = df_diploma_copy[self.namespace.person_identification_number_diploma].duplicated()
        
        df_diploma_copy['average_range'] = df_diploma_copy['average'].str.replace(',', '.').astype(float)

        df_diploma_copy.rename(columns = {self.namespace.person_identification_number_diploma:self.namespace.person_identification_number_enrolment}, inplace = True)

        result_of_avg = pd.merge(df_enrolment_without_duplicates, df_diploma_copy, on=self.namespace.person_identification_number_enrolment)

        labels = ["{:.2f} - {:.2f}".format(i + 0.01, i + 10.00) for i in range(0, 110, 10)]
        labels[-1] = "> 100"

        result_of_avg['enrolmment_points'] = pd.cut(result_of_avg.points_recived_in_enrolment_percentage, range(0, 111, 10), right=True, labels=labels)
        result_of_avg = result_of_avg.sort_values(by='enrolmment_points')

        return result_of_avg
    
    @staticmethod
    def find_label(points):
        # Given labels list
        labels = ["{:.2f} - {:.2f}".format(i + 0.01, i + 10.00) for i in range(0, 110, 10)]

        if points > 100:
            return "> 100"

        # Iterate through labels and check if 'points' is in any label
        matching_label = None
        for label in labels:
            start_range, end_range = map(float, label.split(' - '))
            
            if start_range <= points <= end_range:
                matching_label = label
                break

        if matching_label is not None:
            return matching_label
        else:
            return None
