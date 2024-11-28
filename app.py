from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from shiny import reactive
from shiny.express import render, ui

# Load the data
@reactive.calc
def dat():
    infile = Path(__file__).parent / "car_crashes.csv"
    try:
        return pd.read_csv(infile)
    except FileNotFoundError:
        return pd.DataFrame()  # Return an empty DataFrame if file is not found
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})  # Show error message in the table

# Reactive plot for crashes by state using a choropleth map
@reactive.calc
def map_data():
    data = dat()
    if data.empty or 'abbrev' not in data.columns or 'total' not in data.columns:
        return None  # If data or necessary columns are missing, return None

    # Group the data by state abbreviation and sum the total crashes
    state_data = data.groupby('abbrev')['total'].sum().reset_index()

    # Plotly Choropleth Map
    fig = px.choropleth(state_data,
                        locations="abbrev",
                        locationmode="USA-states",
                        color="total",
                        hover_name="abbrev",
                        color_continuous_scale="Viridis",
                        title="Total Crashes by State",
                        labels={"total": "Total Crashes", "abbrev": "State"})
    
    
    # Update layout for better appearance
    fig.update_geos(showcoastlines=True, coastlinecolor="Black", projection_type="albers usa")
    fig.update_layout(
        geo=dict(scope="usa", projection_scale=5),
        title="Total Crashes by State"
    )

    return fig


# Reactive plot for Total Crashes vs Speeding with Trend Line
@reactive.calc
def plot_data():
    data = dat()
    if data.empty or 'speeding' not in data.columns or 'total' not in data.columns:
        return None  # If data or necessary columns are missing, return None

    # Create a scatter plot of points only
    fig = px.scatter(data, x='speeding', y='total', 
                     title="Total Crashes vs Speeding",
                     labels={"speeding": "Speeding Incidents", "total": "Total Crashes"})

    # Add a trend line using numpy for a simple linear fit
    x_vals = data['speeding']
    y_vals = data['total']
    trend_line = np.polyfit(x_vals, y_vals, 1)  # Fit a linear trend line
    trend_line_fn = np.poly1d(trend_line)
    x_range = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_range = trend_line_fn(x_range)

    # Add the trend line to the plot
    fig.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', name='Trend Line', line=dict(color='red', width=2)))

    return fig
    
# Reactive plot for Alcohol vs Total Crashes
@reactive.calc
def alcohol_plot():
    data = dat()
    if data.empty or 'alcohol' not in data.columns or 'total' not in data.columns:
        return None  # If data or necessary columns are missing, return None

    # Create a scatter plot of points only
    fig = px.scatter(data, x='alcohol', y='total', 
                     title="Alcohol vs Total Crashes",
                     labels={"alcohol": "Alcohol-Related Crashes", "total": "Total Crashes"})

    # Add a trend line using numpy for a simple linear fit
    x_vals = data['alcohol']
    y_vals = data['total']
    trend_line = np.polyfit(x_vals, y_vals, 1)  # Fit a linear trend line
    trend_line_fn = np.poly1d(trend_line)
    x_range = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_range = trend_line_fn(x_range)

    # Add the trend line to the plot
    fig.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', name='Trend Line', line=dict(color='red', width=2)))

    return fig


# Page title
ui.page_opts(title="Car Crashes Data Analysis", fillable=True)

with ui.sidebar(open="open"):
    ui.h5("Filters and Options")
    ui.hr()

with ui.navset_card_underline():

    # Data frame panel
    with ui.nav_panel("Data frame"):
        @render.data_frame
        def frame():
            return dat()

    # Table panel
    with ui.nav_panel("Table"):
        @render.table
        def table():
            return dat()

    # Plot panel for Total Crashes vs Speeding with Trend Line
    with ui.nav_panel("Total Crashes vs Speeding"):
        @render.ui
        def plot_speeding():
            fig = plot_data()
            if fig:
                return ui.HTML(fig.to_html(full_html=False))  # Render Plotly figure as HTML
            else:
                return ui.HTML("<p>No plot available</p>")

    # Plot panel for Alcohol vs Total Crashes
    with ui.nav_panel("Alcohol vs Total Crashes"):
        @render.ui
        def plot_alcohol():
            fig = alcohol_plot()
            if fig:
                return ui.HTML(fig.to_html(full_html=False))  # Render Plotly figure as HTML
            else:
                return ui.HTML("<p>No plot available</p>")

    # Map panel for Total Crashes by State
    with ui.nav_panel("Total Crashes by State (Map)"):
        @render.ui
        def plot_map():
            fig = map_data()
            if fig:
                return ui.HTML(fig.to_html(full_html=False))  # Render Plotly figure as HTML
            else:
                return ui.HTML("<p>No map available</p>")
