import os
import logging
from google.appengine.ext import db
from model import User, Category
from lib.sessions import Session

logging.getLogger().setLevel(logging.DEBUG)

def appInit():
    session = Session()
    user = session.get_user()
    user = None
    logged_in = str(int(user is not None))
    email = ''
    try:
        email = user.email
    except AttributeError:
        pass
    
    print 'Content-Type: text/plain;charset=UTF-8'
    print session.cookie_header()
    print ''
    print logged_in + ',' + email

def doLogin(args):
    user = None
    login_info = args.split(',',2)
    try:
        email_address = login_info[0]
        password_hash = login_info[1]
        user = User.gql('WHERE email_address = :1 AND password_hash = :2', email_address, password_hash).get()
    except IndexError:
        pass
    
    print 'Content-Type: text/plain;charset=UTF-8'
    print ''
    if user is None:
        print '0'
    else:
        Session().set_user(user)
        print '1'

def requestSession():
    print 'Content-Type: text/plain;charset=UTF-8'
    print Session().cookie_header()
    print ''
    print '0'
        

def getSalt(email):
    print 'Content-Type: text/plain;charset=UTF-8'
    print ''
    logging.debug('email: ' + email)
    user = User.gql('WHERE email = :1', email).get()
    if user is not None:
        salt = user.password_salt
    else:
        #send back a dummy salt
        salt = User.generate_salt()
        
    print salt

def getCategory(current_category_key):
    current_category = None
    lineage = []
    
    try:
        current_category = Category.get(db.Key(current_category_key))
        lineage = [Category.get(key) for key in current_category.lineage]
    except db.BadKeyError:
        pass
    except AttributeError:
        pass
    
    #todo - massive oppurtunity for optimization
    retval = current_category.key().__str__() + ',' + current_category.name + ';'
    
    for category in lineage:
        retval += category.key().__str__() + ',' + category.name + ','
    retval += ';'
    
    for category in Category.children(current_category):
        retval += category.key().__str__() + ',' + category.name + ','
    
    print 'Content-Type: text/plain;charset=UTF-8'
    print ''
    print retval

req = os.environ['PATH_INFO']
args = os.environ['QUERY_STRING']
if req == '/async/request_salt':
    getSalt(args)
elif req == '/async/category':
    getCategory(args)
elif req == '/async/app_init':
    appInit()
elif req == '/async/request_session':
    requestSession()
elif req == '/async/do_login':
    doLogin(args)
else:
    pass
    #404 not found

