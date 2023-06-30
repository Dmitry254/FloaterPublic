import traceback
import requests
import json
import time
from json import JSONDecodeError
from datetime import datetime
from .models import MarketPatternItem
from main.api_keys import api_key_market_pattern


def collecting_items():
    names_list = []
    try:
        white_list = ["Doppler", "Case Hardened", "Fade1 "]
        url = "https://market.csgo.com/api/v2/prices/class_instance/RUB.json"
        api = requests.get(url)
        data = json.loads(api.text)
        count_items = len(data['items'])
        for item in data['items']:
            try:
                if (any(words in data['items'][item]['market_hash_name'] for words in white_list)
                        and data['items'][item]['price'] and float(data['items'][item]['price']) > 40):
                    if data['items'][item]['avg_price']:
                        avg_price = data['items'][item]['avg_price']
                    else:
                        avg_price = 0
                    name_and_price = [data['items'][item]['market_hash_name'], avg_price]
                    names_list.append(name_and_price)
            except:
                continue
    except:
        traceback.print_exc()
    return names_list


def phase_parser(names_list):
    dict_name_avg = {}
    link_items = ""
    list_items = []
    items_counter = 0
    for item in names_list:
        try:
            if items_counter < 48:
                items_counter += 1
                item_hash_name = item[0]
                item_avg = item[1]
                dict_name_avg.update({item_hash_name: item_avg})
                link_items += "&list_hash_name[]=" + item_hash_name
            else:
                url_item = f"https://market.csgo.com/api/v2/search-list-items-by-hash-name-all?key={api_key_market_pattern}{link_items}"
                link_items = ""
                items_counter = 0
                item_status = requests.get(url_item)
                current_items = json.loads(item_status.text)
                for item_name in current_items['data'].keys():
                    for item_info in current_items['data'][item_name]:
                        if item_info['extra'] and 'phase' in item_info['extra'].keys():
                            class_and_instance = f"{item_info['class']}-{item_info['instance']}"
                            item_link = f"https://market.csgo.com/item/{class_and_instance}"
                            item_seed = "None"
                            item_float = 0
                            item_phase = item_info['extra']['phase']
                            if item_info['extra'] and 'float' in item_info['extra'].keys():
                                item_float = item_info['extra']['float']
                            item_price = float(item_info['price']) / 100
                            item_avg_price = float(dict_name_avg[item_name])
                            list_items.append([item_name, item_link, item_float, item_seed, item_phase, item_price, item_avg_price])
        except JSONDecodeError:
            time.sleep(5)
        except:
            traceback.print_exc()
            continue
    return list_items


def reload_items_data(items_list):
    database_len = MarketPatternItem.objects.all().count()
    items_for_delete = MarketPatternItem.objects.all()[0:database_len]
    for item in items_list:
        try:
            item_name, item_link, item_float, item_seed, item_phase, item_price, item_avg_price = item
            MarketPatternItem.objects.create(market_item_name=item_name, market_item_link=item_link,
                                             market_item_float=item_float, market_item_seed=item_seed,
                                             market_item_phase=item_phase, market_item_price=item_price,
                                             market_item_avg_price=item_avg_price)
        except:
            traceback.print_exc()
            continue
    for item in items_for_delete:
        item.delete()


def market_start_parsing():
    try:
        start_time = datetime.now()
        names_list = collecting_items()
        list_items = phase_parser(names_list)
        if len(list_items) > 5:
            reload_items_data(list_items)
        end_time = datetime.now()
        work_time = end_time - start_time
        print(work_time)
    except:
        traceback.print_exc()


def market_start_parsing_all_time():
    while True:
        try:
            start_time = datetime.now()
            names_list = collecting_items()
            list_items = phase_parser(names_list)
            if len(list_items) > 5:
                reload_items_data(list_items)
            end_time = datetime.now()
            work_time = end_time - start_time
            print(work_time)
        except:
            traceback.print_exc()
