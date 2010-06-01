from tornado.contrib.easy_app import start, expose_get, expose_post

class MainHandler():
    target = r'/(\w+)'
    def get(self, name):
        self.write("Hello %s" % name)

@expose_get('/home/') 
def home(request):
    request.write("Homee")
        
start('app')