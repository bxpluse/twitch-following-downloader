import requests
import json
import csv
from config import SECRET_CLIENT_ID


def get_following(channel):
    """
    :param channel: Username of channel
    :return: res: Dictionary of following channels
    """
    headers = {'Client-ID': SECRET_CLIENT_ID}
    url = 'https://api.twitch.tv/kraken/users/{0}/follows/channels'
    r = requests.get(url.format(channel), headers=headers)
    json_data = json.loads(r.text)
    res = {}
    try:
        follows_list = json_data['follows']
    except KeyError:
        return res

    # Each request can only fetch 25 channels at a time, so loop through 'next' until all channels are exhausted
    while len(json_data['follows']) > 0:
        for follower in follows_list:
            following_name = str(follower['channel']['display_name'])  # Channel name
            follow_date = str(follower['created_at'])  # Date user followed
            notified = str(follower['notifications'])  # Notifications
            created_date = str(follower['channel']['created_at'])  # Channel created date
            res[following_name] = {'follow_date': follow_date, 'notified': notified, 'created_date': created_date}
        url = json_data['_links']['next']
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)
        follows_list = json_data['follows']

    return res


if __name__ == "__main__":
    if SECRET_CLIENT_ID == "":
        print("Set the client id in config.py")
        exit(0)

    import sys
    if len(sys.argv) != 2:
        print("Usage: python following.py [username]")
        exit(0)

    username = sys.argv[1]  # Change to username to fetch

    following = get_following(username)
    f = open('following.csv', 'w', encoding='utf-8', newline="\n")
    writer = csv.writer(f, dialect='excel', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Channel', 'Follow Date', 'Notifications', 'User Created'])
    for key, value in following.items():
        writer.writerow([key, value['follow_date'], value['notified'], value['created_date']])
