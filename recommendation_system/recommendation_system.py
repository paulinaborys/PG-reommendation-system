from flask import render_template, request

import json
import plotly

from data_processing.data_loader import DataLoader
from data_processing.data_processor import DataProcessor
from plot_generation.plot_generator import PlotGenerator

from private.namespace_private import NamespacePrivate

class RecommendationSystem:

    def __init__(self) -> None:
        self.success_rate_winner_index = 0
        self.avg_rate_winner_index = 0
        # TODO Provide the path to the place where the data is stored
        self.data_path = ''
        self.valid_courses_licencjat = ["Analityka gospodarcza", "Ekonomia", "Matematyka", "Zarządzanie"]
        self.valid_courses_brak_danych = ["Automatyka, robotyka i systemy sterowania", 
                                        "Budowa maszyn i okrętów", 
                                        "Fizyka techniczna", 
                                        "Inżynieria danych", 
                                        "Inżynieria mechaniczno-medyczna", 
                                        "Inżynieria odzysku surowców i energii", 
                                        "Okręty i konstrukcje morskie", 
                                        "Projektowanie i budowa jachtów", 
                                        "Technologie wodorowe i elektromobilność", 
                                        "Transport i logistyka", 
                                        "Zielone technologie"]
        self.valid_courses_skomplikowana_analiza = ["Architektura"]
        self.namespace = NamespacePrivate()

        
   
    def find_index_winner_course(self, success_winner_list, avg_winner_list):
        max_success = max(success_winner_list)
        max_avg = max(avg_winner_list)
        return success_winner_list.index(max_success), avg_winner_list.index(max_avg)

    
    def unify_points_this_year(self, points):
        # TODO Normalize the points to the maximum in the year of using the system
        if points >= 1000:
            points = 105.0
        else:
            points = round(((points/220) * 100), 2)  
        return points

    def index(self):
        return render_template('index.html')

    def candidate_recommendation(self):
        data = request.form

        # Name of the candiate
        name = data['imie']

        # Candidate's points from the enrolment
        points_enrolment = data['punkty']
        if not points_enrolment:
            error_messages = "Pole 'Punkty rekrutacyjne' jest wymagane."
            return render_template('index.html', error_messages=error_messages)
        try:
            points_enrolment = float(points_enrolment)
            points = self.unify_points_this_year(points=points_enrolment)
        except ValueError:
            error_messages = "Błędne dane. Proszę podaj wartość liczbową."
            return render_template('index.html', error_messages=error_messages)

        # Courses - preferences of the candidate
        courses=[]
        if data['wybor1'] != 'Wybierz':
            courses.append(data['wybor1'])
        if data['wybor2'] != 'Wybierz':
            courses.append(data['wybor2'])
        if data['wybor3'] != 'Wybierz': 
            courses.append(data['wybor3']) 
        if data['wybor4'] != 'Wybierz':
            courses.append(data['wybor4']) 
        if data['wybor5'] != 'Wybierz':
            courses.append(data['wybor5'])

        if not courses:
            error_messages = "Conajmniej jednen kierunek jest wymagany."
            return render_template('index.html', error_messages=error_messages)

        graphJSON_success = []
        success_rate_list = []
        succes_winner_list =[]

        graphJSON_avg = []
        avg_rate_list = []
        avg_winner_list =[]

        messages=[]

        for course in courses:
            if course in self.valid_courses_licencjat:
                m = "Wybrany kurs to studia I stopnia - licencjackie. Ten system posiada analizy wyłącznie dla studiów I stopnia - inżynierskie."
                messages.append(m)
                success_rate_list.append('Brak danych')
                avg_rate_list.append('Brak danych')

                succes_winner_list.append(0)
                avg_winner_list.append(0)

                graphJSON_success.append(None)
                graphJSON_avg.append(None)
            
            elif course in self.valid_courses_brak_danych:
                m = "Dla wybranego kursu nie ma wystarczającej ilości danych historycznych do przeprowadzenia wiarygodnych analiz."
                messages.append(m)
                success_rate_list.append('Brak danych')
                avg_rate_list.append('Brak danych')

                succes_winner_list.append(0)
                avg_winner_list.append(0)

                graphJSON_success.append(None)
                graphJSON_avg.append(None)
            
            elif course in self.valid_courses_skomplikowana_analiza:
                m = "Wybrany kurs posiada skomplikowany proces rekrutacji, którego nie można znormalizować."
                messages.append(m)
                success_rate_list.append('Brak danych')
                avg_rate_list.append('Brak danych')

                succes_winner_list.append(0)
                avg_winner_list.append(0)

                graphJSON_success.append(None)
                graphJSON_avg.append(None)
            
            else:
                m = "Przedstawiam analizę."
                messages.append(m)

                # Load data
                data_loader = DataLoader(course=course, path=self.data_path)
                df_enrolment = data_loader.load_enrolment_data()
                df_diploma = data_loader.load_diploma_data()

                # Process data
                data_processor = DataProcessor(namespace=self.namespace)
                df_enrolment = data_processor.unify_received_points(df_enrolment)
                matching_label = data_processor.find_label(float(points))

                df_success, width, count_of_candidates = data_processor.success_measure(df_enrolment=df_enrolment, df_diploma=df_diploma)
                df_avg = data_processor.avg_measure(df_enrolment=df_enrolment, df_diploma=df_diploma)
                
                # Generate plots
                plot_generator = PlotGenerator()

                # Success
                success_rate, fig_success = plot_generator.generate_success_rate_chart(course=course, df_success=df_success,count_of_candidates=count_of_candidates, width=width, matching_label=matching_label)
                succes_winner_list.append(success_rate)
                success_rate = f"{round(success_rate, 2)}%"
                success_rate_list.append(success_rate)

                # Average
                avg_rate, fig_avg = plot_generator.generate_avg_rate_chart(course=course, df_avg=df_avg, matching_label=matching_label)
                avg_rate = (round(avg_rate, 2))
                avg_winner_list.append(avg_rate)
                avg_rate_list.append(avg_rate)

                graphJSON_success.append(json.dumps(fig_success, cls=plotly.utils.PlotlyJSONEncoder))
                graphJSON_avg.append(json.dumps(fig_avg, cls=plotly.utils.PlotlyJSONEncoder))

        # Find the best choices of the course based on success and avg
        self.success_rate_winner_index, self.avg_rate_winner_index = self.find_index_winner_course(success_winner_list=succes_winner_list, avg_winner_list=avg_winner_list)

        points = f"{points}%"
        return render_template('candidateresults.html',
                                name=name, 
                                points_enrolment=points_enrolment, 
                                points=points, 
                                courses=courses, 
                                messages=messages, 
                                success_rate_list=success_rate_list, 
                                avg_rate_list=avg_rate_list,
                                success_rate_winner_index=self.success_rate_winner_index,
                                avg_rate_winner_index=self.avg_rate_winner_index,
                                graphJSON_success=graphJSON_success, 
                                graphJSON_avg=graphJSON_avg)

