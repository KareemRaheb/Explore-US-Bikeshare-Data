import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# global variables that will be used alternatively in different functions
df = ''
city = ''
month = ''
day = ''
correct_month = ["january", "february", "march", "april", "may", "june", "all"]
correct_day = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global city 
    correct_city = ['chicago','new york city','washington']
    while True:
        city =  input("Please Choose City: Chicago - New York City - Washington ").lower() # lower method is used to prevenet errors if user used capital letters
        if city in correct_city:
            break
        else:
            print("INVALID INPUT - PLEASE ENTER FROM:", correct_city)

    # get user input for month (all, january, february, ... , june)
    global month, correct_month
    while True:
        month = input("Do you want to filter by month? - Enter month name from january to june if yes, enter 'all' for no filter ").lower()
        if month in correct_month:
            break
        else:
            print("INVALID INPUT - PLEASE ENTER FROM:", correct_month)


    # get user input for day of week (all, monday, tuesday, ... sunday)
    global day, correct_day
    while True:
        day =  input("Do you want to filter by day? - Enter day name if yes, Enter 'all' for no filter ").lower()
        if day in correct_day:
            break
        else:
            print("INVALID INPUT PLEASE ENTER FROM:", correct_day) 


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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    global df 
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday + 1 
    # +1 to unite the values of the three columns not starting with zeros, because why not?
    df['hour'] = df['Start Time'].dt.hour

    # make a seperated index to call the filter, keeping the code oragnized and specified 
    day_index = correct_day.index(day) + 1
    month_index = correct_month.index(month) + 1
    
    # month and day filters if applicable together 
    if month != 'all' and day != 'all':
         df = df.loc[(df['month'] == month_index) & (df['day_of_week'] == day_index)]    
    
    # month filter if applicable alone
    elif month != 'all':
         df = df.loc[df['month'] == month_index]

    # day filter if applicable alone
    elif day != 'all':
         df = df.loc[df['day_of_week'] == day_index]
    

    # display function
    return df

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0] # variable with the first mode of month column in the last modified df 

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0] # variable with the first mode of day_of_week column in the last modified df


    # display the most common start hour
    common_hour = df['hour'].mode()[0] # variable with the first mode of hour column in the last modified df

    # display the three modes
    print("The most common month is:", common_month)
    print("The most common day is:", common_day)
    print("the most common start hour is:", common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_station = df['Start Station'].mode()[0] # variable with the first mode of start station column in the last modified df


    # display most commonly used end station
    common_destination = df['End Station'].mode()[0] # variable with the first mode of end station column in the last modified df

    # display most frequent combination of start station and end station trip
    start_end_columns = df.groupby(['Start Station','End Station']) # variable that groups start station and end station colums with groupby method
    most_used_combination = start_end_columns.size().sort_values(ascending=False).head(1) # shows the value of the most two used stations together, by sorting the values descendingly

    # display the three variables
    print("The most common start station is:", common_station)
    print("The most common end station is:", common_destination)
    print("the most used combination (Trip) is:", most_used_combination)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum() # sums all records in the trip duration column


    # display mean travel time
    average_time = df['Trip Duration'].mean() # gets the average of the trip duration column

    # display the two variables
    print("The total travel time is:", total_time)
    print("The average travel time is:", average_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()    

    # Display counts of user types
    user_types_count = df['User Type'].value_counts() # count method returns the number of non-empty values in the column

    # only chicago and new york cities has gender and birth year columns
    # Display counts of gender if existed
    if 'Gender' in df:
        count_gender = df['Gender'].value_counts()
        print("The Gender count is:", count_gender)

    else:
        print("Gender stats cannot be calculated because Gender does not appear in the dataframe")
        
    # Display earliest, most recent, and most common year of birth if existed
    if 'Birth Year' in df:
        earliest_birth = df['Birth Year'].min() # min method returns the smallest value in the column
        most_recent_birth = df['Birth Year'].max() # max method returns the largest value in the column
        common_birth = df['Birth Year'].mode()[0] # mode method as already used before to return the first mode in birth year column
        # this is a conditional statement that prints only if the user did not choose chicago city
        print("The earliest year of birth is:", earliest_birth)
        print("The most recent year of birth is:", most_recent_birth)
        print("The most common year of birth is:", common_birth)
    else:
        print("Birth Year stats cannot be calculated because Birth Year does not appear in the dataframa")
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def interactive_display(df): # new function for displaying 5 rows if the user wanted to
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no? ").lower()
    start_loc = 0
    if view_data != 'no':
        while view_data == 'yes': # the while loop will keep working till the user enters no
            print(df.iloc[start_loc:start_loc+5]) # displays 5 records starting from the last displayed data 
            start_loc += 5
            view_display = input("Do you wish to continue? Yes or No: ").lower()
            if view_display == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        interactive_display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()