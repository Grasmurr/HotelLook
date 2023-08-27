import requests
import pandas as pd


def print_results(hotels, i=2):
    if i != 12:
        for hotel in hotels[i - 2:i]:
            print(hotel)
            print(f"Название отеля: {hotel['label']}")
            print(f"Местоположение: {hotel['locationName']}")
            print(f"Широта: {hotel['location']['lat']}")
            print(f"Долгота: {hotel['location']['lon']}")
            print("------------------------")

            df = pd.DataFrame.from_dict(hotel)

            # Выбран mode a, который добавляет данные в конец файла
            df.to_csv('hotels.csv', mode='a')

        continuation = input('Если хотите продолжить поиск, введите +, '
                             '\nесли хотите остановить, любой другой символ: ')
        if continuation == '+':
            i += 2
            print_results(hotels, i)
    else:
        print('Кажется, отели закончились! Попробуйте поиск с другими параметрами')


def get_hotel_data(city, token):
    url = "http://engine.hotellook.com/api/v2/lookup.json"
    params = {
        "query": city,
        "lang": "ru",
        "lookFor": "hotel",
        "limit": 100,
        "token": token
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()


        if data["status"] != "ok":
            print("Не удалось получить данные. Пожалуйста, проверьте запрос.")
            return
    except Exception as E:
        print("Не удалось получить данные. Пожалуйста, проверьте запрос.")
    hotels = data["results"]["hotels"]
    return print_results(hotels)


def hello_user():
    search = input('Добро пожаловать на поисковик среди отелей! '
                   'Рады приветствовать вас! \nИтак, наш поисковик '
                   'устроен достаточно просто - нужно всего лишь ввести'
                   ' название либо города, \nлибо гостиницы, и мы вам выдадим список того, что нашли: ')

    return get_hotel_data(search, "b6118d3185cc46c42971512f2e883f8d")


def handle_df(df_name):
    df = pd.read_csv(df_name)
    print('Итак, самый часто встречающийся город - ', end='')
    print(df['locationName'].value_counts().idxmax())


hello_user()
handle_df('hotels.csv')