#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import inspect, new
import tornado.web

def expose_get(url):
    def wrap(f):
        def wrapped_f(*args):
            f(*args)
        wrapped_f.method = 'get'
        wrapped_f.url = url
        return wrapped_f
    return wrap

def expose_post(url):
    def wrap(f):
        def wrapped_f(*args):
            f(*args)
        wrapped_f.method = 'post'
        wrapped_f.url = url
        return wrapped_f
    return wrap

def start_class(obj):
    handlers = []
    obj = obj()
    for name in dir(obj):
        if name[0:2] == '__'  or not callable(getattr(obj, name)):
            continue
        func = getattr(obj, name)
        if func.__name__ != expose_post.__name__ and  func.__name__ != expose_get.__name__:
            _name = "Handler-" + func.url
            methods_dict = { func.method : func }
            _class = new.classobj(name,(tornado.web.EasyRequestHandler, ), methods_dict)
            handlers.append((func.url, _class))
    return handlers

def start_module(mod_name):
    handlers = []
    mod = __import__(mod_name)
    for name in dir(mod):
        obj = getattr(mod, name)
        if inspect.isclass(obj):
            obj.__bases__ =  (tornado.web.RequestHandler,)
            handlers.append((obj.target, obj))
        if inspect.isfunction(obj):
            if obj.__name__ != expose_post.__name__ and  obj.__name__ != expose_get.__name__ and obj.__name__ != 'start':
                _name = "Handler-" + obj.url
                methods_dict = { obj.method : obj }
                _class = new.classobj(name,(tornado.web.RequestHandler, ), methods_dict)
                handlers.append((obj.url, _class))
    return handlers
 
def start(obj, settings, port=8888):
    handlers = []
    if inspect.isclass(obj):
        handlers = start_class(obj)
    else:
        handlers = start_module(obj)
                    
    application = tornado.web.Application(handlers, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

