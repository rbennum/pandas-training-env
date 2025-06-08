import pandas as pd
from utils import load_data

def problem_1():
    '''
    Group data by Gender column, then calculate average CLV for each gender category. If Average CLV value is null, fill with 0.

    Next, categorize Average CLV into 3 categories:
    - "Low": if average is less than or equal to 5,000
    - "Medium": if between 5,000 and 10,000
    - "High": if greater than or equal to 10,000

    Display final result with columns:
    - Gender  
    - Average CLV (two decimal places)
    - CLV Category

    Data Path:
    Customer Loyalty History.csv
    '''
    df = load_data('customer-loyalty.csv')
    CLV_BINS = [float('-inf'), 5000, 10000, float('inf')]
    CLV_LABELS = ['Low', 'Medium', 'High']
    result = (
        df.groupby('Gender', as_index=False)
            .agg(Average_CLV=('CLV', 'mean'))
            .assign(
                Average_CLV=lambda x: x['Average_CLV'].fillna(0).round(2),
                CLV_Category=lambda x: pd.cut(
                    x['Average_CLV'],
                    bins=CLV_BINS,
                    labels=CLV_LABELS,
                    include_lowest=True
                )
            )
    )
    result.rename(columns={
        'Average_CLV': 'Average CLV', 
        'CLV_Category': 'CLV Category'
    }, inplace=True)
    return result

def problem_2():
    '''
    Filter customers from Customer Loyalty History.csv who enrolled between 2013-2015 (inclusive).
    Group by Enrollment Year and Marital Status, then count number of customers in each group.

    Create pivot table with:
    - Rows: Enrollment Year
    - Columns: Marital Status
    - Values: Customer count

    Fill any missing values with 0. Display the complete pivot table.

    Data Path:
    Customer Loyalty History.csv
    '''
    df = load_data('customer-loyalty.csv')
    df_sample = (
        df[df['Enrollment Year'].between(2013, 2015, inclusive='both')]
    )
    result = (
        df_sample
            .pivot_table(
                index='Enrollment Year',
                columns='Marital Status',
                values='Loyalty Number',
                aggfunc='count',
                fill_value=0
            )
    )
    return result

def problem_3():
    '''
    Calculate total Points Accumulated and Points Redeemed per Year and Month from Customer Flight Activity 2017.csv.
    Create new column Points_Balance as (Points Accumulated - Points Redeemed).

    Filter only months where total Points_Balance > 10000. Sort by Year and Month ascending.

    Display final result with columns:
    - Year
    - Month
    - Total Points Accumulated
    - Total Points Redeemed
    - Points_Balance

    Data Path:
    Customer Flight Activity 2017.csv
    '''
    df = load_data('customer-flight-activity.csv')
    df = df[df['Year'] == 2017]

    # Only uncomment if you want to see the proof
    # df = df.sample(n=20, random_state=444).sort_values(by=['Year', 'Month'])
    df_agg = (
        df.groupby(['Year', 'Month'], as_index=False)
            .agg({'Points Accumulated': 'sum', 'Points Redeemed': 'sum'})
    )
    df_agg['Points_Balance'] = df_agg['Points Accumulated'] - df_agg['Points Redeemed']
    df_agg = df_agg[df_agg['Points_Balance'] > 10000]
    df_agg = df_agg.sort_values(['Year', 'Month'], ascending=[True, True])
    return df_agg

def problem_4():
    '''
    Identify customers from Customer Loyalty History.csv with CLV above median value. 
    For these high-value customers, categorize by City and calculate percentage distribution of Education levels within each city.

    Only include cities with at least 5 customers. Round percentages to one decimal place.

    Display final result with columns:
    - City
    - Bachelor (%)
    - College (%)
    - High School (%)
    - Doctor (%)
    - Total_Customers

    Sort by Total_Customers descending.

    Data Path:
    Customer Loyalty History.csv
    '''
    df = load_data('customer-loyalty.csv')
    clv_median = df['CLV'].median()
    df = df[df['CLV'] > clv_median]
    df_agg = (
        df.groupby(['City', 'Education'], as_index=False)
            .agg(Total_Customers=('Loyalty Number', 'count'))
    )
    df_pivot = (
        df_agg.pivot(index='City',
                     columns='Education',
                     values='Total_Customers')
            .rename_axis(None, axis=1)
            .reset_index()
    )
    edu_cols = ['Bachelor', 'College', 'Doctor', 'High School or Below', 'Master']
    df_pivot[edu_cols] = df_pivot[edu_cols].fillna(0)
    df_pivot['Total_Customers'] = df_pivot[edu_cols].sum(axis=1)
    df_pivot[edu_cols] = (
        df_pivot[edu_cols]
            .div(df_pivot['Total_Customers'], axis=0)
            .mul(100)
            .round(1)
    )
    df_pivot = df_pivot.sort_values(by='Total_Customers', ascending=False)
    return df_pivot

def problem_5():
    '''
    Merge Customer Flight Activity 2017.csv with Customer Loyalty History.csv on Loyalty Number. 
    Filter rows where Year=2017 and Total Flights>0.

    Group by Province and compute:
    - Customers: count of unique Loyalty Number
    - Avg_Total_Flights: mean of Total Flights
    - Avg_Distance: mean of Distance

    Round averages to two decimals. Sort by Avg_Distance descending and display top 5 provinces with columns:
    Province, Customers, Avg_Total_Flights, Avg_Distance

    Data Paths:
    Customer Flight Activity 2017.csv
    Customer Loyalty History.csv
    '''
    df1 = load_data('customer-flight-activity.csv')
    df2 = load_data('customer-loyalty.csv')
    df = pd.merge(df1, df2, on='Loyalty Number', how='left')
    df = df[(df['Year'] == 2017) & (df['Total Flights'] > 0)]
    df = df.sample(n=10, random_state=42)
    print(df[['Loyalty Number', 'Province', 'Total Flights', 'Distance']])
    df_agg = (
        df.groupby('Province', as_index=False)
            .agg(
                Customers=('Loyalty Number', 'nunique'),
                Avg_Total_Flights=('Total Flights', 'mean'),
                Avg_Distance=('Distance', 'mean')
            )
            .round(2)
            .sort_values('Avg_Distance', ascending=False)
            .reset_index(drop=True)
            .head(5)
    )
    return df_agg

solutions_dict = {
    1: (problem_1.__doc__, problem_1),
    2: (problem_2.__doc__, problem_2),
    3: (problem_3.__doc__, problem_3),
    4: (problem_4.__doc__, problem_4),
    5: (problem_5.__doc__, problem_5),
}