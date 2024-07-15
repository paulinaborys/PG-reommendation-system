import plotly.graph_objects as go

class PlotGenerator:

    @staticmethod
    def generate_success_rate_chart(course, df_success, count_of_candidates, width, matching_label):
        title_success  = 'Współczynnik sukcesu kierunek: ' + course + ', rekrutacja w latach: 2015-2019'

        filtered_df_success = df_success[df_success['enrolmment_points'] == matching_label]
        success_rate = filtered_df_success['success'].values[0]

        color_discrete_sequence = ['#609cd4']*len(df_success)
        color_discrete_sequence[filtered_df_success.index.values[0]] = '#ec7c34'

        fig_success = go.Figure()

        fig_success.add_trace(
            go.Bar(
                x=df_success['enrolmment_points'],
                y=df_success['success'],
                text=count_of_candidates,
                textposition="inside",
                width=width,
                marker_color=color_discrete_sequence
            )
        )

        fig_success.update_layout(
            title=title_success,
            xaxis_title='Wynik punktów rekrutacyjnych [%]',
            yaxis_title='Współczynnik Sukcesu [%]'
        )

        # fig_success.show()
        # Return the success rate and the generated figure
        return success_rate, fig_success
    
    @staticmethod
    def generate_avg_rate_chart(course, df_avg, matching_label):
        print(df_avg)
        title_avg  = 'Średni wynik ze studiów: ' + course + ', rekrutacja w latach: 2015-2019'
        
        filtered_df_avg = df_avg[df_avg['enrolmment_points'] == matching_label]

        avg_rate = filtered_df_avg['average_range'].mean()
        
        fig_avg = go.Figure()

        fig_avg.add_trace(
            go.Box(
                x=df_avg['enrolmment_points'], 
                y=df_avg['average_range'],
                marker_color='#609cd4',
                boxpoints='all',
            )
        )

        fig_avg.add_trace(
            go.Box(
                x=filtered_df_avg['enrolmment_points'], 
                y=filtered_df_avg['average_range'],
                marker_color='#ec7c34',
            )
        )

        fig_avg.update_layout(
            title=title_avg,
            xaxis_title='Wynik punktów rekrutacyjnych [%]',
            yaxis_title='Średnia ocen',
            showlegend=False
        )

        # fig_avg.show()
        # Return the average rate and the generated figure
        return avg_rate, fig_avg        
       
