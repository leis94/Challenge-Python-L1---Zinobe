import requests
import pandas as pd
import hashlib

def get_all_contries():
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url).json()
    
    # country = response[0]['name']['common']
    # # print(country)

    # region = response[0]['region']

    # langugages = response[0]['languages']
    
    # print(response[0]['region'])
    # print(response[0]['languages'])

    list_countries = []

    for i in range(len(response)):
        #print(i)
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
            langugages_str = '|'.join(languages_enc_hex)
        except KeyError:
            langugages = 'NA'
        
        item = [region, country, langugages_str]
        df = add_to_dataframe(item)
        list_countries.append(item)

    #df = add_to_dataframe(list_countries)
    
    print(df)


def add_to_dataframe(list_of_countries):
    #df = pd.DataFrame(list_of_countries, columns=['Region', 'City Name', 'Languages'])
    df = pd.DataFrame(columns=['Region', 'City Name', 'Languages'])

    #print(list_of_countries)

    df = df.append(list_of_countries)

    #print(df)
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