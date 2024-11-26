import shiny
import pandas as pd
import plotly.express as px
from shiny import ui, render, reactive

# Load the dataset
url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv'
data = pd.read_csv(url)

# Preprocess data if necessary (e.g., handling missing values, casting types)
data['speeding'] = data['speeding'].astype(bool)
data['alcohol'] = data['alcohol'].astype(bool)

# UI Layout
app_ui = ui.page_fluid(
    ui.panel_title("Car Crashes Analysis"),
    
    # Sidebar
    ui.sidebar_layout(
        ui.sidebar(
            ui.input_slider("pop_slider", "Population range", min=0, max=40000000, value=[0, 40000000]),
            ui.input_checkbox("speeding", "Filter speeding accidents", value=False),
            ui.input_checkbox("alcohol", "Filter alcohol-related accidents", value=False),
        ),
        ui.main_panel(
            ui.output_plot("plot"),
            ui.output_table("table")
        )
    )
)

# Server Logic
def server(input, output, session):
    
    # Reactive expression to filter the data based on user input
    @reactive.function
    def filtered_data():
        # Get the selected population range
        pop_min, pop_max = input.pop_slider
        filtered = data[(data['population'] >= pop_min) & (data['population'] <= pop_max)]
        
        # Apply additional filters for speeding and alcohol if selected
        if input.speeding:
            filtered = filtered[filtered['speeding'] == True]
        if input.alcohol:
            filtered = filtered[filtered['alcohol'] == True]
        
        return filtered
    
    # Render plot based on filtered data
    @output()
    @render.plot
    def plot():
        filtered = filtered_data()
        fig = px.scatter(filtered, x='no_previous', y='no_injuries', color='abbrev',
                         title="Car Crashes: Previous Crashes vs Injuries (Colored by State)",
                         labels={'no_previous': 'Previous Crashes', 'no_injuries': 'Number of Injuries'})
        return fig
    
    # Render table based on filtered data
    @output()
    @render.table
    def table():
        return filtered_data()

# Run the app
app = shiny.App(app_ui, server)


