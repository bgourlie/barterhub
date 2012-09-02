import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from model import Category

class IndexHandler(webapp.RequestHandler):
    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.tpl_vars = {}
        
    def get(self):
        current_category_key = self.request.get('category')
        current_category = None
        lineage = []
        
        try:
            current_category = Category.get(db.Key(current_category_key))
            lineage = [Category.get(key) for key in current_category.lineage]
        except db.BadKeyError:
            pass
        except AttributeError:
            pass
        
        child_categories = Category.children(current_category)
        self.tpl_vars['current_category'] = current_category
        self.tpl_vars['child_categories'] = child_categories
        self.tpl_vars['lineage'] = lineage
        path = os.path.join(os.path.dirname(__file__), 'templates/admin/index.html')
        self.response.out.write(template.render(path, self.tpl_vars))

    def post(self):
        parent_key = self.request.get('parent_key')
        name = self.request.get('category_name')
        
        if len(name) < 3:
            pass #no feedback, as of now
        else:
            try:
                parent = Category.get(db.Key(parent_key))
                Category.new(name,parent)
            except db.BadKeyError:
                pass #no feedback, as of now
            except:
                pass #no feedback, as of now
                
        self.redirect('./?category=' + parent_key)

#script level
application = webapp.WSGIApplication([(r'/admin/',IndexHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

