from .etl import *
from .calcs import *
import sys


def main_menu():
    while True:
        print("Select an option:")
        print("0. Execute all exercises")
        print("1. Exercise 1: Read and clean data")
        print("2. Exercise 2: Data processing")
        print("3. Exercise 3: Data grouping")
        print("4. Exercise 4: Time Analysis")
        print("5. Exercise 5: State analysis")
        print("6. Exercise 6: Choropleth maps")
        print("7. Exit program")

        choice = input("Enter choice: ")

        print("---------------------------------------------------------------")

        if choice == '0':
            execute_all()
        elif choice == '1':
            exercise_1()
        elif choice == '2':
            exercise_2()
        elif choice == '3':
            exercise_3()
        elif choice == '4':
            exercise_4()
        elif choice == '5':
            exercise_5()
        elif choice == '6':
            exercise_6()
        elif choice == '7':
            print("Exiting program...")
            sys.exit()
        else:
            print("Invalid choice...")

        print("---------------------------------------------------------------")


def exercise_1():
    print("Exercise 1: Read and clean data...")
    df = read_csv("./data/nics-firearm-background-checks.csv")
    df = clean_csv(df)
    df = rename_col(df)
    print("Exercise 1 completed.")
    return df


def exercise_2():
    print("Exercise 2: Data processing...")
    df = read_csv("./data/nics-firearm-background-checks.csv")
    df = clean_csv(df)
    df = rename_col(df)
    df = breakdown_date(df)
    df = erase_month(df)
    print("Exercise 2 completed.")
    return df


def exercise_3():
    print("Exercise 3: Data grouping...")
    df = read_csv("./data/nics-firearm-background-checks.csv")
    df = clean_csv(df)
    df = rename_col(df)
    df = breakdown_date(df)
    df = erase_month(df)
    grouped_df = groupby_state_and_year(df)
    _, _, _ = print_biggest_handguns(grouped_df)
    _, _, _ = print_biggest_longguns(grouped_df)
    print("Exercise 3 completed.")
    return grouped_df


def exercise_4():
    print("Exercise 4: Time analysis...")
    df = read_csv("./data/nics-firearm-background-checks.csv")
    df = clean_csv(df)
    df = rename_col(df)
    df = breakdown_date(df)
    df = erase_month(df)
    grouped_df = groupby_state_and_year(df)
    time_evolution(grouped_df)
    print("Exercise 4 completed.")


def exercise_5():
    print("Exercise 5: State analysis...")
    df = read_csv("./data/nics-firearm-background-checks.csv")
    df = clean_csv(df)
    df = rename_col(df)
    df = breakdown_date(df)
    df = erase_month(df)
    grouped_df = groupby_state_and_year(df)
    state_grouped_df = groupby_state(grouped_df)
    cleaned_states_df = clean_states(state_grouped_df)
    pop_df = read_csv("./data/us-state-populations.csv")
    merged_df = merge_datasets(cleaned_states_df, pop_df)
    relative_values_df = calculate_relative_values(merged_df)
    _, _ = analyze_state_data(relative_values_df)
    print("Exercise 5 completed.")
    return relative_values_df


def exercise_6():
    print("Exercise 6: Choropleth maps...")
    df = read_csv("./data/nics-firearm-background-checks.csv")
    df = clean_csv(df)
    df = rename_col(df)
    df = breakdown_date(df)
    df = erase_month(df)
    grouped_df = groupby_state_and_year(df)
    state_grouped_df = groupby_state(grouped_df)
    cleaned_states_df = clean_states(state_grouped_df)
    pop_df = read_csv("./data/us-state-populations.csv")
    merged_df = merge_datasets(cleaned_states_df, pop_df)
    relative_values_df = calculate_relative_values(merged_df)
    geo_json_path = "./data/us-states.json"
    create_choropleth_map(relative_values_df, 'permit_perc', geo_json_path, 'Permit Percentage', 'permit_perc_map')
    create_choropleth_map(relative_values_df, 'handgun_perc', geo_json_path, 'Handgun Percentage', 'handgun_perc_map')
    create_choropleth_map(relative_values_df, 'longgun_perc', geo_json_path, 'Long Gun Percentage', 'longgun_perc_map')
    print("Exercise 6 completed. Generated maps saved under data/maps/.")


def execute_all():
    print("Executing all exercises...")
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    print("All exercises completed. Generated maps saved under data/maps/.")


if __name__ == "__main__":
    main_menu()
