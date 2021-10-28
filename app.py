import requests
import pandas as pd
import hashlib
import time
import json


def create_table():
    """
    This function make a GET requests to the API to get all countries with a region and language and return a a dataframe that was create using the library pandas.
    """
    start = time.time()
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url).json()
    end = time.time()
    execution_time = (end - start) * 1000

    df = pd.DataFrame(columns=['Region', 'City Name', 'Languages', 'Time'])

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
                [data], columns=['Region', 'City Name', 'Languages', 'Time'])
            df = df.append(temporary_df, ignore_index=True)

    else:
        end = time.time_ns()
        row_time = ((end - start_time)/1000000)
        row_time_data = f"{row_time:.2f} ms"
        data.append(row_time_data)
        temporary_df = pd.DataFrame(
            [data], columns=['Region', 'City Name', 'Languages', 'Time'])
        df = df.append(temporary_df, ignore_index=True)

    return df


def encript_language(languages):
    """
    This function encrypt a string using SHA-1 and returns a hexadecil strings with the hash.
    """
    langs_hex = []
    for language in languages:
        lang_enc = hashlib.sha1(bytes(language, 'utf-8'))
        lang_hex = lang_enc.hexdigest()
        langs_hex.append(lang_hex)

    return langs_hex


def calcule_times(df):
    ms = df["Time"].apply(lambda x: float(x.replace('ms', '')))
    sum_ms = f"{ms.sum():.2f} ms"
    avg_ms = f"{ms.mean():.2f} ms"
    max_ms = f"{ms.max()} ms"
    min_ms = f"{ms.min()} ms"
    print(f"Total time: {sum_ms}")
    print(f"Average time: {avg_ms}")
    print(f"Max time: {max_ms}")
    print(f"Min time: {min_ms}")
    metrics = {
        "avg": avg_ms,
        "total": sum_ms,
        "max": max_ms,
        "min": min_ms
    }
    with open('./exports/metrics.json', 'w') as fp:
        json.dump(metrics, fp)


def save_df_to_bd(df):
    pass

if __name__ == '__main__':
    dataframe = create_table()
    calcule_times(df=dataframe)
    save_df_to_bd(df=dataframe)
