import pandas as pd
import matplotlib.pyplot as plt
import folium
from selenium import webdriver
import json
import os

def print_biggest_handguns(df: pd.DataFrame) -> None:
    """
    Function to print the state and year with the highest number of handguns.
    Args:
     -df (pd.DataFrame): The dataframe with data grouped by year and state.
    Returns:
     -None
    """

    # Find the row with the maximum number of handguns
    max_handguns_row = df.loc[df['handgun'].idxmax()]
    state = max_handguns_row['state']
    year = max_handguns_row['year']
    handguns = int(max_handguns_row['handgun'])

    # Print the state and year with the highest number of handguns
    print(
        f"Exercise 3 - The state with the highest number of handguns is {state}"
        f" in the year {year} with {handguns} handguns."
    )

    return state, year, handguns


def print_biggest_longguns(df: pd.DataFrame) -> None:
    """
    Function to print the state and year with the highest number of long guns.
    Args:
     -df (pd.DataFrame): The dataframe with data grouped by year and state.
    Returns:
     -None
    """

    # Find the row with the maximum number of long guns
    max_longguns_row = df.loc[df['long_gun'].idxmax()]
    state = max_longguns_row['state']
    year = max_longguns_row['year']
    longguns = int(max_longguns_row['long_gun'])

    # Print the state and year with the highest number of long guns
    print(f"Exercise 3 - The state with the highest number of long guns is "
          f"{state}in the year {year} with {longguns} long guns.")

    return state, year, longguns


def time_evolution(df: pd.DataFrame) -> None:
    """
    Function to create a time evolution graph for the number of permits,
    handguns, and long guns registered each year.
    Args:
     -df (pd.DataFrame): The dataframe with data grouped by year and state.
    Returns:
     -None
    """

    # Group by year and sum the values for each year
    yearly_data = df.groupby('year').sum().reset_index()

    # Plotting the data
    plt.figure(figsize=(12, 6))
    plt.plot(yearly_data['year'], yearly_data['permit'], label='Permits',
             marker='o')
    plt.plot(yearly_data['year'], yearly_data['handgun'], label='Handguns',
             marker='o')
    plt.plot(yearly_data['year'], yearly_data['long_gun'], label='Long Guns',
             marker='o')

    # Adding titles and labels
    plt.title('Excersise 4 - Evolution of Permits, Handguns, and Long Guns')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.legend()

    # Show the plot
    plt.show()


def analyze_state_data(df: pd.DataFrame) -> None:
    """
    Function to analyze state data and print the results as specified.
    Args:
     -df (pd.DataFrame): The dataframe with relative values calculated.
    Returns:
     -None
    """

    # Calculate and print the mean of permit_perc
    old_mean_permit_perc = df['permit_perc'].mean()
    print(f"Mean permit_perc: {old_mean_permit_perc:.2f}")

    # Print information about Kentucky
    kentucky_data = df[df['state'] == 'Kentucky']
    print("Kentucky data:")
    print(kentucky_data)

    # Replace the permit_perc value for Kentucky with the mean
    df.loc[df['state'] == 'Kentucky', 'permit_perc'] = old_mean_permit_perc

    # Recalculate and print the mean of permit_perc
    new_mean_permit_perc = df['permit_perc'].mean()
    print(f"New mean permit_perc: {new_mean_permit_perc:.2f}")

    # Print analysis
    print("Analysis:")
    print(f"The mean permit_perc changed from {old_mean_permit_perc:.2f}"
          f"to {new_mean_permit_perc:.2f}.")
    print("This change illustrates the impact of outliers on statistical "
          "metrics. In this example, we handled outliers by imputation: we "
          "imputed the mean for Kentucky with the mean of all states, to bring "
          "the metric closer to the average of our data.")

    return old_mean_permit_perc, new_mean_permit_perc


def create_choropleth_map(df: pd.DataFrame, column: str, geo_json_path: str,
                          map_title: str, output_file: str) -> None:
    """
    Function to create a choropleth map for a specific column.
    Args:
     -df (pd.DataFrame): The dataframe with the data.
     -column (str): The column to visualize.
     -geo_json_path (str): The path to the geo JSON file.
     -map_title (str): The title of the map.
     -output_file (str): The file name to save the map as an image.
    Returns:
     -None
    """

    # Load GeoJSON data
    with open(geo_json_path) as f:
        geo_data = json.load(f)

    # Create a folium map
    m = folium.Map(location=[37.8, -96], zoom_start=4)

    # Create the choropleth map
    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth',
        data=df,
        columns=['state', column],
        key_on='feature.properties.name',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=map_title
    ).add_to(m)

    # Ensure the output directory exists
    output_dir = os.path.join('data', 'maps')
    os.makedirs(output_dir, exist_ok=True)
    html_file_path = os.path.join(output_dir, f'{output_file}.html')

    # Save the map as an HTML file
    m.save(html_file_path)

    # Use Selenium to open the HTML file and save as PNG
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(f'file://{os.path.abspath(html_file_path)}')

    # Give the map some time to render
    driver.implicitly_wait(5)
    print("Rendering image... may take a few seconds...")

    # Save the screenshot
    png_file_path = os.path.join(output_dir, f'{output_file}.png')
    driver.save_screenshot(png_file_path)
    driver.quit()
