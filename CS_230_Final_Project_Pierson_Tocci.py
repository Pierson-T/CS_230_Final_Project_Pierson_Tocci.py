'''
Name: Pierson Tocci
CS230: Section 05
Data: Cambridge Property Database FY2022-8000-Sample
URL: *insert URL*
Description: This program is a short analysis tool regarding the data derived from the Cambridge Property Database. IN this program the user can input multiple filters as well as analyze the
results over a myriad of charts and tools. The map included only shows the top 10 highest assessed properties according to the parameters set by the user, this is both
to combat clutter on the map and to make it more digestible for the user. Please let me know if you have any questions or comments! Enjoy!
'''
import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(layout='wide')
df_properties = pd.read_csv("Cambridge_Property_Database_FY2022_8000_sample.csv")
#Map data must contain a column named "latitude" or "lat"
df_properties.rename(columns={"Latitude":"lat", "Longitude": "lon"}, inplace= True)
# print(df_properties)
df_properties_clean = df_properties.drop(['PID', 'GISID', 'BldgNum', 'StateClassCode',
                                          'Zoning', 'Map/Lot', 'YearOfAssessment', 'TaxDistrict',
                                          'Book/Page', 'Owner_Name', 'Owner_CoOwnerName', 'Owner_Address', 'Owner_Address2',
                                          'Owner_State', 'Owner_Zip', 'Exterior_WallHeight', 'Exterior_RoofType',
                                          'Exterior_RoofMaterial', 'Exterior_FloorLocation', ], axis=1)
# print(df_properties_clean)
# print(type(df_properties_clean.lat))
#

#ensure all properties listed have latitude/longitude and that they are numbers
df_properties_clean = df_properties_clean.dropna(axis=0, subset=['lat'])
df_properties_clean = df_properties_clean.dropna(axis=0, subset=['SaleDate'])
df_properties_clean['lat'] = pd.to_numeric(df_properties_clean['lat'])
df_properties_clean['lon'] = pd.to_numeric(df_properties_clean['lon'])



st.sidebar.subheader('Filters')


st.sidebar.text('Property Type')
condition_type = st.sidebar.radio('Filter by Condition', options=['All', 'Excellent', 'Very Good', 'Good', 'Average', 'Fair'])
if condition_type == 'All':
    pass
else:
    df_properties_clean = df_properties_clean.query('Condition_OverallCondition == @condition_type')


#create title and subtitle and format
title = '<p style="font-family:Courier; color:DarkBlue; font-size: 40px;">Cambridge Property Analysis Tool</p>'
st.markdown(title, unsafe_allow_html=True)
sub_title = '<p style="font-family:Courier; color:LightBlue; font-size: 24px;">Bentley University</p>'
st.markdown(sub_title, unsafe_allow_html=True)
st.markdown('---')

image = Image.open('Bentley Logo.png')
# st.image(image)
#center image with columns
col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.image(image)
with col3:
    st.write('')

st.markdown('---')

#create selection for user based off of property type, used selectbox for this as was most efficient for this data



selection_property_types = ['Both(Combined)',
                  'NonResidential',
                  'Residential']
selected_category = st.selectbox('Please select a property category', selection_property_types)

df_residential = df_properties_clean[df_properties_clean.ResidentialExemption == True]
df_nonresidential = df_properties_clean[df_properties_clean.ResidentialExemption != True]


if selected_category == 'Residential':
    df_properties_clean = df_residential
elif selected_category == 'NonResidential':
    df_properties_clean = df_nonresidential
else:
    pass

year_built = int(st.sidebar.text_input('Oldest Year Built:', 0))
if len(str(year_built)) == 4:
    df_properties_clean = df_properties_clean.query('Condition_YearBuilt >= @year_built')
else:
    st.sidebar.text('Please enter valid year.')
    pass



st.sidebar.markdown('---')
st.sidebar.text('Created by Pierson Tocci')
# st.sidebar.text('Pierson Tocci')
# st.sidebar.text('Bentley University')

#summary columns
col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.subheader('Value Summary')
with col3:
    st.write('')

st.markdown('---')

col1, col2, col3 = st.columns(3)

with col1:
    total_assessed_value = f'${int(df_properties_clean.AssessedValue.sum()):,}'
    st.text(total_assessed_value)
    st.text('Total Assessed Value')
with col2:
    previous_total_assessed_value = f'${int(df_properties_clean.PreviousAssessedValue.sum()):,}'
    st.text(previous_total_assessed_value)
    st.text('Total Previous Assessed Value')

with col3:
    difference_in_assessed_value = f'${int(df_properties_clean.AssessedValue.sum()) - int(df_properties_clean.PreviousAssessedValue.sum()):,}'
    st.text(difference_in_assessed_value)
    st.text('Difference')

st.markdown('---')

#charts

# df_pie_residential = df_residential.Address.count()
# df_pie_commercial = df_nonresidential.Address.count()
# pie_labels = ['Residential', 'NonResidential']
# st.write(df_pie_residential)
# df_pie = pd.DataFrame({'Residential': [df_pie_residential],
#                        'NonResidential': [df_pie_commercial]}, index=[df_properties_clean.Address.count()])
# st.write(df_pie.plot.pie(y='Residential', figsize=(5, 5))
col1, col2, col3 = st.columns(3)

with col1:

    bar_df = pd.DataFrame([('Total Value', int(df_properties_clean.AssessedValue.sum())),
                           ('Total Previous Value', int(df_properties_clean.PreviousAssessedValue.sum()))],
                          columns=('Category', 'Value')
                          )
    bar_chart = px.bar(bar_df,
                       x='Category',
                       y='Value',
                       title='Value vs Previous')
    st.plotly_chart(bar_chart, use_container_width=True)
    # st.write(bar_df.plot.bar(x='label', y='value', rot=0))

with col2:
    pie_df = pd.DataFrame(df_properties_clean.groupby('ResidentialExemption').ResidentialExemption.count()).rename(columns={'ResidentialExemption':'count'}).reset_index()
    pie1 = px.pie(pie_df,
                values='count',
                names='ResidentialExemption',
                color='ResidentialExemption',
                color_discrete_map={True: 'blue', False: 'red'},
                title='Residential vs NonResidential')
    st.plotly_chart(pie1, use_container_width=True)

with col3:
    bar_df_2 = pd.DataFrame([('Total Building Value', int(df_properties_clean.BuildingValue.sum())),
                           ('Total Land Value', int(df_properties_clean.LandValue.sum()))],
                          columns=('Category', 'Value')
                          )
    bar_chart_2 = px.bar(bar_df_2,
                       x='Category',
                       y='Value',
                       title='Building vs Land Value')
    st.plotly_chart(bar_chart_2, use_container_width=True)

# pie1 = px.pie(df_pie_residential, labels=pie_labels, autopct='%.2f%%')
# st.write(pie1)


# st.write(df_properties_clean)
st.markdown('---')
#map showing top ten highest value properties within queries
df_properties_map = df_properties_clean[['lat', 'lon', 'SaleDate', 'AssessedValue']]
s2 = df_properties_map.sort_values(['AssessedValue'], ascending=False)
# st.write(s2)
s3 = s2[:10]
# st.write(s3)
# df_properties_map.sort_values.AssessedValue
# st.write(df_properties_map)
# df_properties_map['AssessedValue'] = df_properties_clean['AssessedValue'].nlargest(n=10)

# st.map(s3)

st.subheader("Map of 10 Highest Assessed Properties")

# Create custom icons
ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Home-icon.svg/1200px-Home-icon.svg.png" # Get the custom icon online
#Icon or picture finder: https://commons.wikimedia.org/

# Format your icon
icon_data = {
    "url": ICON_URL,
    "width": 100,
    "height": 100,
    "anchorY": 100
    }

# Add icons to your dataframe
s3["icon_data"]= None
for i in s3.index:
    s3["icon_data"][i] = icon_data

# Create a layer with your custom icon
icon_layer = pdk.Layer(type="IconLayer",
                        data = s3,
                        get_icon="icon_data",
                        get_position='[lon,lat]',
                        get_size=4,
                        size_scale=10,
                        pickable=True)

# Create a view of the map: https://pydeck.gl/view.html
view_state = pdk.ViewState(
    latitude=s3["lat"].mean(),
    longitude=s3["lon"].mean(),
    zoom=11,
    pitch=0
    )

# stylish tool tip: https://pydeck.gl/tooltip.html?highlight=tooltip
tool_tip = {"html": "Assessed Value:<br/> <b>{AssessedValue}</b>",
            "style": { "backgroundColor": "orange",
                        "color": "white"}
            }


icon_map = pdk.Deck(
    map_style='mapbox://styles/mapbox/navigation-day-v1',
    layers=[icon_layer],
    initial_view_state= view_state,
    tooltip = tool_tip)

st.pydeck_chart(icon_map)

