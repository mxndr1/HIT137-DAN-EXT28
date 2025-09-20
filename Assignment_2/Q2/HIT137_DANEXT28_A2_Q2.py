'''

Group Name: DAN/EXT 28

Group Members:
FATEEN RAHMAN - s387983
HENDRICK DANG (VAN HOI DANG)- s395598
KEVIN ZHU (JIAWEI ZHU) - s387035
MEHRAAB FERDOUSE - s393148

'''

import os
import pandas as pd



def dataframe_concat():
    """
    Locates the 'temperatures' folder and also concatenates all CSV files in the specified directory into a single dataframe
    """
    
    dataframes = []

    # Finds the absolute path to the 'temperatures' folder no matter where it is located
    base_dir = os.getcwd()
    for root, dirs, files in os.walk(base_dir):
        if 'temperatures' in dirs:
            temperatures_path = os.path.join(root, 'temperatures')
            break

    # Iterates through all CSV files in the 'temperatures' folder and reads them into dataframes
    with os.scandir(temperatures_path) as temperatures:
        for file in temperatures:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file.path)
                dataframes.append(df)

    # Concatenates all dataframes into a single dataframe and returns it and also returns the path to the 'temperatures' folder
    return (pd.concat(dataframes, ignore_index=True)), temperatures_path



def extract_station_temperatures(all_temperatures):
    """
    Extracts the temperatures for each station across all years and stores them in a dictionary
    """
    
    # Creates a dictionary to store the temperatures for each station across every year
    extracted_temps = {}
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    num_rows = all_temperatures.shape[0]

    # Since the concatenated dataframe has 112 unique rows/stations that repeat in the same order for every year,
    # we only need to iterate through the first 112 rows to get the station names
    for unique_rows in range(112):
        station_name = all_temperatures.iloc[unique_rows]['STATION_NAME']
        temps_list = []
        # A step of 112 is used in the for loop to get the temperature values for each station across all years.
        # This is because the dataframe is structured such that each station's data appears every 112 rows
        for repeat_station_rows in range(unique_rows, num_rows, 112):
            temps = all_temperatures.iloc[repeat_station_rows][months].tolist()
            temps_list.extend(temps)
        extracted_temps[station_name] = temps_list
        
    # Returns the dictionary containing the temperatures for each station
    return extracted_temps



def calculate_averages(all_temperatures):
    """
    Calculates the average temperatures for each season and returns a dictionary with the results
    """
    
    # Calculates the average temperatures for each season
    summer_avgs = all_temperatures[['January', 'February', 'December']].mean()
    total_summer_avg = summer_avgs.mean()

    winter_avgs = all_temperatures[['June', 'July', 'August']].mean()
    total_winter_avg = winter_avgs.mean()    

    autumn_avgs = all_temperatures[['March', 'April', 'May']].mean()
    total_autumn_avg = autumn_avgs.mean()

    spring_avgs = all_temperatures[['September', 'October', 'November']].mean()
    total_spring_avg = spring_avgs.mean()

    # Returns a dictionary with the average temperatures for each season
    return {'Summer': total_summer_avg,
            'Winter': total_winter_avg,
            'Autumn': total_autumn_avg,
            'Spring': total_spring_avg}
    


def calculate_largest_temp_range(all_temps_per_station):
    """
    Calculates the largest temperature range for each station and returns a dictionary with the results
    """

    # The maximum temperature, minimum temperature, and the range between those values for each station is calculated and added to a dictionary
    station_ranges = {}
    max_range = None

    for station, temps in all_temps_per_station.items():
        temp_range = max(temps) - min(temps)
        station_ranges[station] = {
            'range': temp_range,
            'min': min(temps),
            'max': max(temps)}
        
        if (max_range is None) or (temp_range > max_range):
            max_range = temp_range

    # The ranges from the previous dictionary are compared to find the stations with the largest temperature range
    # and a new dictionary is created to store these stations and their temperature ranges
    highest_ranges_dict = {}
    for station, minmaxrange in station_ranges.items():
        if minmaxrange['range'] == max_range:
            highest_ranges_dict[station] = {
                'range': minmaxrange['range'],
                'max': minmaxrange['max'],
                'min': minmaxrange['min']}
            
    # Returns the dictionary containing the stations with the largest temperature range
    return highest_ranges_dict



def calculate_most_stable_temperature(all_temps_per_station):
    """
    Calculates the station with the most stable temperature and returns its name and standard deviation
    as well as the station with the most variable temperature and returns its name and standard deviation
    """
    
    # The station with the most stable temperature is determined by calculating the standard deviation of the temperatures for each station
    # The station with the most variable temperature is also determined in the same way
    most_stable_station = None
    lowest_std_dev = None
    most_variable_station = None
    highest_std_dev = None

    for station, temps in all_temps_per_station.items():
        std_dev = pd.Series(temps).std()
        if (lowest_std_dev is None) or (std_dev < lowest_std_dev):
            lowest_std_dev = std_dev
            most_stable_station = station
        if (highest_std_dev is None) or (std_dev > highest_std_dev):
            highest_std_dev = std_dev
            most_variable_station = station

    # Returns the names and standard deviations of the most stable and most variable stations
    return {'Most Stable': {'station': most_stable_station, 'std_dev': lowest_std_dev},
            'Most Variable': {'station': most_variable_station, 'std_dev': highest_std_dev}}
    
    

def main():
    """
    The main function that reads data from CSV files, analyses it, then writes the results to text files
    """

    # Assigns the concatenated dataframe and folder path to variables
    all_temperatures, temperatures_path = dataframe_concat()
    # Assigns the station names and their temperatures across every year to a dictionary
    all_temps_per_station = extract_station_temperatures(all_temperatures)

    # Determines the parent folder of the 'temperatures' folder so the output files are saved there
    output_folder = os.path.dirname(temperatures_path)

    # Writes the average temperatures to a text file
    avg_file = os.path.join(output_folder, 'average_temp.txt')
    with open(avg_file, 'w') as file:
        averages = calculate_averages(all_temperatures)
        for season, avg in averages.items():
            file.write(f"{season}: {avg:.1f}°C\n")
    
    
    # Writes the largest temperature ranges to a text file        
    range_file = os.path.join(output_folder, 'largest_temp_range_station.txt')
    with open(range_file, 'w') as file:
        highest_ranges = calculate_largest_temp_range(all_temps_per_station)
        for station, values in highest_ranges.items():
            file.write(f"{station}: Range {values['range']:.1f}°C (Max: {values['max']:.1f}°C, Min: {values['min']:.1f}°C)\n")
            
            
    # Writes the most stable and most variable temperatures to a text file
    stability_file = os.path.join(output_folder, 'temperature_stability_stations.txt')
    with open(stability_file, 'w') as file:
        most_stable_variable = calculate_most_stable_temperature(all_temps_per_station)
        for stability, values in most_stable_variable.items():
            file.write(f"{stability}: Station {values['station']}: StdDev {values['std_dev']:.1f}°C\n")


    # Checks if all three files exist before printing success message
    if all(os.path.exists(f) for f in [avg_file, range_file, stability_file]):
        print(f"Results successfully written to files!")    


if __name__ == "__main__":
    main()
