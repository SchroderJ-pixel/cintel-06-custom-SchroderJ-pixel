import pandas as pd
import requests
from io import StringIO
import plotly.express as px
from shiny import App, ui, render
import faicons as fa

# Fetch Titanic dataset from GitHub raw URL
url = "https://raw.githubusercontent.com/SchroderJ-pixel/cintel-06-custom-SchroderJ-pixel/main/car_crashes.csv"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Read the CSV data into a Pandas DataFrame
    data = pd.read_csv(StringIO(response.text))
else:
    raise Exception("Failed to fetch the dataset")

# Sample plot using actual column names (update with desired columns)
fig = px.scatter(data, x='total', y='speeding', color='abbrev')

# Define UI
app_ui = ui.page_fluid(
    ui.output_ui("plot")
)

# Define server logic
def server(input, output, session):
    @output()
    @render.ui
    def plot():
        # Convert Plotly figure to HTML and return as UI element
        return ui.HTML(fig.to_html(full_html=False))

# Create the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
