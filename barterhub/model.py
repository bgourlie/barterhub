from google.appengine.ext import db
from google.appengine.api import memcache
import random

class User(db.Model):
    email = db.EmailProperty(required=True)
    password_hash = db.StringProperty(required=True)
    password_salt = db.StringProperty(required=True)
        
    @staticmethod
    def generate_salt():
        return str(random.random())
        
    @staticmethod
    def authenticate_user(email, password_hash):
        return User.gql('WHERE email = :1 AND password_hash = :2', email, password_hash).get()
    
class Registration(db.Model):
    confirmation_code = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
        
class Category(db.Model):
    name = db.CategoryProperty(required=True)
    parent_ = db.SelfReferenceProperty(required=False)
    lineage = db.ListProperty(db.Key)
    
    @staticmethod
    def good():
        good = memcache.get('GOOD')
        if good is None:
            good = Category.get_by_key_name('good')
            if good is None:
                good = Category(name='Goods', key_name='good')
                good.put()
                memcache.set('GOOD',good)
        return good
        
    @staticmethod
    def service():
        service = memcache.get('SERVICE')
        if service is None:
            service = Category.get_by_key_name('service')
            if service is None:
                service = Category(name='Services', key_name='service')
                service.put()
                memcache.set('SERVICE',service)
        return service
    
    @staticmethod
    def new(name, parent):
        grandparent = parent
        lineage = []
        while grandparent is not None:
            lineage.append(grandparent.key())
            grandparent = grandparent.parent_
        lineage.reverse()
        category = Category(name=name, lineage=lineage, parent_=parent)
        category.put()
        return category
    
    @staticmethod
    def children(category):
        if category is None:
            children = [Category.good(), Category.service()]
        else:
            children = Category.gql('WHERE parent_ = :1', category).fetch(1000)
        return children

class Posting(db.Model):
    category = db.ReferenceProperty(Category)
    title = db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    tags = db.StringListProperty()

class _Session(db.Model):
    sid = db.StringListProperty()
    ip = db.StringProperty()
    ua = db.StringProperty()
    last_activity = db.DateTimeProperty(auto_now=True)
    user = db.ReferenceProperty(User)
