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
app.layout = html.Div(style={'background-color': '#7f8f8d'},
                      children=[
    html.H1('Анализ продаж услуг автосервиса', style={'font-size': '250%', 'text-align': 'center', 'border': '1px solid #cc6881'}),

    # Описание дашборда
    html.P([
        'Данный дашборд предназначен для анализа продаж услуг автосервиса.',
        html.Br(),
        'Основные функции дашборда:',
        html.Br(),
        'Возможность выбора года для анализа данных.',
        html.Br(),
        'Возможность выбора услуги для более детального анализа.',
        html.Br(),
        'Визуализация данных в виде графиков для наглядного представления информации.',
        html.Br(),
        'Обновление графиков в зависимости от выбранной услуги и года, что позволяет быстро адаптировать дашборд под свои нужды.',
        html.Br(),
        'Дашборд может быть полезен для менеджеров автосервиса, аналитиков и других специалистов, которым необходимо проводить анализ продаж услуг автосервиса.',
    ], style={'font-size': '150%', 'border': '1px solid #cc6881', 'padding': '10px'}),

    # Выбор года
    html.Div([
        html.Label('Выберите год:', style={'font-size': '220%'}),
        dcc.RadioItems(
            id='year-radio',
            options=[{'label': i, 'value': i} for i in df['Год'].unique()],
            value=df['Год'].unique()[0],
            labelStyle={'display': 'block', 'font-size': '190%', 'height': '190%'}
        )
    ], style={'text-align': 'left'}),

    # Выбор услуги
    html.Div([
        html.Label('Выберите услугу:', style={'font-size': '140%'}),
        dcc.Dropdown(
            id='service-dropdown',
            options=[{'label': i, 'value': i} for i in df['Услуга'].unique()],
            value=df['Услуга'].unique()[0],
            clearable=False
        )
    ], style={'text-align': 'left'}),

    # Графики
    html.Div([
        # Колонка с графиками 1 и 3
        html.Div([
            # График 1
            dcc.Graph(id='scatter-graph', style={'border': '1px solid #cc6881'}),

            # График 3
            dcc.Graph(id='bar-chart', style={'border': '1px solid ##cc6881'})
        ], style={'display': 'flex', 'flexDirection': 'column'}),

        # График 2
        dcc.Graph(id='pie-chart', style={'border': '1px solid #cc6881'})
    ], style={'display': 'flex'})])

# Определение логики дашборда
@app.callback(
    Output('scatter-graph', 'figure'),
    [Input('service-dropdown', 'value'),
     Input('year-radio', 'value')]
)
def update_scatter_graph(selected_service, selected_year):
    # Фильтрация данных
    filtered_df = df[(df['Услуга'] == selected_service) & (df['Год'] == selected_year)]

    # Создание графика
    fig1 = go.Figure(go.Scatter(x=filtered_df['Количество'], y=filtered_df['Месяц']))
    fig1.update_layout(title='График количества продаж по месяцам',
                  xaxis_title='Количество продаж',
                  plot_bgcolor='rgb(125, 106, 106)')

    return fig1

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('service-dropdown', 'value'),
     Input('year-radio', 'value')]
)
def update_pie_chart(selected_service, selected_year):
    # Фильтрация данных
    filtered_df = df[(df['Услуга'] == selected_service) & (df['Год'] == selected_year)]

    # Создание графика
    fig2 = px.pie(filtered_df, names='Месяц', values='Прибыль', title='Прибыль по месяцам для выбранной услуги и года')
    fig2.update_layout(plot_bgcolor='rgb(125, 106, 106)')
    return fig2

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-radio', 'value')]
)
def update_bar_chart(selected_year):
    # Фильтрация данных по выбранному году
    filtered_df = df[df['Год'] == selected_year]

    # Агрегация данных по месяцам
    grouped_df = filtered_df.groupby('Месяц').agg({'Прибыль': 'sum', 'Расход': 'sum'}).reset_index()

    # Создание графика
    fig3 = go.Figure(data=[
    go.Bar(name='Прибыль', x=grouped_df['Месяц'], y=grouped_df['Прибыль']),
    go.Bar(name='Расход', x=grouped_df['Месяц'], y=grouped_df['Расход'])
])
    fig3.update_layout(
        barmode='group',
        title='Общая прибыль и расходы за месяц',
        plot_bgcolor='rgb(125, 106, 106)'
    )

    return fig3

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
