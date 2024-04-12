import pandas as pd

station_file = 'stations_ssn.dat'

def get_all_stations():
    df = pd.read_csv(station_file, delim_whitespace=True, names = ['latitude', 'longitude', 'stnm'], dtype = {'latitude':float, 'longitude':float, 'stnm':str})
    
    return df

def get_station_by_name(name):
    df = get_all_stations()
    return df.loc[df['stnm'] == name]['latitude'][0], df.loc[df['stnm'] == name]['longitude'][0]

if __name__ == '__main__':
    ssn = get_all_stations()
    print(ssn)

    station = get_station_by_name('CAIG')
    print(station)
