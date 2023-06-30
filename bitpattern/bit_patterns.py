import requests
import json
import traceback
import pyotp
from datetime import datetime
from .models import BitPatternItem
from main.api_keys import key_and_code_bit_pattern


def items_price():
    global avg_dict
    names_list = []
    avg_dict = {}
    white_list = ["Doppler", "Case Hardened", "Fade1 "]
    url1 = f"https://bitskins.com/api/v1/get_price_data_for_items_on_sale/?api_key={api_key_bit_pattern}&code={my_token}"
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
                names_list.append(item['market_hash_name'])
                avg_dict.update({item['market_hash_name']: float(avg_price)})
        except:
            traceback.print_exc()
            continue
    return names_list


def parser(names_list):
    for item in names_list:
        try:
            get_item_id(item)
        except:
            traceback.print_exc()
            continue


def get_item_id(name):
    global list_id
    my_secret = google_code
    my_token = pyotp.totp.TOTP(my_secret).now()
    url = f"https://bitskins.com/api/v1/get_inventory_on_sale/?api_key={api_key_bit_pattern}&code={my_token}&market_hash_name={name}"
    api = requests.get(url)
    data = json.loads(api.text)
    for item in data['data']['items']:
        try:
            list_id.append(item['item_id'])
            if len(list_id) > 95:
                get_phase(list_id)
                list_id = []
        except:
            traceback.print_exc()
            continue


def get_phase(list_id):
    global items_list
    my_secret = google_code
    my_token = pyotp.totp.TOTP(my_secret).now()
    list_id = ",".join(list_id)
    url = f"https://bitskins.com/api/v1/get_specific_items_on_sale/?api_key={api_key_bit_pattern}&code={my_token}&item_ids={list_id}"
    api = requests.get(url)
    data = json.loads(api.text)
    for item_info in data['data']['items_on_sale']:
        try:
            item_name = item_info['market_hash_name']
            item_link = f"https://bitskins.com/view_item?app_id=730&item_id={item_info['item_id']}"
            item_float = float(item_info['float_value'])
            if item_info['pattern_info']['paintseed'] is None:
                item_seed = "None"
            else:
                item_seed = item_info['pattern_info']['paintseed']
            if item_info['phase'] is None:
                item_phase = "None"
            else:
                item_phase = item_info['phase']
            item_price = float(item_info['price'])
            item_avg_price = float(avg_dict[item_name])
            items_list.append([item_name, item_link, item_float, item_seed, item_phase,  item_price, item_avg_price])
        except:
            traceback.print_exc()
            continue


def reload_items_data(items_list):
    database_len = BitPatternItem.objects.all().count()
    items_for_delete = BitPatternItem.objects.all()[0:database_len]
    for item in items_list:
        try:
            item_name, item_link, item_float, item_seed, item_phase, item_price, item_avg_price = item
            BitPatternItem.objects.create(bit_item_name=item_name, bit_item_link=item_link,
                                                bit_item_float=item_float, bit_item_seed=item_seed, bit_item_phase=item_phase,
                                                bit_item_price=item_price, bit_item_avg_price=item_avg_price)
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
        global api_key_bit_pattern
        global my_token
        global my_secret
        start_time = datetime.now()
        avg_dict = {}
        list_id = []
        items_list = []
        api_key_bit_pattern = ""
        google_code = ""
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
    global api_key_bit_pattern
    global my_token
    global my_secret
    key_and_code = key_and_code_bit_pattern
    api_key_bit_pattern, google_code = key_and_code
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
