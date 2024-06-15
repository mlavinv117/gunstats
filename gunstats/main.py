from .etl import *
from .calcs import *
import sys


def main_menu():
    print("Select an option:")
    print("1. Read and clean data")
    print("2. Print biggest handguns and longguns")
    print("3. Group by state and clean states")
    print("4. Merge datasets and calculate relative values")
    print("5. Analyze state data")
    print("6. Create choropleth maps")
    print("7. Execute all steps")

    choice = input("Enter choice: ")

    if choice == '1':
        step1()
    elif choice == '2':
        step2()
    elif choice == '3':
        step3()
    elif choice == '4':
        step4()
    elif choice == '5':
        step5()
    elif choice == '6':
        step6()
    elif choice == '7':
        execute_all()
    else:
        print("Invalid choice. Exiting.")
        sys.exit()

def step1():
    print("Reading and cleaning data...")
    df = read_csv("./data/nics-firearm-background-checks.csv")
    df = clean_csv(df)
    df = rename_col(df)
    df = breakdown_date(df)
    df = erase_month(df)
    print("Excersise 1 completed.")
    return df

def step2():
    print("Printing biggest handguns and long guns...")
    df = step1()
    grouped_df = groupby_state_and_year(df)
    print_biggest_handguns(grouped_df)
    print_biggest_longguns(grouped_df)
    print("Excersise 2 completed.")

def step3():
    print("Grouping by and cleaning states...")
    df = step1()
    grouped_df = groupby_state_and_year(df)
    state_grouped_df = groupby_state(grouped_df)
    cleaned_states_df = clean_states(state_grouped_df)
    print("Excersise 3 completed.")
    return cleaned_states_df

def step4():
    print("Merging datasets and calculating relative values...")
    cleaned_states_df = step3()
    pop_df = read_csv("./data/us-state-populations.csv")
    merged_df = merge_datasets(cleaned_states_df, pop_df)
    relative_values_df = calculate_relative_values(merged_df)
    print("Excersise 4 completed.")
    return relative_values_df

def step5():
    print("Analyzing state data...")
    relative_values_df = step4()
    analyze_state_data(relative_values_df)
    print("Excersise 5 completed.")

def step6():
    print("Creating maps...")
    relative_values_df = step4()
    geo_json_url = "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
    create_choropleth_map(relative_values_df, 'permit_perc', geo_json_url, 'Permit Percentage', 'permit_perc_map')
    create_choropleth_map(relative_values_df, 'handgun_perc', geo_json_url, 'Handgun Percentage', 'handgun_perc_map')
    create_choropleth_map(relative_values_df, 'longgun_perc', geo_json_url, 'Long Gun Percentage', 'longgun_perc_map')
    print("Excersise 6 completed."
          "Generated maps saved under data/maps/.")


def execute_all():
    print("Executing all steps...")
    step1()
    step2()
    step3()
    step4()
    step5()
    step6()

if __name__ == "__main__":
    main_menu()
