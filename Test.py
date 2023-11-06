import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# Загрузка данных
df = pd.read_csv('C:\programing\Dashbords\хуй.csv')

# Создание экземпляра приложения
app = dash.Dash(__name__)

# Определение структуры дашборда
app.layout = html.Div([
    html.H1('Анализ продаж услуг автосервиса'),

    # Выбор услуги
    html.Label('Выберите услугу:'),
    dcc.Dropdown(
        id='service-dropdown',
        options=[{'label': i, 'value': i} for i in df['Услуга'].unique()],
        value=df['Услуга'].unique()[0],
        clearable=False
    ),

    # Графики
    html.Div([
        # График 1
        dcc.Graph(id='scatter-graph'),

        # График 2
        dcc.Graph(id='pie-chart')
    ], style={'display': 'flex'})
])

# Определение логики дашборда
@app.callback(
    Output('scatter-graph', 'figure'),
    [Input('service-dropdown', 'value')]
)
def update_scatter_graph(selected_service):
    # Фильтрация данных
    filtered_df = df[df['Услуга'] == selected_service]

    # Создание графика
    fig = go.Figure(go.Scatter(x=filtered_df['Количество'], y=filtered_df['Месяц']))

    fig.update_layout(title='График количества продаж по месяцам'.format(selected_service),
                  xaxis_title='Количество продаж',
    plot_bgcolor='rgb(230, 230,230)')

    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('service-dropdown', 'value')]
)
def update_pie_chart(selected_service):
    # Фильтрация данных
    filtered_df = df[df['Услуга'] == selected_service]

    # Создание графика
    fig = px.pie(filtered_df, names='Месяц', values='Прибыль')

    fig.update_layout(title='Круговая диаграмма прибыли по месяцам')

    return fig

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
