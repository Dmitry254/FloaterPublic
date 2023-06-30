import requests
import json
import traceback
import pyotp
from datetime import datetime
from .models import BitFloatItem
from main.api_keys import key_and_code_bit_float


def items_price():
    global avg_dict
    data2 = []
    try:
        white_list = ["(Factory New)", "(Minimal Wear)", "(Field-Tested)", "(Well-Worn)", "(Battle-Scarred)"]
        url1 = f"https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key={api_key_bit_float}&code={my_token}"
        api = requests.get(url1)
        data = json.loads(api.text)
        for item in (data['data']['items']):
            try:
                if (any(words in item['market_hash_name'] for words in white_list)
                        and item['recent_sales_info'] and item['recent_sales_info']['average_price']
                        and item['lowest_price'] and float(item['lowest_price']) > 0.5):
                    if item['recent_sales_info']['average_price']:
                        avg_price = item['recent_sales_info']['average_price']
                    else:
                        avg_price = 0
                    data2.append(item['market_hash_name'])
                    avg_dict.update({item['market_hash_name']: float(avg_price)})
            except:
                continue
    except:
        traceback.print_exc()
    return data2


def parser(data):
    for item in data:
        try:
            get_item_id(item)
        except:
            traceback.print_exc()
            continue


def get_item_id(name):
    global list_id
    my_secret = google_code
    my_token = pyotp.totp.TOTP(my_secret).now()
    url = f"https://bitskins.com/api/v1/get_inventory_on_sale/?api_key={api_key_bit_float}&code={my_token}&market_hash_name={name}"
    api = requests.get(url)
    data = json.loads(api.text)
    for item in data['data']['items']:
        try:
            list_id.append(item['item_id'])
            if len(list_id) > 95:
                get_float(list_id)
                list_id = []
        except:
            traceback.print_exc()
            continue


def get_float(list_id):
    global items_list
    my_secret = google_code
    my_token = pyotp.totp.TOTP(my_secret).now()
    list_id = ",".join(list_id)
    url = f"https://bitskins.com/api/v1/get_specific_items_on_sale/?api_key={api_key_bit_float}&code={my_token}&item_ids={list_id}"
    api = requests.get(url)
    data = json.loads(api.text)
    for item_info in data['data']['items_on_sale']:
        try:
            item_name = item_info['market_hash_name']
            max_float_value = 0
            min_float_value = 1
            if "(Factory New)" in item_name:
                max_float_value = 0.01
                min_float_value = 0
            elif "(Minimal Wear)" in item_name:
                max_float_value = 0.08
                min_float_value = 0.07
            elif "(Field-Tested)" in item_name:
                max_float_value = 0.16
                min_float_value = 0.15
            elif "(Well-Worn)" in item_name:
                max_float_value = 0.385
                min_float_value = 0.38
            elif "(Battle-Scarred)" in item_name:
                max_float_value = 0.455
                min_float_value = 0.45
            if item_info['float_value'] and min_float_value < float(item_info['float_value']) < max_float_value:
                item_link = f"https://bitskins.com/view_item?app_id=730&item_id={item_info['item_id']}"
                item_float = float(item_info['float_value'])
                item_price = float(item_info['price'])
                item_avg_price = float(avg_dict[item_name])
                items_list.append([item_name, item_link, item_float, item_price, item_avg_price])
        except:
            traceback.print_exc()
            continue


def reload_items_data(items_list):
    database_len = BitFloatItem.objects.all().count()
    items_for_delete = BitFloatItem.objects.all()[0:database_len]
    for item in items_list:
        try:
            item_name, item_link, item_float, item_price, item_avg_price = item
            BitFloatItem.objects.create(bit_item_name=item_name, bit_item_link=item_link,
                                        bit_item_float=item_float, bit_item_price=item_price, bit_item_avg_price=item_avg_price)
        except:
            traceback.print_exc()
            continue
    for item in items_for_delete:
        item.delete()


def bit_start_parsing():
    try:
        global avg_dict
        global list_id
        global items_list
        global google_code
        global api_key_bit_float
        global my_token
        global my_secret
        start_time = datetime.now()
        avg_dict = {}
        list_id = []
        items_list = []
        key_and_code = key_and_code_bit_float
        api_key_bit_float, google_code = key_and_code
        my_secret = google_code
        my_token = pyotp.totp.TOTP(my_secret).now()
        data = items_price()
        parser(data)
        if len(items_list) > 5:
            reload_items_data(items_list)
        end_time = datetime.now()
        work_time = end_time - start_time
        print(work_time)
    except:
        traceback.print_exc()


def bit_start_parsing_all_time():
    global avg_dict
    global list_id
    global items_list
    global google_code
    global api_key_bit_float
    global my_token
    global my_secret
    api_key_bit_float = ""
    google_code = ""
    while True:
        try:
            start_time = datetime.now()
            avg_dict = {}
            list_id = []
            items_list = []
            my_secret = google_code
            my_token = pyotp.totp.TOTP(my_secret).now()
            data = items_price()
            parser(data)
            if len(items_list) > 5:
                reload_items_data(items_list)
            end_time = datetime.now()
            work_time = end_time - start_time
            print(work_time)
        except:
            traceback.print_exc()
