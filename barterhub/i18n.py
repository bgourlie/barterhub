REGISTERED_LANGS = ['en']

class I18nException(Exception):
    pass

def get_lang(lang):
    lang_registered = False
    for l in REGISTERED_LANGS:
        if l == lang:
            lang_registered = True
            break
            
    if not lang_registered:
        raise I18nException, 'Requested lang not registered'
        
    try:
        exec "from i18n_" + lang + ' import *'
    except ImportError:
        raise I18nException, 'Could not import lang file'
        
    return i18n()


