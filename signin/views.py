from django.shortcuts import render, redirect, HttpResponse
from .steamsignin import SteamSignIn
from urllib.parse import unquote
from .models import CustomUser
from django.contrib.auth import authenticate, login
from main.help_defs import base_view
from main.api_keys import steam_api
import json
import requests


@base_view
def signin(request):
    steamLogin = SteamSignIn()
    encodedData = steamLogin.ConstructURL('http://127.0.0.1:8000/getauthinfo')
    encodedData = 'https://steamcommunity.com/openid/login?{0}'.format(encodedData)
    response = HttpResponse(content="", status=303)
    response["Location"] = encodedData
    response["Content-type"] = 'application/x-www-form-urlencoded'
    return response


@base_view
def getauthinfo(request):
    auth_info = request.get_full_path()
    auth_info = auth_info.replace("/en/getauthinfo?", "")
    auth_info = auth_info.replace("/ru/getauthinfo?", "")
    result = dict(x.split('=') for x in auth_info.split('&'))
    for i in result.keys():
        result[i] = unquote(result[i])
    steamLogin = SteamSignIn()
    returnedSteamID = steamLogin.ValidateResults(result)
    url_req = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_api}&steamids={returnedSteamID}"
    api_req = requests.get(url_req)
    data = json.loads(api_req.text)
    if data['response']['players']:
        account_name = data['response']['players'][0]['personaname']
        account_id = returnedSteamID
        full_avatar = data['response']['players'][0]['avatarfull']
        medium_avatar = data['response']['players'][0]['avatarmedium']
        mini_avatar = data['response']['players'][0]['avatar']
        password = "12340987"
        if not CustomUser.objects.all().filter(steamid=account_id):
            CustomUser.objects.create_user(steamid=account_id, nickname=account_name, password=password,
                                           full_avatar=full_avatar, medium_avatar=medium_avatar, mini_avatar=mini_avatar)
        current_user = CustomUser.objects.get(steamid=account_id)
        if current_user.nickname != account_name:
            current_user.nickname = account_name
            current_user.save()
        if current_user.full_avatar != full_avatar:
            current_user.full_avatar = full_avatar
            current_user.medium_avatar = medium_avatar
            current_user.mini_avatar = mini_avatar
            current_user.save()
        user = authenticate(request, steamid=account_id, password=password)
        login(request, user)
    return redirect('home')

# 'profileurl': 'https://steamcommunity.com/profiles/76561198209299857
# 'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/2c/2c1621e558172b740888c641dca58114da2a26da.jpg'
# 'avatarmedium': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/2c/2c1621e558172b740888c641dca58114da2a26da_medium.jpg'
# 'avatarfull': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/2c/2c1621e558172b740888c641dca58114da2a26da_full.jpg', 'avatarhash': '2c1621e558172b740888c641dca58114da2a26da'
