import unittest
import pandas as pd
from gunstats.etl import read_csv, clean_csv, rename_col, breakdown_date, \
    erase_month, groupby_state_and_year, groupby_state, clean_states, \
    merge_datasets, calculate_relative_values
from gunstats.calcs import print_biggest_handguns, print_biggest_longguns, \
    time_evolution, analyze_state_data, create_choropleth_map
import io
import sys


class TestETL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Load the dataset once for all test cases to improve efficiency.
        """
        print("Loading dataset")
        cls._df = read_csv(".../Data/nics-firearm-background-checks.csv")

    def test_read_csv(self):
        """
        Test the read_csv function to ensure it loads a dataframe correctly.
        """
        self.assertIsInstance(self._df, pd.DataFrame)

    def test_clean_csv(self):
        """
        Test the clean_csv function to ensure it retains only the specified
        columns.
        """
        cleaned_df = clean_csv(self._df)
        self.assertEqual(list(cleaned_df.columns),
                         ['month', 'state', 'permit', 'handgun', 'long_gun'])

    def test_rename_col(self):
        """
        Test the rename_col function to ensure it renames the 'longgun' column
        correctly.
        """
        # Adding 'longgun' column for the test
        test_df = self._df.rename(columns={'long_gun': 'longgun'})
        df_with_renamed_col = rename_col(test_df)
        self.assertIn('long_gun', df_with_renamed_col.columns)

    def test_breakdown_date(self):
        """
        Test the breakdown_date function to ensure it splits the 'month' column
        correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        self.assertIn('year', df_with_dates.columns)
        self.assertIn('month', df_with_dates.columns)
        self.assertIsInstance(df_with_dates['year'].iloc[0], int)
        self.assertIsInstance(df_with_dates['month'].iloc[0], int)

    def test_erase_month(self):
        """
        Test the erase_month function to ensure it removes the 'month' column.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        self.assertNotIn('month', df_without_month.columns)

    def test_groupby_state_and_year(self):
        """
        Test the groupby_state_and_year function to ensure it groups the data
        correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_df = groupby_state_and_year(df_without_month)
        self.assertIn('year', grouped_df.columns)
        self.assertIn('state', grouped_df.columns)

    def test_groupby_state(self):
        """
        Test the groupby_state function to ensure it groups the data correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_by_year_df = groupby_state_and_year(df_without_month)
        grouped_df = groupby_state(grouped_by_year_df)
        self.assertIn('state', grouped_df.columns)

    def test_clean_states(self):
        """
        Test the clean_states function to ensure it removes specified states.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_by_year_df = groupby_state_and_year(df_without_month)
        grouped_df = groupby_state(grouped_by_year_df)
        cleaned_states_df = clean_states(grouped_df)
        self.assertNotIn('Guam', cleaned_states_df['state'].values)
        self.assertNotIn('Mariana Islands', cleaned_states_df['state'].values)
        self.assertNotIn('Puerto Rico', cleaned_states_df['state'].values)
        self.assertNotIn('Virgin Islands', cleaned_states_df['state'].values)

    def test_merge_datasets(self):
        """
        Test the merge_datasets function to ensure it merges the data correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_by_year_df = groupby_state_and_year(df_without_month)
        grouped_df = groupby_state(grouped_by_year_df)
        cleaned_states_df = clean_states(grouped_df)
        pop_df = read_csv("path_to_us_state_populations_csv_file")
        merged_df = merge_datasets(cleaned_states_df, pop_df)
        self.assertIn('pop_2014', merged_df.columns)

    def test_calculate_relative_values(self):
        """
        Test the calculate_relative_values function to ensure it calculates
        relative values correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_by_year_df = groupby_state_and_year(df_without_month)
        grouped_df = groupby_state(grouped_by_year_df)
        cleaned_states_df = clean_states(grouped_df)
        pop_df = read_csv("path_to_us_state_populations_csv_file")
        merged_df = merge_datasets(cleaned_states_df, pop_df)
        relative_values_df = calculate_relative_values(merged_df)
        self.assertIn('permit_perc', relative_values_df.columns)
        self.assertIn('handgun_perc', relative_values_df.columns)
        self.assertIn('longgun_perc', relative_values_df.columns)

class TestCalcs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Load the dataset once for all test cases to improve efficiency.
        """
        print("Loading dataset")
        df = read_csv("path_to_your_test_csv_file")
        cleaned_df = clean_csv(df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        cls.grouped_df = groupby_state_and_year(df_without_month)

    def test_print_biggest_handguns(self):
        """
        Test the print_biggest_handguns function to ensure it prints the correct
        state and year.
        """
        # Redirect stdout to capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print_biggest_handguns(self.grouped_df)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertIn("The state with the highest number of handguns is",
                      output)

    def test_print_biggest_longguns(self):
        """
        Test the print_biggest_longguns function to ensure it prints the correct
        state and year.
        """
        # Redirect stdout to capture print output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print_biggest_longguns(self.grouped_df)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertIn("The state with the highest number of long guns is",
                      output)


    def test_time_evolution(self):
        """
        Test the time_evolution function to ensure it creates the plot correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_df = groupby_state_and_year(df_without_month)
        time_evolution(grouped_df)

    def test_analyze_state_data(self):
        """
        Test the analyze_state_data function to ensure it performs analysis
        correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_by_year_df = groupby_state_and_year(df_without_month)
        grouped_df = groupby_state(grouped_by_year_df)
        cleaned_states_df = clean_states(grouped_df)
        pop_df = read_csv("path_to_us_state_populations_csv_file")
        merged_df = merge_datasets(cleaned_states_df, pop_df)
        relative_values_df = calculate_relative_values(merged_df)

        captured_output = io.StringIO()
        sys.stdout = captured_output
        analyze_state_data(relative_values_df)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        self.assertIn("Mean permit_perc", output)
        self.assertIn("Kentucky data", output)
        self.assertIn("New mean permit_perc", output)
        self.assertIn("The mean permit_perc changed from", output)

    def test_create_choropleth_map(self):
        """
        Test the create_choropleth_map function to ensure it creates the map
        correctly.
        """
        cleaned_df = clean_csv(self._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        grouped_by_year_df = groupby_state_and_year(df_without_month)
        grouped_df = groupby_state(grouped_by_year_df)
        cleaned_states_df = clean_states(grouped_df)
        pop_df = read_csv("path_to_us_state_populations_csv_file")
        merged_df = merge_datasets(cleaned_states_df, pop_df)
        relative_values_df = calculate_relative_values(merged_df)
        create_choropleth_map(
            relative_values_df, 'permit_perc', 'path_to_us_states_json_file',
            'Permit Percentage', 'permit_perc_map')
        create_choropleth_map(
            relative_values_df, 'handgun_perc', 'path_to_us_states_json_file',
            'Handgun Percentage', 'handgun_perc_map')
        create_choropleth_map(
            relative_values_df, 'longgun_perc', 'path_to_us_states_json_file',
            'Long Gun Percentage', 'longgun_perc_map')


if __name__ == '__main__':
    unittest.main()
