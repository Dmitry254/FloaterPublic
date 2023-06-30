import traceback
from json import JSONDecodeError
import time
import requests
import json

from django.utils import timezone
from .models import MarketFloatItem
from buysub.models import Subscribers
from datetime import datetime
from main.api_keys import api_key_market_float


def collecting_items():
    list_items = []
    try:
        white_list = ["(Factory New)", "(Minimal Wear)", "(Field-Tested)", "(Well-Worn)", "(Battle-Scarred)"]
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
                    list_items.append(name_and_price)
            except:
                continue
    except:
        traceback.print_exc()
    return list_items


def many_floats(names_list, api_key_market_float):
    floats_list = []
    items_list = []
    link_items = ""
    items_counter = 0
    dict_name_avg = {}
    for item in names_list:
        try:
            if items_counter < 48:
                items_counter += 1
                item_hash_name = item[0]
                item_avg = item[1]
                dict_name_avg.update({item_hash_name: item_avg})
                link_items += "&list_hash_name[]=" + item_hash_name
            else:
                url_items = f"https://market.csgo.com/api/v2/search-list-items-by-hash-name-all?key={api_key_market_float}{link_items} "
                items_counter = 0
                link_items = ""
                items_status = requests.get(url_items)
                current_items = json.loads(items_status.text)
                for item_name in current_items['data'].keys():
                    try:
                        for item_info in current_items['data'][item_name]:
                            try:
                                float_value = 0
                                if "(Factory New)" in item_name:
                                    float_value = 0.01
                                elif "(Minimal Wear)" in item_name:
                                    float_value = 0.08
                                elif "(Field-Tested)" in item_name:
                                    float_value = 0.16
                                elif "(Well-Worn)" in item_name:
                                    float_value = 0.385
                                elif "(Battle-Scarred)" in item_name:
                                    float_value = 0.455
                                if len(item_info['extra']) > 0 and 'float' in item_info['extra'].keys() \
                                        and item_info['price'] and item_info['price'] != 0 \
                                        and (float(item_info['extra']['float']) < float_value or float(item_info['extra']['float']) > 0.98)\
                                        and float(item_info['extra']['float']) not in floats_list:
                                    class_and_instance = f"{item_info['class']}-{item_info['instance']}"
                                    item_link = f"https://market.csgo.com/item/{class_and_instance}"
                                    item_float = float(item_info['extra']['float'])
                                    floats_list.append(item_float)
                                    item_price = float(item_info['price']) / 100
                                    item_avg_price = float(dict_name_avg[item_name])
                                    items_list.append([item_name, item_link, item_float, item_price, item_avg_price])
                            except:
                                traceback.print_exc()
                                continue
                    except:
                        traceback.print_exc()
                        continue
                dict_name_avg.clear()
        except JSONDecodeError:
            time.sleep(5)
        except:
            traceback.print_exc()
            continue
    return items_list


def reload_items_data(items_list):
    database_len = MarketFloatItem.objects.all().count()
    items_for_delete = MarketFloatItem.objects.all()[0:database_len]
    for item in items_list:
        item_name, item_link, item_float, item_price, item_avg_price = item
        MarketFloatItem.objects.create(market_item_name=item_name, market_item_link=item_link,
                                       market_item_float=item_float, market_item_price=item_price,
                                       market_item_avg_price=item_avg_price)
    for item in items_for_delete:
        item.delete()
    stop_sub = Subscribers.objects.all().filter(end_date__lte=timezone.now())
    stop_sub.delete()


def market_start_parsing():
    try:
        start_time = datetime.now()
        names_list = collecting_items()
        items_list = many_floats(names_list, api_key_market_float)
        if len(items_list) > 5:
            reload_items_data(items_list)
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
            items_list = many_floats(names_list, api_key_market_float)
            if len(items_list) > 5:
                reload_items_data(items_list)
            end_time = datetime.now()
            work_time = end_time - start_time
            print(work_time)
        except:
            traceback.print_exc()
