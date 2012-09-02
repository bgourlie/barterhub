import logging
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from lib.sessions import Session
import i18n

logging.getLogger().setLevel(logging.DEBUG)
CACHE_CLIENT = False;
client = ''
lang = 'en'
client_id = 'client_' + lang
logging.debug('client id: ' + client_id)
client = memcache.get(client_id)
if not client:
    logging.debug('client not cached')
    tpl_vars = {}
    tpl_vars['SESSION_COOKIE_NAME'] = Session.COOKIE_NAME
    tpl_vars['i18n'] = i18n.get_lang(lang)
    client = template.render('templates/client.headers', tpl_vars) + \
             template.render('templates/client.html', tpl_vars)
    if CACHE_CLIENT:
        logging.debug('caching client')
        memcache.set(client_id, client)
    
print client


