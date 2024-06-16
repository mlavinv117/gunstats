import unittest
import pandas as pd
from gunstats.etl import read_csv, clean_csv, rename_col, breakdown_date, \
    erase_month, groupby_state_and_year, groupby_state, clean_states, \
    merge_datasets, calculate_relative_values
from gunstats.calcs import print_biggest_handguns, print_biggest_longguns, \
    analyze_state_data


class TestETL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Load the dataset once for all test cases to improve efficiency.
        """
        print("Setup: Loading dataset...")
        cls._df = read_csv("./data/nics-firearm-background-checks.csv")

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
        pop_df = read_csv("./data/us-state-populations.csv")
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
        pop_df = read_csv("./data/us-state-populations.csv")
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
        print("Setup: Loading datase...t")
        cls._df = read_csv("./data/nics-firearm-background-checks.csv")
        cleaned_df = clean_csv(cls._df)
        df_with_dates = breakdown_date(cleaned_df)
        df_without_month = erase_month(df_with_dates)
        cls.grouped_df = groupby_state_and_year(df_without_month)

    def test_print_biggest_handguns(self):
        """
        Test the get_biggest_handguns function to ensure it returns the correct
        state and year.
        """
        state, year, handguns = print_biggest_handguns(self.grouped_df)
        self.assertEqual(state, 'Florida')
        self.assertEqual(year, 2016)
        self.assertEqual(handguns, 662308)

    def test_print_biggest_longguns(self):
        """
        Test the get_biggest_longguns function to ensure it returns the correct
        state and year.
        """
        state, year, longguns = print_biggest_longguns(self.grouped_df)
        self.assertEqual(state, 'Pennsylvania')
        self.assertEqual(year, 2012)
        self.assertEqual(longguns, 873543)

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
        pop_df = read_csv("./data/us-state-populations.csv")
        merged_df = merge_datasets(cleaned_states_df, pop_df)
        relative_values_df = calculate_relative_values(merged_df)

        # Get the analysis results
        old_mean_permit_perc, new_mean_permit_perc = analyze_state_data(relative_values_df)

        # Check the mean permit percentage
        self.assertAlmostEqual(old_mean_permit_perc, 34.878732819341515, places=2)

        # Check the new mean permit percentage
        self.assertAlmostEqual(new_mean_permit_perc, 21.121821287235978, places=2)

        # Ensure the mean changed
        self.assertNotEqual(old_mean_permit_perc, new_mean_permit_perc)


if __name__ == '__main__':
    unittest.main()
