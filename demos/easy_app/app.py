from tornado.contrib.easy_app import start, expose_get, expose_post

class MainHandler():
    target = r'/(\w+)'
    def get(self, name):
        self.write("Hello %s" % name)
        
@expose_get('/test/(\w+)') 
def test(tornado, name):
    tornado.write(name)

@expose_get('/home/') 
def home(tornado):
    tornado.write("Homee")
    
start(__name__)