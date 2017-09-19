from app import app, mongo

from flask import Blueprint, request, jsonify
from urllib.request import unquote

webfinger = Blueprint('webfinger', __name__, template_folder='templates')

@webfinger.route('/')
def get_user_info(**kwargs):
  id = request.args['resource']
  u = mongo.db.users.find_one({'id': id})

  jrd = {
          'subject': u['id'],
          'aliases': [
            request.url_root+'@'+u['username'],
            request.url_root+'users/'+u['username']
          ],
          'properties': {
            'http://schema.org/name': u['name']
          },
          'links': [
            {
              'rel': 'http://webfinger.net/rel/profile-page',
              'href': request.url_root+'@'+u['username']
            },
            {
              'href': request.url_root+'api/'+u['username']+'/feed',
              'rel': 'self',
              'type': 'application/activity+json'
            }
          ]
        }

  return jsonify(jrd)


