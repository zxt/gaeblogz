from google.appengine.ext import db
from google.appengine.api import memcache

class Post(db.Model):
    subject = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    content = db.TextProperty()
    created_time = db.DateTimeProperty(auto_now_add=True)
    draft = db.BooleanProperty(default=False)

# TODO: use memcached
def get_draft_posts(offset=0, limit=None):
    q = db.Query(Post)
    return q.filter('draft', True).order('-created_time').run(offset=offset, limit=limit)

def get_published_posts(offset=0, limit=None):
    q = db.Query(Post)
    return q.filter('draft', False).order('-created_time').run(offset=offset, limit=limit)

def get_all_posts(offset=0, limit=None):
    q = db.Query(Post)
    return q.order('-created_time').run(offset=offset, limit=limit)

def get_all_slugs():
    q = db.Query(Post)
    return [p.slug for p in q]

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty()
