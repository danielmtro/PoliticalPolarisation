import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('percentage_positive_negative_with_percentages.csv')

# Filter out specific dates
dates_to_exclude = ['march_8', 'march_21', 'april_16']
df = df[~df['Date'].isin(dates_to_exclude)]

# Group the data by 'Outlet' and 'Figure' to calculate the statistics
grouped_df = df.groupby(['Outlet', 'Figure'])

# Calculate weighted averages and standard deviations for Percentage Positive
weighted_avg_pos = grouped_df.apply(lambda x: ((x['Positive'] / x['Totals']) * 100).mean())
std_dev_pos = grouped_df.apply(lambda x: ((x['Positive'] / x['Totals']) * 100).std())
weighted_avg_pos = weighted_avg_pos.reset_index()
std_dev_pos = std_dev_pos.reset_index()

# Rename columns appropriately
weighted_avg_pos.rename(columns={0: 'Weighted Avg Positive'}, inplace=True)
std_dev_pos.rename(columns={0: 'Std Dev Positive'}, inplace=True)

# Merge weighted averages and standard deviations for positive sentiments
result_pos = pd.merge(weighted_avg_pos, std_dev_pos, on=['Outlet', 'Figure'])

# Calculate weighted averages and standard deviations for Percentage Negative
weighted_avg_neg = grouped_df.apply(lambda x: ((x['Negative'] / x['Totals']) * 100).mean())
std_dev_neg = grouped_df.apply(lambda x: ((x['Negative'] / x['Totals']) * 100).std())
weighted_avg_neg = weighted_avg_neg.reset_index()
std_dev_neg = std_dev_neg.reset_index()

# Rename columns appropriately
weighted_avg_neg.rename(columns={0: 'Weighted Avg Negative'}, inplace=True)
std_dev_neg.rename(columns={0: 'Std Dev Negative'}, inplace=True)

# Merge weighted averages and standard deviations for negative sentiments
result_neg = pd.merge(weighted_avg_neg, std_dev_neg, on=['Outlet', 'Figure'])


pd.set_option('display.max_columns', None)  # Display any number of columns
pd.set_option('display.width', None)        # Use the maximum width of the terminal

# Print the results
print("Results with Weighted Averages and Standard Deviations for Percentage Positive:")
print(result_pos)
print("\nResults with Weighted Averages and Standard Deviations for Percentage Negative:")
print(result_neg)
