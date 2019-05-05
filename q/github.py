import os
import sys

import requests
import termcolor
import yaml

_BASE_URL = 'https://api.github.com'


def _credentials():
    with open(os.path.expanduser("~/.q/github_credentials"), 'r') as stream:
        return yaml.safe_load(stream)


def print_notifications():
    credentials = _credentials()
    all_maybe = 'true' if len(sys.argv) < 4 or sys.argv[3] != 'all' else 'false'
    result = requests.get(
        _BASE_URL + f"/notifications?participating={all_maybe}&all=false&per_page=100",
        auth=(credentials['username'], credentials['password'])
    ).json()

    notifications_by_repo = {}
    for notification in result:
        name = notification['repository']['full_name']
        if name not in notifications_by_repo:
            notifications_by_repo[name] = []

        notifications_by_repo[name].append(notification)

    for repo in notifications_by_repo.keys():
        print(termcolor.colored(repo, color='green', attrs=['bold']))
        for notification in notifications_by_repo[repo]:
            notification_details = requests.get(notification['subject']['url'],
                                                auth=(credentials['username'], credentials['password'])
                                                ).json()
            print(
                '    ' +
                f"({notification_details['id']}) " +
                notification_details['user']['login'] + ' ' +
                termcolor.colored(notification['updated_at'], color='cyan') + ' ' +
                termcolor.colored(notification['subject']['type'] + ' ' + notification['reason'],
                                  color='magenta') + ' ' +
                notification['subject']['title']
            )
            print('        ' +
                  (termcolor.colored('[merged]', color='magenta') + ' ' if 'merged' in notification_details.keys() and
                                                                           notification_details['merged'] else '') +
                  termcolor.colored(notification_details['html_url'], color='blue'))
