import dash
from dash import dcc, html, Input, Output
import dash_table
import pandas as pd

# Загрузка данных из CSV файла
df = pd.read_csv('research_papers.csv')

# Инициализация Dash приложения
app = dash.Dash(__name__)

app.layout = html.Div([
    # Фильтры для поиска и выбора
    html.Div([
        dcc.Input(id='search-title', type='text', placeholder='Search by title...', style={'marginRight': '10px'}),
        dcc.Input(id='search-authors', type='text', placeholder='Search by authors...', style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='filter-year',
            options=[{'label': str(year), 'value': year} for year in sorted(df['year'].unique())],
            multi=True,
            placeholder='Select year(s)...',
            style={'width': '200px', 'marginRight': '10px'}
        ),
        dcc.Dropdown(
            id='filter-category',
            options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
            multi=True,
            placeholder='Select category(ies)...',
            style={'width': '200px'}
        )
    ], style={'display': 'flex', 'marginBottom': '10px'}),
    
    # Таблица для отображения данных
    html.Div(id='table-div')
])

# Callback для обновления таблицы
@app.callback(
    Output('table-div', 'children'),
    [
        Input('search-title', 'value'), 
        Input('search-authors', 'value'),
        Input('filter-year', 'value'),
        Input('filter-category', 'value')
    ]
)
def update_table(search_title, search_authors, filter_year, filter_category):
    filtered_df = df
    if search_title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]
    if search_authors:
        filtered_df = filtered_df[filtered_df['authors'].str.contains(search_authors, case=False, na=False)]
    if filter_year:
        filtered_df = filtered_df[filtered_df['year'].isin(filter_year)]
    if filter_category:
        filtered_df = filtered_df[filtered_df['category'].isin(filter_category)]

    # Определяем стили для ячеек таблицы
    cell_style = {
        'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'normal'
    }

    table = dash_table.DataTable(
        id='datatable-paging',
        columns=[
            {"name": i, "id": i} for i in filtered_df.columns
        ],
        data=filtered_df.to_dict('records'),
        page_size=10,
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell=cell_style,
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold',
            'textAlign': 'left',
            'padding': '10px'
        },
        style_data={
            'padding': '10px'
        },
        filter_action="native",  # Включаем фильтрацию
        sort_action="native",
        sort_mode="multi",
        column_selectable="multi",
        editable=True  # Если вы хотите разрешить пользователю редактировать поля
    )

    return html.Div([
        html.H3('Research Papers Table', style={'textAlign': 'center'}),
        html.Div(table, style={'display': 'flex', 'justifyContent': 'center'})  # Обертываем таблицу для выравнивания
    ])

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
