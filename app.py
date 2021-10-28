import requests
import pandas as pd
import hashlib
import time


def get_all_contries():
    start = time.time()
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url).json()
    end = time.time()
    execution_time = (end - start) * 1000
    
    #list_countries = []
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
        df = add_to_dataframe(df=df, data=item, start_time=start, time_req= execution_time)

    print(df)


def add_to_dataframe(df, data, start_time, time_req):
    #import pdb; pdb.set_trace()
    if len(data[2]) > 1:
        for language in data[2]:
            region = data[0]
            country = data[1]
            end = time.time_ns()
            import pdb; pdb.set_trace()
            row_time = ((end - start_time) * 1000) + time_req
            data = [region, country, language, row_time]
            temporary_df = pd.DataFrame(
                [data], columns=['Region', 'City Name', 'Languages', 'Time'])
            df = df.append(temporary_df, ignore_index=True)

    else:
        end = time.time()
        row_time = ((end - start_time) * 1000) + time_req
        import pdb; pdb.set_trace()
        data.append(row_time)
        temporary_df = pd.DataFrame(
            [data], columns=['Region', 'City Name', 'Languages', 'Time'])
        df = df.append(temporary_df, ignore_index=True)

    return df


def encript_language(languages):
    langs_hex = []
    for language in languages:
        lang_enc = hashlib.sha1(bytes(language, 'utf-8'))
        lang_hex = lang_enc.hexdigest()
        langs_hex.append(lang_hex)

    return langs_hex


if __name__ == '__main__':
    get_all_contries()
