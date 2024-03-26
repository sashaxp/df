import requests
import pandas as pd
import json


def load_config(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    return config_data

def getRkList():
    """
    Fetch data from the specified URL with authorization and process it to
    match the structure defined in the Power Query script.

    Returns:
    - pandas.DataFrame: Processed data table.
    """

    # status	
    # integer
    # Enum: -1 4 7 9 11
    # Статус кампании:
    # -1 - кампания в процессе удаления
    # 4 - готова к запуску
    # 7 - кампания завершена
    # 8 - отказался
    # 9 - идут показы
    # 11 - кампания на паузе

    # type	
    # integer
    # Enum: 4 5 6 7
    # Тип кампании:
    # 4 - кампания в каталоге
    # 5 - кампания в карточке товара
    # 6 - кампания в поиске
    # 7 - кампания в рекомендациях на главной странице
    # 8 - автоматическая кампания
    # 9 - поиск + каталог

    # URL and authorization token setup
    url = "https://advert-api.wb.ru/adv/v1/promotion/count"
    PARAM_AUTH_WB_ADVERTIZING = "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNjc4MTU5MSwiaWQiOiI1OTQ4OGQ5NC04NzU0LTQzNTQtOGNhZC0yMDZkM2RlYTgyYjciLCJpaWQiOjQ0MDU0NjIzLCJvaWQiOjUzODEsInMiOjEwNzM3NDE4ODgsInNpZCI6IjIyMWM2ZGY5LTJjOTktNWQ3NC1hN2JlLTc0NzY2YTdlNjE1OCIsInVpZCI6NDQwNTQ2MjN9.OvDKn_B_V2C02gNlsQva_VkJRkbw-7nROBHq2o8DTuhAxR6QzbvBjT3H_U0KH3fL_AfHmKSQCPOnIYlxWW2MPA"


    headers = {
        "accept": "application/json",
        "Authorization": PARAM_AUTH_WB_ADVERTIZING
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

    data = response.json()

    adverts = data.get('adverts', [])
    advert_list = []
    
    for advert in adverts:
        for ad in advert['advert_list']:
            ad_dict = {'type': advert['type'], 'status': advert['status'],
                       'advertId': ad['advertId'], 'changeTime': pd.to_datetime(ad['changeTime']).date()}
            
            advert_list.append(ad_dict)

    df = pd.DataFrame(advert_list)

    # Filter rows with type either 8 or 9
    df_filtered = df[df['type'].isin([8, 9])]

    return df_filtered