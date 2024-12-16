import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient
import re
import random


app = dash.Dash(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client['Bibliometrics']
collection = db['Books']


# Functions
# ---------

def only_book_available(categories_filtered):
    if 'all' in categories_filtered:
        books_list = list(collection.find({"available_stock": {"$gt": 10}}, {'category':1,'title': 1, 'price': 1, 'rating': 1, '_id': 0}))
    else:
        books_list = list(collection.find({"available_stock": {"$gt": 10}, "category": {'$in': categories_filtered}}, {'category':1,'title': 1, 'price': 1, 'rating': 1, '_id': 0}))
    return books_list

def best_rated_books(categories_filtered):
    if 'all' in categories_filtered:
        books_list = list(collection.find({"rating": {"$gt": 4}}, {'category':1,'title': 1, 'rating': 1, '_id': 0}))
    else:
        books_list = list(collection.find({"rating": {"$gt": 4}, "category": {'$in': categories_filtered}}, {'category':1,'title': 1,'rating': 1, '_id': 0}))
    return books_list

def search_in_book_title(search_input):
    search_words = search_input.split()
    
    regex_pattern = r"(?=.*{})".format(")(?=.*".join(map(re.escape, search_words)))
    
    books_list = list(collection.find({"title": {"$regex": regex_pattern, "$options": "i"}}, {'category': 1, 'title': 1, 'rating': 1, 'price': 1, '_id': 0}))
    
    return books_list

def get_random_book():
    random_book = collection.aggregate([{ "$sample": { "size": 1 }}])
    return list(random_book)[0]


# Layout
# ------

app.layout = html.Div([

    html.Div([
        html.H1("BIBLIOMETRIC'S DASHBOARD"),
    ], className='header'),
    
    html.Div([
        html.H2("📚 Number of books in each category"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-count',
                className='dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dcc.Graph(id='book-count-graph')
        ])
    ], className='request-div'),

    html.Div([
        html.H2("⭐️ Average rating for each category"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-rating',
                className='dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dcc.Graph(id='book-rating-graph')
        ])
    ], className='request-div'),

    html.Div([
        html.H2("💹 List of books with more than 10 available"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-table',
                className='dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[
                    {'name': 'Title', 'id': 'title'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Price', 'id': 'price'}, 
                    {'name': 'Rating', 'id': 'rating'}
                ],
                data=[],
                page_size=20,
                style_cell={
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'center',
                },
                style_header={'font-weight': 'bold'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'title'},
                        'minWidth': '300px',
                        'maxWidth': '600px',
                        'text-align': 'left',
                        'padding-left': '10px',
                    },
                ],
            ),
        ])
    ], className='request-div'),
    
    html.Div([
        html.Div([
            html.H2("🎲 Random Book Generator"),
            html.Button("Generate Random Book", id="random-book-button"),
        ], className='generate-title'),
        html.Div([
            html.Div(id="random-book-output"),
            # dash_table.DataTable(
            #     id='table-cover-book',
            #     columns=[{'name': 'Cover', 'id': 'cover_book', 'type' : 'text', 'presentation': 'markdown'}],
            #     data=[],
            # )
        ], className='random-book-generator'),
    ], className='request-div'),

    html.Div([
        html.H2("🥇 List of books with a 5 stars rating"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-table-rating',
                className='dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dash_table.DataTable(
                id='table-rating',
                columns=[
                    {'name': 'Title', 'id': 'title'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Rating', 'id': 'rating'}
                ],
                data=[],
                page_size=20,
                style_cell={
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'center',
                },
                style_header={'font-weight': 'bold'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'title'},
                        'minWidth': '300px',
                        'maxWidth': '600px',
                        'text-align': 'left',
                        'padding-left': '10px',
                    },
                ],  
              )
        ])
    ], className='request-div'),

    html.Div([
        html.H2("🏆 10 best priced books with 5 stars rating"),
        html.Div([
            dash_table.DataTable(
                id='table-rating-price',
                columns=[
                    {'name': 'Cover', 'id': 'cover_book', 'type' : 'text', 'presentation': 'markdown'},
                    {'name': 'Title', 'id': 'title'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Price', 'id': 'price'},
                    {'name': 'Rating', 'id': 'rating'},
                ],
                data=[],
                page_size=20,
                style_cell={
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'center',
                },
                style_header={'font-weight': 'bold'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'title'},
                        'minWidth': '300px',
                        'maxWidth': '600px',
                        'text-align': 'left',
                        'padding-left': '10px',
                    },
                ], 
            )
        ])
    ], className='request-div'),

    html.Div([
        html.H2("🥧 Books count per rating"),
        html.Div([
            dcc.Graph(id='rating-pie-chart'),
        ])
    ], className='request-div'),

    html.Div([
        html.H2("🔍 Search in title"),
        html.Div([
             dcc.Input(
                 id='search-text', 
                 type='text', 
                 placeholder='Enter text...'),
                ]),
        html.Div([
            dash_table.DataTable(
                id='table-description-found-text',
                columns=[
                    {'name': 'Title', 'id': 'title'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Price', 'id': 'price'},
                    {'name': 'Rating', 'id': 'rating'},
                ],
                data=[],
                page_size=20,
                style_cell={
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'center',
                },
                style_header={'font-weight': 'bold'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'title'},
                        'minWidth': '300px',
                        'maxWidth': '600px',
                        'text-align': 'left',
                        'padding-left': '10px',
                    },
                ], 
                 
            )
            
            
        ])
        
    ], className='request-div'),

    dcc.Interval(
        id='interval-component',
        interval=60000, 
        n_intervals=0
    )
])



# Callbacks
# ---------

@app.callback(
    Output('category-dropdown-count', 'options'),
    [Input('category-dropdown-count', 'value')]
)
def update_dropdown_options_count(selected_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

@app.callback(
    Output('book-count-graph', 'figure'),
    [Input('category-dropdown-count', 'value')]
)
def update_count_graph(selected_categories):
    if 'all' in selected_categories:
        filtered_data = collection.find({})
    elif not selected_categories:
        filtered_data = collection.find({})
    else:
        filtered_data = collection.find({'category': {'$in': selected_categories}})
    
    df = pd.DataFrame(list(filtered_data))
    book_count = df['category'].value_counts().reset_index()
    book_count.columns = ['category', 'count']
    
    colors = px.colors.qualitative.Set3[:len(book_count)]
    
    fig = px.bar(book_count, x='category', y='count', color='category', color_discrete_sequence=colors)

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig


@app.callback(
    Output('category-dropdown-rating', 'options'),
    [Input('category-dropdown-rating', 'value')]
)
def update_dropdown_options_rating(selected_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

@app.callback(
    Output('book-rating-graph', 'figure'),
    [Input('category-dropdown-rating', 'value')]
)
def update_rating_graph(selected_categories):
    if 'all' in selected_categories:
        filtered_data = collection.find({})
    elif not selected_categories:
        filtered_data = collection.find({})
    else:
        filtered_data = collection.find({'category': {'$in': selected_categories}})
    
    df = pd.DataFrame(list(filtered_data))
    
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    avg_rating = df.groupby('category')['rating'].mean().reset_index()
    
    avg_rating = avg_rating.sort_values(by='rating', ascending=False)
    
    fig = px.bar(avg_rating, x='category', y='rating', color='category', color_discrete_sequence=px.colors.qualitative.Set3)

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig


@app.callback(
    Output('category-dropdown-table', 'options'),
    [Input('category-dropdown-table', 'value')]
)
def update_dropdown_options_table(filtered_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

@app.callback(
    Output('table', 'data'),
    [Input('category-dropdown-table', 'value')]
)
def update_table(filtered_categories):
    data = only_book_available(filtered_categories)
    return data


@app.callback(
    Output('category-dropdown-table-rating', 'options'),
    [Input('category-dropdown-table-rating', 'value')]
)
def update_dropdown_options_table_rating(selected_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

@app.callback(
    Output('table-rating', 'data'),
    [Input('category-dropdown-table-rating', 'value')]
)
def update_table_rating(filtered_categories):
    data = best_rated_books(filtered_categories)
    return data


@app.callback(
    Output('rating-pie-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_pie_chart(selected_categories):
    books = list(collection.find({}, {'title': 1, 'rating': 1}))
    
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for book in books:
        rating = book['rating']
        rating_counts[rating] += 1
    
    fig = px.pie(
        names=[f'Rating {rating}' for rating in rating_counts.keys()],
        values=list(rating_counts.values()),
        hole=0.3
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig


@app.callback(
    Output('table-rating-price', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def update_table_best_price(best_price_and_rating):
    best_price_and_rating = list(collection.find({"rating": {"$gt": 4}}, {'category': 1, 'title': 1, 'rating': 1,'price':1, 'cover_book': 1, '_id': 0}).sort("price", 1).limit(10))
    for e in best_price_and_rating:
        e['cover_book'] = f"![image]({e['cover_book']})"
    
    return best_price_and_rating


@app.callback(
    Output('search-text', 'value'),
    [Input('search-text', 'value')]
)
def update_search_text_value(search_text):
    return search_text

@app.callback(
    Output('table-description-found-text', 'data'),
    [Input('search-text', 'value')]
)
def update_table_found_text(search_text):
    if search_text:
        data = search_in_book_title(search_text)
        return data
    else:
        return []


@app.callback(
    Output("random-book-output", "children"),
    [Input("random-book-button", "n_clicks")]
)
def update_random_book_info(n_clicks):
    if n_clicks:
        book = get_random_book()
        return html.Div([
            html.Img(src=book["cover_book"], alt="Cover Image"),
            html.Div([
                html.H3(book["title"]),
                html.H4(f"Category : {book['category']}"),
                html.P(f"{book['description']}"),
                # html.P(f"Description: {translated_description}")
            ], className='random-book-desc')
        ], className='random-book-container')
        


# def translate_description(description, target_language='fr'):
#     inputs = translation_tokenizer(description, return_tensors="pt", truncation=True, padding=True)
#     translated = translation_model.generate(**inputs, max_length=128, num_beams=4, early_stopping=True)
#     translated_text = translation_tokenizer.batch_decode(translated, skip_special_tokens=True)
#     translated_description = translated_text[0]  # Accéder au premier élément de la liste
#     return translated_description

# # Load translation model and tokenizer
# translation_model_name = "Helsinki-NLP/opus-mt-en-fr"
# translation_model = MarianMTModel.from_pretrained(translation_model_name)
# translation_tokenizer = MarianTokenizer.from_pretrained(translation_model_name)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)