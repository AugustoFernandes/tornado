from tornado.contrib.easy_app import start, expose_get, expose_post
import os, datetime

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

class WikiPage():
    def __init__(self, id, content, parent=None):
        self.id = id
        self.content = content
        self.history = []
        self.last_modify = datetime.datetime.now()
        self.parent = parent

class Wiki():
    pages = {}
    
    def __init__(self):
        Wiki.pages['Teste'] = 'Pagina de Teste'
    
    @expose_get('/create')
    def page_create_page(self, tornado):
        tornado.render('templates/create_page.html')
    
    @expose_post('/post')
    def create_page(self, tornado):
        page = None
        wikipage = WikiPage(tornado.get_argument('name'), tornado.get_argument('content'), None)
        wikipage.last_modify = datetime.datetime.now()
        if wikipage.id in Wiki.pages:
            page = Wiki.pages[wikipage.id]
        if not page:
            Wiki.pages[wikipage.id] = wikipage
            
        tornado.redirect("/get/%s" % tornado.get_argument('name'))

    @expose_get('/get/(.+)')
    def get_page(self, id, tornado):
        if id in Wiki.pages:
            tornado.write(Wiki.pages[id])
        else:
            return None
        
start(Wiki, settings)