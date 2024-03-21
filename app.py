# %%
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


df = pd.read_csv("gdp_pcap.csv") # gets data set

#app = dash.Dash(__name__) 


external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']  # creates stylesheet

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([ # styles the layout 

    html.H1("GDP per Capita vs Time"),
    html.P("This graph shows the GDP per Capita over time for the selected countries in the dropdown menu and the selected years on the slider. The y-axis represents the GDP per Capita, and the x-axis represents the years. There is a general positive correlation between year and GDP per Capita for countries."),

    html.Div([
        html.Div([
            html.Label('Select Country:'),
            dcc.Dropdown( # creates dropdown
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in df['country']],
                multi=True,
                value=['Afghanistan']
            ),
        ], style={'width': '25%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select Year Range:'),
            dcc.RangeSlider( # creates slider
                id='year-slider',
                min=int(df.columns[1]),
                max=int(df.columns[-1]),
                marks={year: str(year) for year in range(int(df.columns[1]), int(df.columns[-1]) + 1, 10)},
                step=1,
                value=[int(df.columns[1]), int(df.columns[-1])]
            ),
        ], style={'width': '75%', 'display': 'inline-block'}),
    ], style={'display': 'flex'}),

    dcc.Graph(id='gdp-line-chart', style={'width': '100%'}), # creates graph to be displayed

])


@app.callback( # updates the content of the graph when slider or drop down is interacted with
    Output('gdp-line-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_countries, selected_years): # updates data on line chart based off intersction
    filtered_df = df[df['country'].isin(selected_countries)] # filters the data by years selected
    years = list(range(selected_years[0], selected_years[1] + 1))
    selected_columns = [str(year) for year in years]
    
    reshaped_df = pd.melt(filtered_df, id_vars=['country'], value_vars=selected_columns, # row corresponds with a country, year, and GDP per Capita
                        var_name='Year', value_name='GDP per Capita')
    
    reshaped_df['GDP per Capita'] = pd.to_numeric(reshaped_df['GDP per Capita'], errors='coerce')

    reshaped_df.dropna(subset=['GDP per Capita'], inplace=True)

    reshaped_df = reshaped_df.sort_values(by='GDP per Capita')
    
    fig = px.line(  # creates line chart to be displayed
        reshaped_df,
        x='Year',
        y='GDP per Capita',
        color='country',
        labels={'Year': 'Year', 'GDP per Capita': 'GDP per Capita'}
    )

    fig.update_layout(   # updates the layout if the line chart
        xaxis_title='Year',
        yaxis_title='GDP per Capita',
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)



# %%
