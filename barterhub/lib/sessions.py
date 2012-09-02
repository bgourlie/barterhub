# main python imports
import os
import time
import datetime
import random
import sha
import Cookie

import __main__

# google appengine imports
from google.appengine.ext import db

from model import _Session, User


class Session(object):
    COOKIE_NAME = 'bh-sid'
    DEFAULT_COOKIE_PATH = '/'
    SESSION_EXPIRE_TIME = 7200 # sessions are valid for 7200 seconds (2 hours)
    CLEAN_CHECK_PERCENT = 15 # 15% of all requests will clean the database
    CHECK_IP = True # validate sessions by IP
    CHECK_USER_AGENT = True # validate sessions by user agent
    SET_COOKIE_EXPIRES = False # Set to True to add expiration field to cookie
    SESSION_TOKEN_TTL = 5 # Number of seconds a session token is valid for.
    
    def __init__(self):
        
        #Check the cookie and, if necessary, create a new one.
        self.sid = None
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)
        # check for existing cookie
        if self.cookie.get(Session.COOKIE_NAME):
            self.sid = self.cookie[Session.COOKIE_NAME].value
            # If there isn't a valid session for the cookie sid,
            # start a new session.
            self.session = self._get_session()
            if self.session is None:
                self.sid = self.new_sid()
                self.session = _Session()
                self.session.ua = os.environ['HTTP_USER_AGENT']
                self.session.ip = os.environ['REMOTE_ADDR']
                self.session.sid = [self.sid]
                self.cookie[Session.COOKIE_NAME] = self.sid
                self.cookie[Session.COOKIE_NAME]['path'] = Session.DEFAULT_COOKIE_PATH
                if Session.SET_COOKIE_EXPIRES:
                    self.cookie[Session.COOKIE_NAME]['expires'] = \
                        Session.SESSION_EXPIRE_TIME
            else:
                # check the age of the token to determine if a new one
                # is required
                duration = datetime.timedelta(seconds=Session.SESSION_TOKEN_TTL)
                session_age_limit = datetime.datetime.now() - duration
                if self.session.last_activity < session_age_limit:
                    self.sid = self.new_sid()
                    if len(self.session.sid) > 2:
                        self.session.sid.remove(self.session.sid[0])
                    self.session.sid.append(self.sid)
                else:
                    self.sid = self.session.sid[-1]
                self.cookie[Session.COOKIE_NAME] = self.sid
                self.cookie[Session.COOKIE_NAME]['path'] = Session.DEFAULT_COOKIE_PATH
                if Session.SET_COOKIE_EXPIRES:
                    self.cookie[Session.COOKIE_NAME]['expires'] = \
                        Session.SESSION_EXPIRE_TIME
        else:
            self.sid = self.new_sid()
            self.session = _Session()
            self.session.ua = os.environ['HTTP_USER_AGENT']
            self.session.ip = os.environ['REMOTE_ADDR']
            self.session.sid = [self.sid]
            self.cookie[Session.COOKIE_NAME] = self.sid
            self.cookie[Session.COOKIE_NAME]['path'] = Session.DEFAULT_COOKIE_PATH
            if Session.SET_COOKIE_EXPIRES:
                self.cookie[Session.COOKIE_NAME]['expires'] = Session.SESSION_EXPIRE_TIME

        
        # update the last_activity field in the datastore every time that
        # the session is accessed. This also handles the write for all
        # session data above.
        
        self.session.put()

        # randomly delete old stale sessions in the datastore (see
        # CLEAN_CHECK_PERCENT variable)
        if random.randint(1, 100) < Session.CLEAN_CHECK_PERCENT:
            self._clean_old_sessions()

    def new_sid(self):
        #Create a new session id.
        sid = sha.new(repr(time.time()) + os.environ['REMOTE_ADDR'] + \
                str(random.random())).hexdigest()
        return sid

    def _get_session(self):
        #Get the user's session from the datastore
        query = _Session.all()
        query.filter('sid', self.sid)
        if Session.CHECK_USER_AGENT:
            query.filter('ua', os.environ['HTTP_USER_AGENT'])
        if Session.CHECK_IP:
            query.filter('ip', os.environ['REMOTE_ADDR'])
        results = query.fetch(1)
        if len(results) is 0:
            return None
        else:
            sessionAge = datetime.datetime.now() - results[0].last_activity
            if sessionAge.seconds > Session.SESSION_EXPIRE_TIME:
                results[0].delete()
                return None
            return results[0]
    
    def delete(self):
        self.session.delete()

    def _clean_old_sessions(self):
        duration = datetime.timedelta(seconds=Session.SESSION_EXPIRE_TIME)
        session_age = datetime.datetime.now() - duration
        query = _Session.all()
        query.filter('last_activity <', session_age)
        results = query.fetch(1000)
        for result in results:
            result.delete()
    
    def cookie_header(self):
        return self.cookie.__str__()
    
    def set_user(self, user):
        self.session.user = user
        self.session.put()
    
    def get_user(self):
        return self.session.user
    
    def del_user(self):
        self.session.user = None
        self.session.user.put()