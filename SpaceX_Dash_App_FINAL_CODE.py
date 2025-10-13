# Debra Elkins
# Coursera - Build an Interactive Dashboard with Plotly Dash
# Elkins_SpaceX_Dash_AppCODE.py


#---------------------------------------------------------------------------------
# Setup packages with command line installation for 1st time terminal configuration
# These lines of code install packages for Pandas, Dash and Plotly
#---------------------------------------------------------------------------------
#python3.11 -m pip install pandas dash

#To run this file in terminal command line
# python3.11 Elkins_SpaceX_Dash_AppCODE.py


#---------------------------------------------------------------------------------
# Now import Python Libraries for Pandas, Dash, Plotly 
#---------------------------------------------------------------------------------
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

#---------------------------------------------------------------------------------
# GET THE DATA 
# Note: can run the following line in the terminal to download the csv file
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Read the SpaceX data in spacex_launch_dash.csv into a Pandas dataframe
#---------------------------------------------------------------------------------
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application object instance
app = dash.Dash(__name__)


# Create a List of Drop-Down Report Options for the Dash Layout
dropdown_options = [
	{'label': 'All Sites', 'value': 'ALL'},
	{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
	{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
	{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
	{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
    ]

# Create the Dash app layout
app.layout = html.Div(children=[
	html.H1('SpaceX Launch Records Dashboard',
	style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
        
	# TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        html.Div([
		html.Label('Launch Site:', style ={'margin-right': '2em'}), 
		dcc.Dropdown(
			id='site-dropdown',
			options = dropdown_options,
			value = 'ALL',
			placeholder = 'Select a Launch Site here',
			style = {'width':'80%', 'padding':3, 'font-size':20, 'align-items':'center'},
			searchable = True
			)
		]),

	html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

    # TASK 3: Add a slider to select payload range
    # Have min_payload and max_payload already defined from spacex_df
    html.P("Payload range (Kg):"),
    html.Div(dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=[min_payload, max_payload])),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),

#end layout design
])


#---------------------------------------------------------------------------------
# CREATE CALLBACK FUNCTIONS TO MANAGE INTERACTIVITY ON DASHBOARD
#---------------------------------------------------------------------------------
# TASK 2:
# Add a callback function for `site-dropdown` as INPUT, `success-pie-chart` as OUTPUT

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

# If ALL selected, return the outcomes PIE CHART showing percent of launch successes by site
# Else if a site was selected, return a PIE CHART with the success vs failure percentages for the site
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')['class'].sum()
        fig = px.pie(filtered_df, values=filtered_df.values, names= filtered_df.index, title='Total Successful Launches for All Sites')
        return fig
    elif entered_site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        site_df = filtered_df.groupby('class').size()
        labels = ['Failure - 0', 'Success - 1']
        fig = px.pie(site_df, values=site_df.values, names = labels, title='Total Successful Launches by Site CCAFS LC-40')
        return fig
    elif entered_site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        site_df = filtered_df.groupby('class').size()
        labels = ['Failure - 0', 'Success - 1']
        fig = px.pie(site_df, values=site_df.values, names = labels, title='Total Successful Launches by Site CCAFS SLC-40')
        return fig
    elif entered_site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        site_df = filtered_df.groupby('class').size()
        labels = ['Failure - 0', 'Success - 1']
        fig = px.pie(site_df, values=site_df.values, names = labels, title='Total Successful Launches by Site KSC LC-39A')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        site_df = filtered_df.groupby('class').size()
        labels = ['Failure - 0', 'Success - 1']
        fig = px.pie(site_df, values=site_df.values, names = labels,  title='Total Successful Launches by Site VAFB SLC-4E')
        return fig
    else:
        return None          	



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as INPUTS, `success-payload-scatter-chart` as OUTPUT
@app.callback(
	Output(component_id='success-payload-scatter-chart', component_property='figure'),
	[
	Input(component_id='site-dropdown', component_property='value'), 
	Input(component_id="payload-slider", component_property="value")
	])

# filter to select data pass in as INPUT in the payload_range = [min_load, max_load]
def update_output(site, payload_range):
    min_load = payload_range[0]
    max_load = payload_range[1]
    if site == 'ALL':
        filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= min_load) & (spacex_df["Payload Mass (kg)"] <= max_load)]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for ALL Sites")
        return fig
    elif site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        site_df = filtered_df[(filtered_df["Payload Mass (kg)"] >= min_load) & (filtered_df["Payload Mass (kg)"] <= max_load)]
        fig = px.scatter(site_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for CCAFS LC-40")
        return fig
    elif site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        site_df = filtered_df[(filtered_df["Payload Mass (kg)"] >= min_load) & (filtered_df["Payload Mass (kg)"] <= max_load)]
        fig = px.scatter(site_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for CAFS SLC-40")
        return fig
    elif site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        site_df = filtered_df[(filtered_df["Payload Mass (kg)"] >= min_load) & (filtered_df["Payload Mass (kg)"] <= max_load)]
        fig = px.scatter(site_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for KSC LC-39A")
        return fig
    elif site == 'VAFB SLC-4E':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        site_df = filtered_df[(filtered_df["Payload Mass (kg)"] >= min_load) & (filtered_df["Payload Mass (kg)"] <= max_load)]
        fig = px.scatter(site_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title="Correlation between Payload and Success for VAFB SLC-4E")
        return fig
    else:
	    return None

#---------------------------------------------------------------------------------
# ACTIVATE THE DASHBOARD TO RUN AS A WEB APPLICATION
#---------------------------------------------------------------------------------
# Run the Dash app on port 8090
if __name__ == '__main__':
    app.run(debug=True, port=8090)
