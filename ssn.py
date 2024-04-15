import pandas as pd

station_file = '/Users/antonio/Dropbox/python/ssn/stations_ssn.dat'
names = ['No', 'Date', 'Time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference']
dtypes = {'No': int, 'Date': str, 'Time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float,
          'CC': float, 'MAD': float, 'Reference': str}


def get_all_stations():
    df = pd.read_csv(station_file, delim_whitespace=True, names = ['latitude', 'longitude', 'stnm'], dtype = {'latitude':float, 'longitude':float, 'stnm':str})
    
    return df

def get_station_by_name(name):
    df = get_all_stations()
    return df.loc[df['stnm'] == name]['latitude'].to_numpy()[0], df.loc[df['stnm'] == name]['longitude'].to_numpy()[0]

def read_MF_file(match_filter_file, header = None):
    df = pd.read_csv(match_filter_file, delim_whitespace=True, names = names, dtype = dtypes, header = header)
    df['Date'] = df['Date'].str.cat(df['Time'], sep=' ')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S.%f')
    return df

if __name__ == '__main__':
    ssn = get_all_stations()
    print(ssn)

    station = get_station_by_name('CAIG')
    print(station)
