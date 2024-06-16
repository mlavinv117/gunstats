import pandas as pd


def read_csv(url: str) -> pd.DataFrame:
    """
    Function to read a csv file and return it as a pandas DataFrame, printing
    the first 5 rows for validation.
    Args:
     -url (str): The path to the file.
    Returns:
     -df (pd.DataFrame): The csv file converted to a DataFrame.
    """

    # Use pandas to read the csv file and load into a df
    df = pd.read_csv(url)

    # Print first 5 rows
    print("Exercise 1 - First 5 rows from read_csv:")
    print(df.head())

    return df


def clean_csv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to clean the dataframe by retaining only specific columns.
    Args:
     -df (pd.DataFrame): The uncleaned dataframe.
    Returns:
     -df (pd.DataFrame): The cleaned dataframe containing only the relevant
       columns.
    """

    # Keep only the required columns
    columns_to_keep = ['month', 'state', 'permit', 'handgun', 'long_gun']
    df = df[columns_to_keep]

    # Print the column names for verification
    print("Exercise 1 - Columns after clean_csv:")
    print(df.columns)

    return df


def rename_col(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to rename the column 'longgun' to 'long_gun'.
    Args:
     -df (pd.DataFrame): The dataframe with columns to rename.
    Returns:
     -df (pd.DataFrame): The dataframe with the renamed columns.
    """

    # Rename the column
    if 'longgun' in df.columns:
        df = df.rename(columns={'longgun': 'long_gun'})

    # Print the column names to verify
    print("Exercise 1 - Columns after rename_col:")
    print(df.columns)

    return df


def breakdown_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to split the 'month' column into 'year' and 'month' columns.
    Args:
     -df (pd.DataFrame): The dataframe containing the 'month' column.
    Returns:
     -df (pd.DataFrame): The dataframe with 'year' and 'month' columns.
    """

    # Split the 'month' column into 'year' and 'month'
    year_month = df['month'].str.split('-', expand=True)
    df = df.assign(year=year_month[0].astype(int), month=year_month[1].astype(int))

    # Debugging: Verify the types
    print(f"Year dtype: {df['year'].dtype}")
    print(f"Month dtype: {df['month'].dtype}")

    # Print the first 5 rows to verify
    print("Exercise 2 - First 5 rows after breakdown_date:")
    print(df.head())

    return df


def erase_month(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to remove the 'month' column from the dataframe.
    Args:
     -df (pd.DataFrame): The dataframe containing the 'month' column.
    Returns:
     -df (pd.DataFrame): The dataframe without the 'month' column.
    """

    # Drop the 'month' column
    df = df.drop(columns=['month'])

    # Print the first 5 rows and column names to verify
    print("Exercise 2 - First 5 rows and columns after erase_month:")
    print(df.head())
    print(df.columns)

    return df


def groupby_state_and_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate total accumulated values by grouping data by year
    and state.
    Args:
     -df (pd.DataFrame): The dataframe obtained from the previous exercises.
    Returns:
     -df (pd.DataFrame): The dataframe with data grouped by year and state.
    """

    # Group by 'year' and 'state' and sum the values
    grouped_df = df.groupby(['year', 'state']).sum().reset_index()

    return grouped_df


def groupby_state(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate total accumulated values by grouping data by state.
    Args:
     -df (pd.DataFrame): The dataframe with data grouped by year and state.
    Returns:
     -df (pd.DataFrame): The dataframe with data grouped by state.
    """

    grouped_df = df.groupby('state').sum().reset_index()

    # Print the first 5 rows to verify
    print("Exercise 5 - First 5 rows after groupby_state:")
    print(grouped_df.head())

    return grouped_df

def clean_states(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to remove specific states from the dataframe.
    Args:
     -df (pd.DataFrame): The dataframe with data grouped by state.
    Returns:
     -df (pd.DataFrame): The dataframe without the specified states.
    """

    states_to_remove = ['Guam', 'Mariana Islands', 'Puerto Rico', 'Virgin Islands']
    cleaned_df = df[~df['state'].isin(states_to_remove)]

    # Print the number of unique states
    print("Exercise 5 - Number of unique states:")
    print(cleaned_df['state'].nunique())

    return cleaned_df


def merge_datasets(df: pd.DataFrame, pop_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to merge the firearm data with the population data.
    Args:
     -df (pd.DataFrame): The dataframe with firearm data grouped by state.
     -pop_df (pd.DataFrame): The dataframe with population data.
    Returns:
     -df (pd.DataFrame): The merged dataframe.
    """

    merged_df = pd.merge(df, pop_df, how='inner', on='state')

    # Print the first 5 rows to verify
    print("Exercise 5 - First 5 rows after merge_datasets:")
    print(merged_df.head())

    return merged_df


def calculate_relative_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate relative values for permits, handguns, and long guns.
    Args:
     -df (pd.DataFrame): The merged dataframe with population data.
    Returns:
     -df (pd.DataFrame): The dataframe with relative values calculated.
    """

    df['permit_perc'] = (df['permit'] * 100) / df['pop_2014']
    df['handgun_perc'] = (df['handgun'] * 100) / df['pop_2014']
    df['longgun_perc'] = (df['long_gun'] * 100) / df['pop_2014']

    return df
