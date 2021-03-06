import time
import pandas as pd
import numpy as np
import helper
from datetime import datetime
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(' Hello! Let\'s explore some US bikeshare data!')

    
    month = day = 'all'
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = helper.get_user_city()

    # get user input for filetr type input
    filter_val = helper.get_user_filter()

    # get user input for month (all, january, february, ... , june)
    if filter_val == 'both' or filter_val == 'month':
        month = helper.get_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_val == 'both' or filter_val == 'day':
        day = helper.get_day()

    display_raw_data = helper.display_raw_data_request()

    print('-'*40)

    return city, month, day, display_raw_data


def load_data(city, month, day, display_raw_data):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city.replace(' ', '_') + ".csv")

    df['Start Time'], df['End Time'] = pd.to_datetime(
        df['Start Time']), pd.to_datetime(df['End Time'])
    df['start_time_month'], df['end_time_month'] = df['Start Time'].dt.month, df['End Time'].dt.month
    df['start_time_weekday'], df['end_time_weekday'] = df['Start Time'].dt.weekday, df['End Time'].dt.weekday
    df['start_time_hour'], df['end_time_hour'] = df['Start Time'].dt.hour, df['End Time'].dt.hour

    if month != 'all':
        df = df[(df['start_time_month'] == month)
                & (df['end_time_month'] == month)]

    if day != 'all':
        df = df[(df['start_time_weekday'] == day)
                & (df['end_time_weekday'] == day)]

    if display_raw_data == 'yes':
        print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    """
    Determining if 'start_time_month' column exist or not in df
    """
    is_exist = is_column_exist(df, 'start_time_month')

    if is_exist:
        common_month_grp = df.groupby('start_time_month')
        # Getting groupby dataframe keys
        sub_sets_len = len(common_month_grp.groups.keys())

        """
        If one or more key do exist in groupby dataframe, we would
        try to get key has maximum groupped elements.
        """
        if sub_sets_len > 0:
            common_month_max_value = common_month_grp.agg(
                {'start_time_weekday': 'count'}).idxmax()['start_time_weekday']
            print(' most common month : ',
                  helper.MONTH_DATA[common_month_max_value]['full_name'])
        else:
            no_data_found()

    else:
        no_column_error_msg('start_time_month')

    # display the most common day of week
    is_exist = is_column_exist(df, 'start_time_weekday')

    if is_exist:
        common_week_grp = df.groupby('start_time_weekday')
        sub_sets_len = len(common_week_grp.groups.keys())

        if sub_sets_len > 0:
            common_week_max_value = common_week_grp.agg(
                {'start_time_weekday': 'count'}).idxmax()['start_time_weekday']
            print(' most common weekday : ',
                  helper.DAY_DATA[common_week_max_value])
        else:
            no_data_found()

    else:
        no_column_error_msg('start_time_weekday')

    # display the most common start hour
    is_exist = is_column_exist(df, 'start_time_hour')

    if is_exist:
        common_hour_grp = df.groupby('start_time_hour')
        sub_sets_len = len(common_hour_grp.groups.keys())

        if sub_sets_len > 0:
            common_hour_max_value = common_hour_grp.agg(
                {'start_time_weekday': 'count'}).idxmax()['start_time_weekday']
            print(' most common start hour : ', common_hour_max_value)
        else:
            no_data_found()

    else:
        no_column_error_msg('start_time_hour')

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    is_exist_i = is_column_exist(df, 'Start Station')

    if is_exist_i:
        common_start_station_grp = df.groupby('Start Station')
        sub_sets_len = len(common_start_station_grp.groups.keys())

        if sub_sets_len > 0:
            common_start_station_val = common_start_station_grp.agg(
                {'Start Station': 'count'}).idxmax()['Start Station']
            print(' Most commonly used start station : ',
                  common_start_station_val)
        else:
            no_data_found()

    else:
        no_column_error_msg('Start Station')

        # display most commonly used end station

    is_exist_ii = is_column_exist(df, 'End Station')

    if is_exist_ii:
        common_end_station_grp = df.groupby('End Station')
        sub_sets_len = len(common_end_station_grp.groups.keys())

        if sub_sets_len > 0:
            common_end_station_val = common_end_station_grp.agg(
                {'End Station': 'count'}).idxmax()['End Station']
            print(' Most commonly used end station : ', common_end_station_val)
        else:
            no_data_found()

    else:
        no_column_error_msg('End Station')

        # display most frequent combination of start station and end station trip
    if is_exist_i and is_exist_ii:
        common_start_end_trip_grp = df.groupby(
            ['Start Station', 'End Station'])
        sub_sets_len = len(common_start_end_trip_grp.groups.keys())

        if sub_sets_len > 0:
            common_start_end_trip_val = common_start_end_trip_grp.agg(
                {'Start Station': 'count'}).idxmax()['Start Station']
            print(' Most frequent combination of start station and end station : ',
                  common_start_end_trip_val)
        else:
            no_data_found()

    else:
        no_column_error_msg('Start Station, End Station')

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n Calculating Trip Duration...\n')
    start_time = time.time()

    is_exist = is_column_exist(df, 'Trip Duration')

    if is_exist:
        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print(' total travel time : ', total_travel_time)

        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print(' Mean travel time : ', mean_travel_time)
    else:
        no_column_error_msg('Trip Duration')

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    is_exist = is_column_exist(df, 'User Type')

    if is_exist:
        user_types_grp = df.groupby('User Type')
        sub_sets_len = len(user_types_grp.groups.keys())

        if sub_sets_len > 0:
            user_types_grp_agg = user_types_grp.agg(
                {'start_time_month': 'count'})
            user_types_grp_keys = user_types_grp.groups.keys()

            for user_type in user_types_grp_keys:
                print(' User Type: ', user_type, ', Count: ',
                      user_types_grp_agg.loc[user_type]['start_time_month'])
        else:
            no_data_found()
    else:
        no_column_error_msg('User Type')

    print('-'*40, '\n')

    # Display counts of gender
    is_exist = is_column_exist(df, 'Gender')

    if is_exist:
        user_gender_grp = df.groupby('Gender')
        sub_sets_len = len(user_gender_grp.groups.keys())

        if sub_sets_len > 0:
            user_gender_grp_agg = user_gender_grp.agg(
                {'start_time_month': 'count'})
            user_gender_grp_keys = user_gender_grp.groups.keys()

            for user_gender in user_gender_grp_keys:
                print(' Gender: ', user_gender, ', Count: ',
                      user_gender_grp_agg.loc[user_gender]['start_time_month'])
        else:
            no_data_found()
    else:
        no_column_error_msg('Gender')

    print('-'*40, '\n')

    # Display earliest, most recent, and most common year of birth

    is_exist = is_column_exist(df, 'Birth Year')

    if is_exist:
        user_birth_year_grp = df.groupby('Birth Year')
        sub_sets_len = len(user_birth_year_grp.groups.keys())

        if sub_sets_len > 0:
            user_birth_year_max_value = user_birth_year_grp.agg(
                {'start_time_month': 'count'}).idxmax()['start_time_month']
            print(' earliest year of birth : ',
                  df['Birth Year'].nsmallest(n=1).iloc[0])
            print(' most recent year of birth : ',
                  df['Birth Year'].nlargest(n=1).iloc[0])
            print(' most common year of birth : ', user_birth_year_max_value)
        else:
            no_data_found()

    else:
        no_column_error_msg('Birth Year')

    print("\n This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def is_column_exist(df, coulmn):
    is_exist = False

    if coulmn in df.columns:
        is_exist = True

    return is_exist


def no_column_error_msg(column_name):
    print(' ', column_name, 'coulmn does not exist.')


def no_data_found():
    print(' No data found')


def main():
    while True:

        city, month, day, display_raw_data = get_filters()
        df = load_data(city, month, day, display_raw_data)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
