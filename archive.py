#!/usr/bin/env python

import os, sys
import twitter
import simplejson as json
from pprint import pprint


# Loads Twitter credentials from secrets.json in the current directory
with open("secrets.json") as f:    
    secrets = json.load(f)

# Loads Twitter usernames to archive from users.json
with open("users.json") as f:    
    users = json.load(f)

# Initialize Twitter API object
api = twitter.Api(consumer_key=secrets['api-key'],
                  consumer_secret=secrets['api-secret'],
                  access_token_key=secrets['token-key'],
                  access_token_secret=secrets['token-secret'])


def get_user_directory(user):
    """
    Gets the root directory where a given user's Tweets should be saved.
    Creates the directory automatically if it doesn't exist.
    """
    user_path = os.path.join(data_path, user)
    os.makedirs(user_path, exist_ok=True)
    return user_path


def get_subdirectory(user, base_name):
    """
    Takes the base filename and returns a path to a subdirectory, creating it if needed.
    Currently just using the user_directory so this method is just a stub for future.
    """
    return get_user_directory(user)


def get_last_tweet(user):
    """
    Gets the ID of the last Tweet saved for a given user.
    """
    print('Getting last tweet for {}...'.format(user))
    base = get_user_directory(user)
    max = 0
    for root, dirs, files in os.walk(base, topdown=False):
        for name in files:
            if not name.startswith('.'):
                base_name = name.split('.')[0]
                if int(base_name) > max:
                    max = int(base_name)
    if max > 0:
        print('Last tweet for {} was {}...'.format(user, max))
        return max
    else:
        print('No previous tweet for {}...'.format(user, max))
        return None


def get_tweets(user, since=None):
    """
    Gets all Tweets for a given user.
    If since is provided, gets Tweets since that ID. Otherwise,
    gets all current tweets.
    """
    print('Getting tweets for {} since #{}'.format(user, since))

    if since:
        tweets = api.GetUserTimeline(screen_name=user, since_id=since)
    else:
        tweets = api.GetUserTimeline(screen_name=user)

    return tweets


def save_tweets(tweets):
    """
    Saves all Tweets passed to it.
    Tweets are expected to be Status objects from the Python Twitter module.
    Dictionaries are created automatically using the AsDict() method, and then
    serialized to JSON for saving to disk.
    """
    print('Saving tweets...')
    for tweet in tweets:
        data = tweet.AsDict()
        directory = get_subdirectory(data['user']['screen_name'], data['id_str'])
        filename = '{}.json'.format(data['id_str'])
        path = os.path.join(directory, filename)

        with open(path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)



if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))  # Path to current directory
    data_path = os.path.join(repo_path, '_data')                # Root path for record data
    os.makedirs(data_path, exist_ok=True)

    for user in users:
        print('Archiving {}...'.format(user))
        tweets = get_tweets(user, since=get_last_tweet(user))
        save_tweets(tweets)
