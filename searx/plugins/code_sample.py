from flask_babel import gettext
import re
import requests

name = "Stackoverflow answers infobox"
description = gettext("Combines multiple search engines in order to show a infobox... ")
default_on = True

url = 'https://api.stackexchange.com/2.2/questions/{ids}/answers?order=desc&sort=activity&site=stackoverflow&filter=!-*jbN.OXKfDP'

question_re = r"\/(?:questions|q)\/(?P<id>\d+)"

def post_search(request, search):
    google = search.result_container.results['google']

    relevant = {}
    for result in google:
        domain = result['parsed_url'].netloc
        if domain.endswith('stackoverflow.com'):
            google_path = result['parsed_url'].path
            match = re.match(question_re, google_path)
            if match:
                question_id = match.group('id')
                relevant[question_id] = google_path

    for q_id, q_link in relevant.iteritems():
        req = requests.get(url.format(ids=q_id))
        resp = req.json()
        for answer in resp.get('items', {}):
            if answer['is_accepted']:
                links = [{
                    'url': 'http://stackoverflow.com' + q_link,
                    'title': "Stackoverflow"
                }]
                info_test = {
                    'infobox': answer.get('title', 'Deu zica!'),
                    'engine': "wikipedia",
                    'content': answer.get('body', 'Deuzica2'),
                    'urls': links,
                }
                search.result_container.infoboxes.append(info_test)
                break

    return True
