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

def read_repeaters_file(file='../data/time_intervals_20240125.dat'):
    with open(file, 'r') as f:
        lines = f.readlines()
        #df = pd.DataFrame(columns=['id', 'latitude', 'longitude',
        #                           'depth', 'mag', 'no_repeaters',
        #                           'Tr','dates'], dtype={'id':int,'latitude':float,
        #                                               'longitude':float,'depth':float,
        #                                               'mag':float,'no_repeaters':int,
        #                                               'Tr':str,'dates':str})
        df = pd.DataFrame({'id': pd.Series(dtype=int), 'latitude': pd.Series(dtype=float),
                           'longitude': pd.Series(dtype=float), 'depth': pd.Series(dtype=float),
                           'mag': pd.Series(dtype=float), 'no_repeaters': pd.Series(dtype=int),
                           'Tr': pd.Series(dtype=str), 'dates': pd.Series(dtype=str)})
        for k, line in enumerate(lines):
            info = line.split(';')
            row = pd.Series({'id':k+1,
            'latitude': float(info[0].strip().split()[0]),
            'longitude': float(info[0].strip().split()[1]),
            'depth':  float(info[0].strip().split()[2]),
            'mag': float(info[0].strip().split()[3]),
            'no_repeaters': int(info[1].strip()),
            'Tr': info[2].strip(),
            'dates': info[3].strip()})
            df = pd.concat([df, row.to_frame().T], ignore_index=True)

    return df

if __name__ == '__main__':
    ssn = get_all_stations()
    print(ssn)

    station = get_station_by_name('CAIG')
    print(station)
