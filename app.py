import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
import ModelSavingLogic
import plotly.express as px
import copy
import flask
import os
import random

def no_fig():
    return None
def null_el_function():
        return  html.Div()
        

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(random.randint(0, 1000000)))
app = dash.Dash(__name__, server=server)


def run(row_data_figure=no_fig,
        selector_data=pd.read_csv(r"Data\dash_selector_data.csv")):
    selector_data=selector_data.loc[:, ~selector_data.columns.str.contains('^Unnamed')]
    selector_data.insert(0,'id',selector_data.index)
    selector_data=selector_data[selector_data["ModelPredictions"]>0.5]

    selection_table = dash_table.DataTable(
            id='row-selector',
            columns=[
                {'name': i, 'id': i, 'deletable': False} for i in selector_data.columns
            ],
            data=selector_data.to_dict("records"),
            row_selectable='single',
            sort_action="native",
            selected_rows=[],
            editable=False,
            page_size=10
    )

    selection_table_element=html.Div(
            children=[selection_table],
            style={
                        'height':'60vh',
                        'overflow':'auto'
					 })    
   

    app.layout = html.Div([selection_table_element,
        html.Div(id="model-results"),
    ])

    @app.callback(
    Output('model-results', 'children'),
    [Input('row-selector', 'selected_row_ids')])
    def update_model_component(selected_row_ids):
        if selected_row_ids is None:
            return null_el_function()
        if len(selected_row_ids)<1:
            return null_el_function()
        
        fig=row_data_figure(selected_row_ids[0])

        if fig is None:
            return null_el_function()

        return dcc.Graph(figure=fig)

    
    app.run_server(debug=True,threaded=True)




if __name__ == '__main__':
    test_data=pd.read_csv(r"Data\test_data_encoded.csv")
    test_data = test_data.loc[:, ~test_data.columns.str.contains('^Unnamed')]
    test_x = test_data.drop('Attrition',axis=1)## We wil not use the test_y here to simulate the real use case
    test_data=None
    test_data=test_x
    model=ModelSavingLogic.get_best_model("max_hyper_param_testing_random_forrest")

    def get_graph(index):
        data_row = test_data.iloc[index]
        monthly = data_row["MonthlyIncome"]

        graph_data=pd.DataFrame()

        for i in range(0,21): #percent hike proposals from 0-20%
            row = copy.deepcopy(data_row)
            proposal = monthly*(1+(i/100))
            row["MonthlyIncome"]=proposal

            row_df=pd.DataFrame()
            row_df=row_df.append(row)
            prediction= model.predict_proba(row_df)[0][1]
            graph_data=graph_data.append({"salary_bump_percentage":i,"attrition_prob":prediction},ignore_index=True)

        fig =  px.line(graph_data, 
        x="salary_bump_percentage", 
        y="attrition_prob", 
        title='Probability of attrition given salary hike for employee ID '+str(index))

        return fig

    run(row_data_figure=get_graph)

