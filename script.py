'''
Esse script realiza o tratamento dos dados de venda de carros no EBay
A base de dados original possui como origem o projeto guiado proposto pela
DataQuest, em suas tarefas de Introdução à Pandas.
'''
import pandas as pd

def replace_on_column(dataframe,string,dictionary):
    '''
    Versao simplificada da Funcao de substituicao de valores utilizada pelo Pandas
    Args:
        dataframe: dataframe onde os valores devem ser substituidos
        string: coluna onde os valores se encontram
        dictionary: dicionario dos valores a serem substituidos
    Return: Void
    '''
    dataframe[string].replace(dictionary, inplace = True)

if __name__ == "__main__":

    autos = pd.read_csv('autos.csv', encoding = 'latin-1')

    new_columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
           'vehicle_type', 'registration_year', 'gearbox', 'power_PS', 'model',
           'odometer', 'registration_month', 'fuel_type', 'brand',
           'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
           'last_seen']

    autos.columns = new_columns

    autos['price'] = autos['price'].str.replace('$','').str.replace(',','').astype(float)

    autos['odometer'] = autos['odometer'].str.replace('km','').str.replace(',','').astype(float)

    autos.rename(columns = {'odometer':'odometer_km'}, inplace = True)

    autos = autos[autos["price"].between(0,1000000)]

    autos = autos[autos['registration_year'].between(1900,2022)]

    list_brands = autos['brand'].value_counts().head(20).index

    dict_mean_price = {}
    dict_mean_mileage ={}

    for brand in list_brands:
        serie_brand_price = autos.loc[autos['brand'] == brand, 'price']
        mean_price = serie_brand_price.mean()
        dict_mean_price[brand] = mean_price
        serie_brand_mileage = autos.loc[autos['brand'] == brand, 'odometer_km']
        mean_mileage = serie_brand_mileage.mean()
        dict_mean_mileage[brand] = mean_mileage

    price = pd.Series(mean_price)
    mileage = pd.Series(mean_mileage)

    df_price_mileage = pd.DataFrame(price, columns = ['price'])

    df_price_mileage['mileage'] = mileage

    autos['seller'] = autos['seller'] == 'private'
    autos['offer_type'] = autos['offer_type'] == 'Angebot'

    autos.drop(columns = ['seller','offer_type','nr_of_pictures'], inplace = True)

    autos['ad_created'] = autos['ad_created'].str.replace('-','').str[:8]

    dict_vehicle_type = {'kleinwagen':'small_car',
                         'cabrio':'convertible',
                         'andere':'other'}
    dict_gearbox = {'mannuel':'manual','automatik':'automatic'}
    dict_fuel_type = {'benzin':'gasoline','andere':'other'}
    dict_unrepaired_damage = {'nein':'no','ja':'yes'}
    dict_model = {'andere':'other'}

    replace_on_column(autos,'vehicle_type', dict_vehicle_type)
    replace_on_column(autos,'gearbox', dict_gearbox)
    replace_on_column(autos,'fuel_type',dict_fuel_type)
    replace_on_column(autos,'unrepaired_damage', dict_unrepaired_damage)
    replace_on_column(autos,'model', dict_model)

    print(autos)
