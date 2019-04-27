import sys
import time
import datetime
import pandas as pd

# city datafile names
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# city DataFrames, dynamically built and indexed similar to CITY_DATA
CITY_DFS = {}

# months and days
months = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december', 'all']

days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def user_input():
    """ Get user input in a controlled manner.  cntl-D or 'quit' will exit from here. """
    ans = ''
    try:
        ans = input().lower()
    except EOFError:
        sys.exit()
    except:
        print("please try again ...")
        ans = ''
    else:
        if ans == 'quit':
            sys.exit()
    return ans        


def get_filters():
    """
    Get city, month, and day filters from the user.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # user to choose a city
    city = ''
    while city not in CITY_DATA:
        print("Enter city (one of: {}), or cntl-D or 'quit':".format(list(CITY_DATA.keys())))
        city = user_input()
            
    # user to choose a month (january, february, etc. or 'all')
    month = ''
    while month not in months:
        print("Enter month (one of: {}), or cntl-D or 'quit':".format(months))
        month = user_input()

    # user to choose day of week (sunday, monday, tuesday, etc. or 'all')
    day = ''
    while day not in days_of_week:
        print("Enter day of week (one of: {}), or cntl-D or 'quit':".format(days_of_week))
        day = user_input()

    print('-'*40)
    return city, month, day


def load_data_files():
    """
    Load the data files into memory and prepare the DataFrames.  
    Do it just once to minimize filesystem interaction and data prep.
    Populate a dict with the cities' enhanced DataFrames, indexed by city name.

    """
    print("Loading city data files ...")
    for key, value in zip(CITY_DATA.keys(), CITY_DATA.values()):
        print("{0}: \"{1}\" ... ".format(key,value), end='', flush=True)
        start_time = time.time()
        df = pd.read_csv(value)
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        # create new columns from individual time values from Start Time
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['Start Hour'] = df['Start Time'].dt.hour
        CITY_DFS[key] = df
        print("%s seconds." % (time.time() - start_time))


def get_data(city, month, day):
    """
    Load data for the specified city, and filter by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # get the city's DataFrame
    df = CITY_DFS.get(city)
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # NOTE: the 'months' list is 0-based.
        month_index = months.index(month) + 1
        df = df[df['month'] == month_index]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # NOTE: the month in the df 'month' column is 1-based; the 'months' list is 0-based.
    print("Most common month: {}".format(months[df['month'].mode()[0]-1].title()))

    # display the most common day of week
    print("Most common day of week: {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print("Most common start hour: {}".format(df['Start Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: {}".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("Most commonly used end station: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    # NOTE: I think this requires combining or concatenating the two columns to produce something on which .mode() can be invoked.
    # I could not figure this out.

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: {}".format(datetime.timedelta(seconds=float(df['Trip Duration'].sum()))))

    # display mean travel time
    print("Average travel time per trip: {}".format(datetime.timedelta(seconds=float(df['Trip Duration'].mean()))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of user types:\n{0}\n".format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df:
        print("Count of genders:\n{0}\n".format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("Birth year:\nearliest={0}\nmost recent={1}\nmost common={2}".format(
            int(df['Birth Year'].min()),
            int(df['Birth Year'].max()),
            int(df['Birth Year'].mode()[0]))
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """
    Conversation with user about showing the raw data, in consecutive chunks of rows
    """
    ans = ''
    while ans == '':
        print("\nWanna see the raw data? 'yes' if yes, or cntl-D or 'quit':")
        ans = user_input()
    if ans != 'yes':
        return

    num_rows = 5
    begin_row = 0
    while True:
        # NOTE: this works only if the df has been gotten with 'all' for month and 'all' for day,
        # becuase the indexes are all off.  I tried to reindex or reset_indexes, but could not get it to work.
        print(df.loc[begin_row : (begin_row+num_rows)-1])
        ans = ''
        while ans == '':
            print("\nNext {} rows? 'yes' if yes, or cntl-D or 'quit':".format(num_rows))
            ans = user_input()
        if ans != 'yes':
            return
        begin_row += num_rows

    print('-'*40)


def again():
    ans = ''
    while ans == '':
        print("\nWould you like to load more data? 'yes' if yes, or cntl-D or 'quit':")
        ans = user_input()
        return ans


def main():
    load_data_files()
    while True:
        city, month, day = get_filters()
        df = get_data(city, month, day)
        df.info()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        if again() != 'yes':
            break


if __name__ == "__main__":
	main()
