import requests
import json
import traceback
import pyotp
import random
from main.api_keys import api_key_market_find_item_list, api_key_bit_find_item_list


def find_market_item(item_name):
    market_result = []
    url = f"https://market.csgo.com/api/v2/search-list-items-by-hash-name-all?key={api_key_market_find_item}&list_hash_name[]={item_name}"
    item_info = requests.get(url)
    data = json.loads(item_info.text)
    market_item_float = 0
    market_item_phase = "None"
    market_item_seed = "None"
    market_item_name = item_name
    try:
        for item in data['data'][item_name]:
            try:
                market_item_link = f"https://market.csgo.com/item/{item['class']}-{item['instance']}"
                market_item_price = float(item['price']) / 100
                if item['extra']:
                    if "float" in item['extra'].keys():
                        market_item_float = float(item['extra']['float'])
                    if "phase" in item['extra'].keys():
                        market_item_phase = item['extra']['phase']
                    market_result.append({'market_item_name': market_item_name, 'market_item_link': market_item_link,
                                          'market_item_price': market_item_price, 'market_item_seed': market_item_seed,
                                          'market_item_phase': market_item_phase, 'market_item_float': market_item_float,
                                          'shop': 'Market CS:GO'})
            except:
                traceback.print_exc()
                continue
    except TypeError:
        return market_result
    except KeyError:
        return market_result
    return market_result


def find_bit_item(item_name):
    global list_id
    bit_result = []
    list_id = []
    my_secret = google_code
    my_token = pyotp.totp.TOTP(my_secret).now()
    url = f"https://bitskins.com/api/v1/get_inventory_on_sale/?api_key={api_key_bit_find_item}&code={my_token}&market_hash_name={item_name}"
    api = requests.get(url)
    data = json.loads(api.text)
    for item in data['data']['items']:
        try:
            list_id.append(item['item_id'])
            if len(list_id) > 90:
                bit_result += get_info(list_id, item_name)
                list_id = []
        except:
            traceback.print_exc()
            continue
    bit_result += get_info(list_id, item_name)
    return bit_result


def get_info(list_id, item_name):
    bit_result = []
    my_secret = google_code
    my_token = pyotp.totp.TOTP(my_secret).now()
    list_id = ",".join(list_id)
    url = f"https://bitskins.com/api/v1/get_specific_items_on_sale/?api_key={api_key_bit_find_item}&code={my_token}&item_ids={list_id}"
    api = requests.get(url)
    data = json.loads(api.text)
    try:
        for item_info in data['data']['items_on_sale']:
            try:
                bit_item_name = item_name
                bit_item_price = float(item_info['price'])
                bit_item_link = f"https://bitskins.com/view_item?app_id=730&item_id={item_info['item_id']}"
                bit_item_float = (float(item_info['float_value']) if item_info['float_value'] else 0)
                bit_item_phase = item_info['phase']
                bit_item_seed = (item_info['pattern_info']['paintseed'] if 'paintseed' in item_info['pattern_info'].keys() else None)
                bit_result.append({'bit_item_name': bit_item_name, 'bit_item_link': bit_item_link,
                                   'bit_item_price': bit_item_price, 'bit_item_seed': bit_item_seed,
                                   'bit_item_phase': bit_item_phase, 'bit_item_float': bit_item_float,
                                   'shop': 'BitSkins'})
            except:
                traceback.print_exc()
                continue
    except KeyError:
        return bit_result
    return bit_result


def start_script_for_market(item_name, sort_type):
    global api_key_market_find_item
    api_key_market_find_item = random.choice(api_key_market_find_item_list)
    market_result = find_market_item(item_name)
    if isinstance(market_result, list):
        if sort_type == 'min_float':
            market_result = sorted(market_result, key=lambda item: item['market_item_float'])
        elif sort_type == 'max_float':
            market_result = sorted(market_result, key=lambda item: item['market_item_float'], reverse=True)
        elif sort_type == 'min_price':
            market_result = sorted(market_result, key=lambda item: item['market_item_price'])
        elif sort_type == 'max_price':
            market_result = sorted(market_result, key=lambda item: item['market_item_price'], reverse=True)
    return market_result


def start_script_for_bit(item_name, sort_type):
    global api_key_bit_find_item, google_code
    api_key_bit_find_item, google_code = random.choice(api_key_bit_find_item_list)
    bit_result = find_bit_item(item_name)
    if isinstance(bit_result, list):
        if sort_type == 'min_float':
            bit_result = sorted(bit_result, key=lambda item: item['bit_item_float'])
        elif sort_type == 'max_float':
            bit_result = sorted(bit_result, key=lambda item: item['bit_item_float'], reverse=True)
        elif sort_type == 'min_price':
            bit_result = sorted(bit_result, key=lambda item: item['bit_item_price'])
        elif sort_type == 'max_price':
            bit_result = sorted(bit_result, key=lambda item: item['bit_item_price'], reverse=True)
    return bit_result


if __name__ == "__main__":
    # AK-47 | Elite Build (Battle-Scarred) Tec-9 | Fuel Injector (Factory New) Butterfly Knife | Case Hardened (Field-Tested)
    item_name = "Five-SeveN | Case Hardened (Well-Worn)"
    market_result = find_market_item(item_name)
    bit_result = find_bit_item(item_name)
