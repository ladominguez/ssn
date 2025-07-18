import pandas as pd
import numpy as np

station_file = '/Users/antonio/Dropbox/python/ssn/stations_ssn.dat'
names = ['No', 'date', 'time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference']
dtypes = {'No': int, 'date': str, 'time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float,
          'CC': float, 'MAD': float, 'Reference': str}

names_ssn = ['date', 'time', 'magnitude', 'latitude', 'longitude', 'depth', 'comments', 'local_date', 'local_time','status']
dtypes_ssn = {'date': str, 'time': str, 'magnitude': float, 'latitude': float, 'longitude': float, 'depth': float,
             'comments': str, 'local_date': str, 'local_time': str, 'status': str}
default_catalog = '/Users/antonio/Dropbox/BSL/CRSMEX/Catalogs/CATALOG_2001_2023_clean.DAT'
names_default_catalog = ['date', 'time', 'latitude', 'longitude', 'depth', 'magnitude','eq_id']
types_default_catalog = {'date': str, 'time': str, 'latitude': float, 'longitude': float, 'depth': float, 'magnitude':
                         float, 'eq_id': str}

names_ssn_catalog = ["date","time","magnitude","latitude","longitude","depth","reference","local_date","local_time","status"]
types_ssn_catalog = {"date":str,
                     "magnitude": float,
                     "latitude": float,
                     "longitude": float,
                     "depth": float,
                     "reference": str,
                     "local_date": str,
                     "local_time": str}

simple_catalog = {'date': pd.Series(dtype='str'), 
                  'latitude': pd.Series(dtype='float'),
                  'longitude': pd.Series(dtype='float'),
                  'depth': pd.Series(dtype='float'),
                  'magnitude': pd.Series(dtype='float')}

AZUL =(17.98652, -102.35257)
IGIG =(20.75304, -101.32780)

def _combine_date_time_to_datetime(df, ssn=True):
    df['date'] = df['date'].str.cat(df['time'], sep=' ')
    if ssn:
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    else:
        df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d %H:%M:%S.%f')
    return df

def _combine_date_time_to_datetime_ssn(df):
    df['date'] = df['date'].str.cat(df['time'], sep=' ')
    df['datetime'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    df = df.drop('time', axis=1)
    df = df.drop('date', axis=1)
    df = df.rename(columns={'datetime': 'date'})

    return df

def _combine_date_time_to_datetime_ssn(df):
    df['date'] = df['date'].str.cat(df['time'], sep=' ')
    df['datetime'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    df = df.drop('time', axis=1)
    df = df.drop('date', axis=1)
    df = df.rename(columns={'datetime': 'date'})

    return df

def read_catalog4repeaters(filename=default_catalog):
    df = pd.read_csv(filename, delim_whitespace=True, names = names_default_catalog, dtype = types_default_catalog)
    return _combine_date_time_to_datetime(df)

def get_profile_ssn(df, point_a, point_b,min_distance_threshold,  num_points = 100,  magnitude_min = 3.5, save=False):
    from interpolate_gc import interpolate_great_circle
    from geopy.distance import great_circle

    interpolation_line = interpolate_great_circle(point_a,point_b, num_points = 100)

    out = pd.DataFrame(simple_catalog)
    

    for _, row in df.iterrows():
        distances = []
        for line_point in interpolation_line:
            distances.append(great_circle((row['latitude'], row['longitude']), line_point).km)
        
        min_distance = np.array(distances).min()
        if min_distance <= min_distance_threshold:
            min_distance = np.array(distances).min()
            out = pd.concat([out, pd.DataFrame({'date': [row['date']],
                                               'latitude': [row['latitude']],
                                               'longitude': [row['longitude']],
                                               'depth': [row['depth']],
                                               'magnitude': [row['magnitude']]})], ignore_index=True)
            distance_from_start = great_circle(point_a,(row['latitude'], row['longitude'])).km 
            print(row['date'], row['latitude'], row['longitude'], row['depth'], row['magnitude'], distance_from_start)

    

    
    return out

def read_ssn_catalog(filename):  # This function is repeated. It does the same as read_ssn_file
    """
    WARNING. Remove last 7 trailing lines
    """
    df = pd.read_csv(filename, sep=",", names = names_ssn_catalog, dtype = types_ssn_catalog, skiprows = 5)
    return _combine_date_time_to_datetime(df)

def get_all_stations(network = None):
    df = pd.read_csv(station_file, sep=r'\s+', names = ['latitude', 'longitude', 'stnm'], dtype = {'latitude':float, 'longitude':float, 'stnm':str}) 
    if network:
        for row in df.itertuples():
            net_id = row.stnm[2:4]
            if network != net_id:
                df.drop(row.Index, inplace=True)            
    return df

def get_station_by_name(name):
    df = get_all_stations()
    return df.loc[df['stnm'] == name.upper()]['latitude'].to_numpy()[0], df.loc[df['stnm'] == name.upper()]['longitude'].to_numpy()[0]


def read_MF_file(match_filter_file, header = None):
    df = pd.read_csv(match_filter_file, delim_whitespace=True, names = names, dtype = dtypes, header = header)
    return _combine_date_time_to_datetime(df)

def read_ssn_file(ssn_file, header = None):
    df = pd.read_csv(ssn_file, delimiter=',', names = names_ssn, dtype = dtypes_ssn, skiprows=5)
    return _combine_date_time_to_datetime_ssn(df)

def filter_time_interval(df, t_start, t_end):
    filtered_df = df[(df['date'] >= start_time) & (df['date'] <= end_time)]
    return filtered_df

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

def M0_from_Mw(Mw):
    return 10**(1.5*Mw + 9.1)

def logM0_from_Mw(Mw):
    return (1.5*Mw + 9.1)

def Mw_from_M0(M0):
    return (2/3)*(np.log10(M0) - 9.1)

def Mw_from_logM0(logM0):
    return (2/3)*(logM0 - 9.1)

if __name__ == '__main__':
    #ssn = get_all_stations()
    #print(ssn)

    #station = get_station_by_name('CAIG')
    #print(station)
    catalog_file = '/Users/antonio/SynologyDrive/Research/Tomography/MP/Section/SSNMX_catalogo_20010101_20250414_utc_m35_99_MICH.csv'

    df = read_ssn_file(catalog_file)
    df = get_profile_ssn(df, AZUL, IGIG, 5)
    pass
