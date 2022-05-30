import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).

    city = -1
    cities = ['chicago','new york city','washington']
    while city<1 or city>3:
        try:
            city = input("First let's choose a city to explore."
                        " Please enter the equivelent city number.\n"
                        "\n[1->Chicago,2->New york city,3->Washington]\n")
            city = cities[int(city)-1]
            break
        except:
            print("\n Wrong Input.\n")
            city = -1

    # get user input for month (all, january, february, ... , june)
    month = -1
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    while month<0 or month>6:
        try:
            month = input("\nThen let's choose a month to explore. "
                        "Please enter the equivelent month number,1->6,"
                        " or 0 for the whole half.\n")
            month = months[int(month)]
            break
        except:
            print("\n Wrong Input.\n")
            month = -1

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=-1
    days = ['all','monday','tuesday','wednesday','thursday','friday',
            'saturday','sunday']
    while day<0 or day>12:
        try:
            day = input("\nFinally let's choose a day to explore. "
                        " Please enter the equivelent day number,1->7,\n"
                        "with monday=1 & sunday=7 or 0 for the whole week.\n")
            day = days[int(day)]
            break
        except:
            print("\n Wrong Input.\n")
            day = -1

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df=df[df['day_of_week']==day.title()]

    return df



def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel.

        args:
            (Dataframe) df - the dataframe object containing the data.
            (str) month - name of the month choosen or 'all' for the whole year.
            (str) day - name of the day_of_week choosen or 'all' for the whole week.
        returns:
            None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    m = d = h = -1

    # display the most common month
    if month !='all':
        #check if the df has a specific month data
        m=month.title()
    else:
        m = months[df['month'].mode()[0]-1]
    # display the most common day of week
    if day != 'all':
        #check if the df has a specific day data
        d = day.title()
    else:
        d = df['day_of_week'].mode()[0]
    # display the most common start hour

    h = df['hour'].mode()[0]
    print("The most common month is {}.\n"
        "The most common day is {}.\n"
        "The most common hour is {}.\n".format(m,d,h))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    #print(df['hour'].mode())

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    combinations = (df['Start Station']+", "+df['End Station']).mode()[0]

    print("The most Popular start_station is {}.\n"
        "The most Popular end_station is {}.\n"
        "The most Popular start_station, end_station combination is {}.\n"
        .format(start_station, end_station, combinations))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_delta_to_stats(t):
    """Helper function that extracts the days, hours, minutes and seconds in a
        timedelta datatype object.
        ex:
            300 days 23h:50m:30s to 300days, 23 hours, 50 minutes, 30 seconds.
        args:
            (timedelta) t - the timedelta object.
        return:
            (int) days - the number of days in that time delta.
            (int) hours - the number of hours that remain after extracting the days.
            (int) minutes - the number of minutes that don't make it to full hour.
            (int) seconds - the number of seconds that don't make a full minute.
    """
    days = t.days
    hours, rem = divmod(t.seconds,3600)
    minutes, seconds= divmod(rem,60)
    return days,hours,minutes,seconds

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    start = df['Start Time']
    end = pd.to_datetime(df['End Time'])
    # the difference is a timedelta object that will be formed with the
    # helper function time_delta_to_stats().
    difference = end - start

    # display total travel time
    total_travel_time = difference.sum()

    t_days,t_hours,t_minutes,t_seconds = time_delta_to_stats(total_travel_time)

    # display mean travel time
    mean_travel_time = difference.mean()
    a_days,a_hours,a_minutes,a_seconds = time_delta_to_stats(mean_travel_time)

    print("The total travel time in that duration is {} days, {} hours,"
        " {} minutes and {} seconds.\n".format(t_days, t_hours, t_minutes, t_seconds))

    print("The average travel time is {} days, {} hours,"
        " {} minutes and {} seconds.\n".format(a_days, a_hours, a_minutes, a_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # the code would produce a key Error if any of variable data doesn't exist
    # in the choosen day/week combination like a day/week with no subscribers
    # only customers/ so a punch of try/except blocks were used to prevent that.
    counts = df['User Type'].value_counts()
    try:
        subscribers = counts['Subscriber']
    except:
        subscribers = 0
    try:
        customers = counts['Customer']
    except:
        customers = 0
    try:
        dependents = counts['Dependent']
    except:
        dependents = 0

    print("The Users Distripution is : {} subscriber/s, {} customer/s and"
            " {} dependent/s.\n".format(subscribers, customers, dependents))

    # this block is separated to prevent the keyerror that shows in case the
    # user choose Washington city.
    try:
        # Display counts of gender
        counts = df['Gender'].value_counts()
        try:
            males = counts['Male']
        except:
            males = 0
        try:
            females = counts['Female']
        except:
            females = 0
        # Display earliest, most recent, and most common year of birth
        yob = df['Birth Year']
        earliest = yob.min()
        most_recent = yob.max()
        most_common = yob.mode()[0]

        print("The Gender Distripution is : {} Female/s, {} Male/s.\n".format(females,males))

        print("The earliest YOB is : {}"
            " The most recent YOB is : {}\n"
            "and the most common YOB is : {}.\n".format(earliest,most_recent,most_common))
    except KeyError:
        pass
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df,current_record=0):
    """A prompt to display the raw data in the dataframe if the user wants.
        It terminates in case the user answer was 'No' or the dataframe ended.

        args:
            (dataframe) df - the frame that holds the data.
            (int) current_record - a holder for the record number that was last shown
                                   to keep track in the recursive calls.
        note:
            tabulate module was used to fix a display issue where the columns
             would truncate to ... .
    """
    ans = -1
    count = df['Start Time'].count()
    while ans not in ['yes', 'no'] and current_record != count:
        try:
            ans = input("\nwould u like to see some raw data. yes/no \n").lower()
        except:
            continue
    if ans == 'yes':
        if current_record>=count:
            print("No more records to show\n")
            return None
        else:
            raw_num = -1
            while raw_num<1 or raw_num>count or raw_num+current_record>count:
                try:
                    raw_num = int(input("how many rows would u like to see.\n"
                                   "please enter a number between {} & {}."
                                   .format(1,count-current_record)))
                except:
                    raw_num = -1
                    continue

            #using the tabulate module fixis the columns truncation to ,...,
            print(tabulate(df[:][current_record:current_record+raw_num], headers ="keys"))
            print('-'*40)
            print('\n')
            return raw_data(df, current_record+raw_num)
    else:
        return None
"""
def raw_data(df):
    '''Another version of raw_data that displays only 5 raws at a time.'''
    i=0
    while True:
        try:
            display_data = input("\nWould you like to see 5 lines of raw data?"
                                "Enter yes or no.\n").lower()
        except:
            continue
        if display_data != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,5+i)], headers ="keys"))
"""

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
