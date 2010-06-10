from tornado.contrib.easy_app import start, expose_get, expose_post
from forms import LoginForm

class MainHandler():
    target = r'/main/(\w+)'
    def get(self, name):
        self.write("Hello %s" % name)
        
@expose_get('/test/(\w+)') 
def test(tornado, name):
    tornado.write(name)

@expose_get('/home/') 
def home(tornado):
    form = LoginForm()
    tornado.write('<form action="/homep" method="post">' +
                  form.as_p() +
                  '<input type="submit" value="ok"></form>')
    
@expose_post('/homep') 
def homep(tornado):
    form = LoginForm(tornado.request.arguments)
    if form.is_valid():
        tornado.write('<form action="/homep" method="post">' +
                  form.as_p() +
                  '<input type="submit" value="ok"></form>')
    else:
        tornado.write('<form action="/homep" method="post">' +
                  form.as_p() +
                  '<input type="submit" value="ok"></form>')
    
start(__name__)