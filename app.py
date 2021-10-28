import requests
import pandas as pd
import hashlib
import time
from sqlalchemy import create_engine, MetaData, Table, Column, String


def create_dataframe():
    """
    This function make a GET requests to the API to get all countries with a region and language and return a a dataframe that was create using the library pandas.
    """

    start = time.time()
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url).json()
    end = time.time()
    execution_time = (end - start) * 1000

    df = pd.DataFrame(columns=['Region', 'City Name', 'Language', 'Time'])

    for i in range(len(response)):
        start = time.time_ns()
        try:
            country = response[i]['name']['common']
        except KeyError:
            country = 'NA'

        try:
            region = response[i]['region']
        except KeyError:
            region = 'NA'

        try:
            langugages = response[i]['languages']
            langugages = list(langugages.values())
            languages_enc_hex = encript_language(langugages)
            #langugages_str = '|'.join(languages_enc_hex)
        except KeyError:
            langugages = 'NA'

        item = [region, country, languages_enc_hex]
        df = add_to_dataframe(
            df=df, data=item, start_time=start, time_req=execution_time)

    return(df)


def add_to_dataframe(df, data, start_time, time_req):
    """
    This function add rows into dataframe who was created to get all countries with a region and language
    """

    # There are countries with more than one language, for that reason I will iterate over the languages to create a row for each language in the country.
    if len(data[2]) > 1:
        for language in data[2]:
            region = data[0]
            country = data[1]
            end = time.time_ns()
            row_time = ((end - start_time)/1000000)
            row_time_data = f"{row_time:.2f} ms"
            data = [region, country, language, row_time_data]
            temporary_df = pd.DataFrame(
                [data], columns=['Region', 'City Name', 'Language', 'Time'])
            df = df.append(temporary_df, ignore_index=True)

    else:
        data[2] = ''.join(data[2])
        end = time.time_ns()
        row_time = ((end - start_time)/1000000)
        row_time_data = f"{row_time:.2f} ms"
        data.append(row_time_data)
        temporary_df = pd.DataFrame(
            [data], columns=['Region', 'City Name', 'Language', 'Time'])
        df = df.append(temporary_df, ignore_index=True)

    return df


def encript_language(languages):
    """
    This function encrypt a string using SHA-1 and returns a hexadecil strings with the hash.
    """

    langs_hex = []
    for language in languages:
        lang_enc = hashlib.sha1(bytes(language, 'utf-8'))
        lang_hex = lang_enc.hexdigest().upper()
        langs_hex.append(lang_hex)

    return langs_hex


def calcule_times(df, eng):
    """
    This function receives a data frame and calculates the total time, the average time, the minimum and the maximum time that it takes to process all the rows of the table and generates a .json file with these values
    """

    ms = df["Time"].apply(lambda x: float(x.replace('ms', '')))
    sum_ms = f"{ms.sum():.2f} ms"
    avg_ms = f"{ms.mean():.2f} ms"
    max_ms = f"{ms.max()} ms"
    min_ms = f"{ms.min()} ms"
    metrics = {
        "total": sum_ms,
        "avg": avg_ms,
        "min": min_ms,
        "max": max_ms
    }

    df_cal_time = pd.DataFrame(metrics, index=[0])
    df_cal_time = df_cal_time.rename(columns={
                                     'total': 'total_time', 'avg': 'avg_time', 'min': 'min_time', 'max': 'max_time'})

    df_cal_time.to_sql('regions', con=eng, if_exists='append', index=False)


def export_df_to_json(df):
    """
    This function receives a dataframe and generates a json file which it exports in the path of the to_json () function.
    """

    df.to_json(r'exports/data.json')


def create_table_db():
    """
    This function generates the connection to the database and creates a table in the database if the table does not exist.
    """

    engine = create_engine('sqlite:///regions.sqlite')
    meta = MetaData()

    regions = Table(
        'regions', meta,
        Column('total_time', String),
        Column('avg_time', String),
        Column('min_time', String),
        Column('max_time', String),
    )

    regions.create(engine, checkfirst=True)

    return engine


if __name__ == '__main__':
    engine = create_table_db()
    dataframe = create_dataframe()
    dataframe_calc = calcule_times(df=dataframe, eng=engine)
    export_df_to_json(dataframe)
