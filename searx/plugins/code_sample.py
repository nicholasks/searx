from flask_babel import gettext
import re
import requests

name = "Stackoverflow answers infobox"
description = gettext("Shows an infobox containing the possible answer for the question.")
default_on = True

js_dependencies = ('plugins/js/stackoverflow_infobox.js',)

url = 'https://api.stackexchange.com/2.2/questions/{ids}/answers?order=desc&sort=activity&site=stackoverflow&filter=!-*jbN.OXKfDP'
question_re = r"\/(?:questions|q)\/(?P<id>\d+)"

def post_search(request, search):
    try:
        google = search.result_container.results.get('google', {})
    except Exception:
        google = {}

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
                    'infobox': answer.get('title', ' '),
                    'engine': "StackOverFlow",
                    'content': answer.get('body', ' '),
                    'urls': links,
                }
                search.result_container.infoboxes.append(info_test)
                break

    return True
