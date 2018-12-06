# coding=utf-8
import json
from api.tinder_master import fb_auth_token

import requests

class TinderErro(Exception):
    def __init__(self, valor):
        self.valor = valor
    def __str__(self):
        return repr({'error': self.valor})


headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)",
    "Accept": "application/json",
}

host = 'https://api.gotinder.com'


def get_auth_token(fb_auth_token, fb_user_id):
    if "error" in fb_auth_token:
        return {"error": "could not retrieve fb_auth_token"}
    if "error" in fb_user_id:
        return {"error": "could not retrieve fb_user_id"}
    url = host + '/auth'
    req = requests.post(url,
                        headers=headers,
                        data=json.dumps(
                            {'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
                        )

    if 'token' in req.json():
        return req.json()
    else:
        raise TinderErro("Acesso não autorizado")

    # try:
    #     print(req.json())
    #     # breakpoint()
    #     tinder_auth_token = req.json()["token"]
    #     print("You have been successfully authorized!")
    #
    #     return req.json()
    # except Exception as e:
    #     print(e)
    #     return {"error": "Algo deu errado. Desculpe, mas não conseguimos autorizá-lo."}


def facebook_conection(name, password):
    fb_access_token = fb_auth_token.get_fb_access_token(name, password)
    fb_user_id = fb_auth_token.get_fb_id(fb_access_token)

    return fb_user_id, fb_access_token
    # res = get_auth_token(fb_access_token, fb_user_id)
    # if "error" in res:
    #     return False
    # return True

def tinder_conection(fb_access_token, fb_user_id):
    res = get_auth_token(fb_access_token, fb_user_id)
    # if "error" in res:
    #     return res
    return res


def get_recommendations(tinder_auth_token):
    '''
    Returns a list of users that you can swipe on
    '''

    headers.update({"X-Auth-Token": tinder_auth_token})

    try:
        r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting recomendations:", e)


def get_updates(last_activity_date=""):
    '''
    Returns all updates since the given activity date.
    The last activity date is defaulted at the beginning of time.
    Format for last_activity_date: "2017-07-09T10:28:13.392Z"
    '''
    try:
        url = host + '/updates'
        r = requests.post(url,
                          headers=headers,
                          data=json.dumps({"last_activity_date": last_activity_date}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting updates:", e)


def get_self():
    '''
    Returns your own profile data
    '''
    try:
        url = host + '/profile'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your data:", e)


def change_preferences(**kwargs):
    '''
    ex: change_preferences(age_filter_min=30, gender=0)
    kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
    age_filter_min: 18..46
    age_filter_max: 22..55
    age_filter_min <= age_filter_max - 4
    gender: 0 == seeking males, 1 == seeking females
    distance_filter: 1..100
    discoverable: true | false
    {"photo_optimizer_enabled":false}
    '''
    try:
        url = host + '/profile'
        r = requests.post(url, headers=headers, data=json.dumps(kwargs))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not change your preferences:", e)


def get_meta():
    '''
    Returns meta data on yourself. Including the following keys:
    ['globals', 'client_resources', 'versions', 'purchases',
    'status', 'groups', 'products', 'rating', 'tutorials',
    'travel', 'notifications', 'user']
    '''
    try:
        url = host + '/meta'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your metadata:", e)

def update_location(lat, lon):
    '''
    Updates your location to the given float inputs
    Note: Requires a passport / Tinder Plus
    '''
    try:
        url = host + '/passport/user/travel'
        r = requests.post(url, headers=headers, data=json.dumps({"lat": lat, "lon": lon}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)

def reset_real_location():
    try:
        url = host + '/passport/user/reset'
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)


def get_recs_v2():
    '''
    This works more consistently then the normal get_recommendations becuase it seeems to check new location
    '''
    try:
        url = host + '/v2/recs/core?locale=en-US'
        r = requests.get(url, headers=headers)
        return r.json()
    except Exception as e:
        print('excepted')

def set_webprofileusername(username):
    '''
    Sets the username for the webprofile: https://www.gotinder.com/@YOURUSERNAME
    '''
    try:
        url = host + '/profile/username'
        r = requests.put(url, headers=headers,
                         data=json.dumps({"username": username}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not set webprofile username:", e)

def reset_webprofileusername(username):
    '''
    Resets the username for the webprofile
    '''
    try:
        url = host + '/profile/username'
        r = requests.delete(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not delete webprofile username:", e)

def get_person(id):
    '''
    Gets a user's profile via their id
    '''
    try:
        url = host + '/user/%s' % id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get that person:", e)


def send_msg(match_id, msg):
    try:
        url = host + '/user/matches/%s' % match_id
        r = requests.post(url, headers=headers,
                          data=json.dumps({"message": msg}))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not send your message:", e)


def superlike(person_id):
    try:
        url = host + '/like/%s/super' % person_id
        r = requests.post(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not superlike:", e)


def like(person_id, tinder_auth_token):
    headers.update({"X-Auth-Token": tinder_auth_token})
    try:
        url = host + '/like/%s' % person_id
        r = requests.get(url, headers=headers)
        print(r.json())
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not like:", e)


def dislike(person_id, tinder_auth_token):
    headers.update({"X-Auth-Token": tinder_auth_token})
    try:
        url = host + '/pass/%s' % person_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not dislike:", e)


def report(person_id, cause, explanation=''):
    '''
    There are three options for cause:
        0 : Other and requires an explanation
        1 : Feels like spam and no explanation
        4 : Inappropriate Photos and no explanation
    '''
    try:
        url = host + '/report/%s' % person_id
        r = requests.post(url, headers=headers, data={
                          "cause": cause, "text": explanation})
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not report:", e)


def match_info(match_id):
    try:
        url = host + '/matches/%s' % match_id
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)

def all_matches():
    try:
        url = host + '/v2/matches'
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your match info:", e)

def fast_match_info():
  try:
      url = host + '/v2/fast-match/preview'
      r = requests.get(url, headers=headers)
      count = r.headers['fast-match-count']
      # image is in the response but its in hex..
      return count
  except requests.exceptions.RequestException as e:
      print("Something went wrong. Could not get your fast-match count:", e)

def trending_gifs(limit=3):
  try:
      url = host + '/giphy/trending?limit=%s' % limit
      r = requests.get(url, headers=headers)
      return r.json()
  except requests.exceptions.RequestException as e:
      print("Something went wrong. Could not get the trending gifs:", e)

def gif_query(query, limit=3):
  try:
      url = host + '/giphy/search?limit=%s&query=%s' % (limit, query)
      r = requests.get(url, headers=headers)
      return r.json()
  except requests.exceptions.RequestException as e:
      print("Something went wrong. Could not get your gifs:", e)


# def see_friends():
#     try:
#         url = config.host + '/group/friends'
#         r = requests.get(url, headers=headers)
#         return r.json()['results']
#     except requests.exceptions.RequestException as e:
#         print("Something went wrong. Could not get your Facebook friends:", e)
