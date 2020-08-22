import requests
import json
import csv
from config import CLIENT_ID, CLIENT_SECRET


def get_oauth():
    url = "https://id.twitch.tv/oauth2/token?client_id={0}&client_secret={1}&grant_type=client_credentials" \
        .format(CLIENT_ID, CLIENT_SECRET)
    r = requests.post(url)
    json_data = json.loads(r.text)
    access_token = json_data['access_token']
    return access_token


def get_following(channel, access_token):
    """
    :param access_token: Access token from OAuth
    :param channel: Username of channel
    :return: res: Dictionary of following where key=username and value=follow_date
    """
    headers = {'Client-ID': CLIENT_ID,
               'Authorization': 'Bearer {0}'.format(access_token)}
    res = {}

    user_id = get_id(channel, access_token)
    if user_id is None:
        return res

    url = "https://api.twitch.tv/helix/users/follows?first=100&from_id={0}"
    r = requests.get(url.format(user_id), headers=headers)
    json_data = json.loads(r.text)

    total = json_data['total']  # total number of following users
    current = 0  # current number of following users fetched

    # Each POST can only fetch 100 users at a time
    while current < total:
        cursor = json_data['pagination']['cursor']  # Cursor to fetch the next batch
        for user in json_data['data']:
            following_name = str(user['to_name'])  # Channel name
            follow_date = str(user['followed_at'])  # Date user followed
            res[following_name] = follow_date
            current += 1

        url = "https://api.twitch.tv/helix/users/follows?first=100&from_id={0}&after={1}"
        r = requests.get(url.format(user_id, cursor), headers=headers)
        json_data = json.loads(r.text)

    return res


def get_id(channel, access_token):
    """
    :param access_token: Access token from OAuth
    :param channel: Username of channel
    :return: user_id: Integer id of user
    """
    headers = {'Client-ID': CLIENT_ID,
               'Authorization': 'Bearer {0}'.format(access_token)}
    id_req = "https://api.twitch.tv/helix/users?login={0}"
    try:
        r = requests.get(id_req.format(channel), headers=headers)
        json_data = json.loads(r.text)
        user_id = json_data['data'][0]['id']
    except:
        user_id = None
    return user_id


if __name__ == "__main__":
    if CLIENT_SECRET == "" or CLIENT_ID == "":
        print("Set the client id and client secret in config.py")
        exit(0)

    import sys

    if len(sys.argv) != 2:
        print("Usage: python following.py [username]")
        exit(0)

    username = sys.argv[1]  # Change to username to fetch

    token = get_oauth()
    following = get_following(username, token)
    f = open('following.csv', 'w', encoding='utf-8', newline="\n")
    writer = csv.writer(f, dialect='excel', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Channel', 'Follow Date', 'Notifications', 'User Created'])
    for key, value in following.items():
        writer.writerow([key, value])
