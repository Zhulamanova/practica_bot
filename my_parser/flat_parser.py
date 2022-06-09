import requests
from bs4 import BeautifulSoup

from dictionaries import rooms_dict
from work_models.flat import Flat
from work_models.user_request import UserRequest

ROOT_URL = "https://chelyabinsk.n1.ru"

limit_number = 5


async def __get_flat(item) -> Flat:
    test_flat = Flat()
    address_block = item.find("div", {'class': 'card-title living-list-card__inner-block'})
    if address_block is not None:
        test_flat.link = ROOT_URL + address_block.find("a", {'class': 'link'}, href=True)['href']
        test_flat.address = address_block.text.replace("Показать на карте", "")
    test_flat.district = item.find("div", {'class': 'search-item-district living-list-card__inner-block'}).text
    test_flat.price = item.find("div", {'class': 'living-list-card-price__item _object'}).text
    test_flat.floor = item.find("span", {'class': 'living-list-card-floor__item'}).text
    test_flat.area = item.find("div", {
        'class': 'living-list-card__area living-list-card-area living-list-card__inner-block'}).text
    test_flat.upper_address = item.find("div", {
        'class': 'living-list-card__city-with-estate living-list-card-city-with-estate living-list-card__inner-block'}) \
        .text

    image_block = item.find("div", {"class": "offer-list-preview__item _printed-image"})
    test_flat.image_url = image_block.find("img")['src']

    return test_flat


async def __get_flat_list(url: str) -> list:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")

    flat_list = soup.find_all("div", {'class': 'living-list-card'})

    entity_flat_list = list()

    for item in flat_list:
        if item is None:
            continue

        test_flat = await __get_flat(item)
        entity_flat_list.append(test_flat)

    return entity_flat_list


async def validate_request(user_request: str) -> [bool, UserRequest]:
    try:
        params = user_request.split(',')

        if len(params) != 3:
            return [False, None]

        price_arr = params[1].split('до')
        if len(price_arr) != 2:
            return [False, None]

        floor_arr = params[2].split('до')
        if len(floor_arr) != 2:
            return [False, None]

        result_user_request = UserRequest()
        min_price = int(price_arr[0].replace("от", '').strip())
        max_price = int(price_arr[1].strip())
        min_floor = int(floor_arr[0].replace("от", '').strip())
        max_floor = int(floor_arr[1].strip())
        rooms_count = int(params[0].strip())

        await set_user_request_model(max_floor, max_price, min_floor, min_price, result_user_request, rooms_count)

        return [True, result_user_request]
    except():
        return [False, None]


async def set_user_request_model(max_floor, max_price, min_floor, min_price, result_user_request, rooms_count):
    result_user_request.max_price = max_price
    result_user_request.min_price = min_price
    result_user_request.room_count = rooms_count
    result_user_request.max_floor = max_floor
    result_user_request.min_floor = min_floor


async def generate_url(result_user_request: UserRequest) -> str:
    rooms_string = ''
    if rooms_dict.keys().__contains__(result_user_request.room_count):
        rooms_string = 'rooms-' + rooms_dict[result_user_request.room_count]
    result_url = ROOT_URL + '/snyat/dolgosrochno/kvartiry/' + rooms_string \
                 + '/district-' + result_user_request.district \
                 + '/?price_min=' + str(result_user_request.min_price) \
                 + '&price_max=' + str(result_user_request.max_price) \
                 + "&floor_min=" + str(result_user_request.min_floor) \
                 + "&floor_max=" + str(result_user_request.max_floor) \
                 + '&limit=' + str(limit_number)
    return result_url


async def parse(user_request: UserRequest) -> list:
    url = await generate_url(user_request)

    flat_list = await __get_flat_list(url)
    return flat_list
