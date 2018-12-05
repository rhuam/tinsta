#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import requests
import json
import re

instagram_url = 'https://www.instagram.com'
login_route = '%s/accounts/login/ajax/' % (instagram_url)
logout_route = '%s/accounts/logout/' % (instagram_url)
profile_route = '%s/%s/'
query_route = '%s/graphql/query/' % (instagram_url)
unfollow_route = '%s/web/friendships/%s/unfollow/'
follow_route = '%s/web/friendships/%s/follow/'

session = requests.Session()


def instagram_conection(username, password):

    session.headers.update({
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'www.instagram.com',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/',
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'),
        'X-Instagram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest'
    })
    session.cookies.update({
        'ig_pr': '1',
        'ig_vw': '1920',
    })

    response = session.get(instagram_url)
    session.headers.update({
        'X-CSRFToken': response.cookies['csrftoken']
    })

    time.sleep(random.randint(2, 6))

    post_data = {
        'username': username,
        'password': password
    }

    response = session.post(login_route, data=post_data, allow_redirects=True)
    response_data = json.loads(response.text)


    if response_data['authenticated']:
        session.headers.update({
            'X-CSRFToken': response.cookies['csrftoken']
        })
    else:
        return get_id(username), {"error": "Acesso restrito"}


    token = response.cookies['csrftoken']
    sessionid = response.cookies['sessionid']

    print("COOKIES CONEXAO: ", response.cookies)
    print("HEADERS CONEXAO: ", response.headers)

    return get_id(username), token, sessionid


# Not so useful, it's just to simulate human actions better
def get_user_profile(username):
    response = session.get(profile_route % (instagram_url, username))
    extract = re.search(r'window._sharedData = (.+);</script>', response.text)
    if (extract == None):
        return {"error": "Usuário inválido"}
    response = json.loads(extract.group(1))
    return response['entry_data']['ProfilePage'][0]['graphql']['user']

def get_id(username):
    profile = get_user_profile(username)
    if 'error' in profile.keys():
        return profile
    return profile['id']


# def follow(user_id, urlgen, user_follow):
def follow(user_follow):

    user_follow_id = get_id(user_follow)

    response = session.get(profile_route % (instagram_url, user_follow_id))
    time.sleep(random.randint(2, 4))


    session.headers.update({
        'X-CSRFToken': response.cookies['csrftoken']
    })

    urlgen = response.cookies['urlgen']

    print("COOKIES ANTES DE SEGUIR: ", response.cookies)
    print("HEADERS ANTES DE SEGUIR: ", response.headers)

    try:
        response = session.post(follow_route % (instagram_url, user_follow_id))

        print("COOKIES DEPOIS DE SEGUIR: ", response.cookies)
        print("HEADERS DEPOIS DE SEGUIR: ", response.headers)

        if response.status_code == 200:
            # response = json.loads(response.text)
            return response

    except Exception as ex:
        print(ex)
        return {'error': ex}



def follow_2(user_follow, token, sessionid, user_id):
    session = requests.Session()
    session.headers.update({
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'www.instagram.com',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/',
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'),
        'X-Instagram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest'
    })

    user_follow_id = get_id(user_follow)

    response = session.get(profile_route % (instagram_url, user_follow_id))
    time.sleep(random.randint(2, 4))

    # update header again, idk why it changed
    session.headers.update({
        'X-CSRFToken': token
    })

    session.cookies.update({
        'ds_user_id=': user_id,
        'sessionid': sessionid,
    })

    print(response.cookies)

    try:
        response = session.post(follow_route % (instagram_url, user_follow_id))

        if response.status_code == 200:
            response = json.loads(response.text)
            return response

    except Exception as ex:
        return {'error': ex}

def main(name, password, follow_user):

    is_logged = instagram_conection(name, password)
    if is_logged == False:
        print('Falha no Login')

    #
    # connected_user = get_user_profile(username)
    # print('You\'re now logged as {} ({} followers, {} following)'.format(connected_user['username'],
    #                                                                      connected_user['edge_followed_by']['count'],
    #                                                                      connected_user['edge_follow']['count']))

    time.sleep(random.randint(1, 5))
    follow(follow_user)

    if 'error' in is_logged[1]:
        return '123','123', '123'
    return is_logged



# if __name__ == "__main__":
#     # main('RhuamSena', 'Sofia&1503')
#     print(get_id('gabiimassi'))
