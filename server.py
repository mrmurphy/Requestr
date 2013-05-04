#! /usr/bin/python
import web
import random
from collections import OrderedDict

urls = (
    '/entry/?([^/]*)/?([^/]*)', 'entry',
    '/list/?(\d*)', 'list',
)
app = web.application(urls, globals())
model = OrderedDict()


class entry:
    def GET(self, key, _):
        if not model.keys() or (key and not model.get(key)):
            return app.notfound()
        elif key:
            return model.get(key)
        else:
            randomkey = random.choice(model.keys())
            return "{key} -> {value}".format(key=randomkey,
                                             value=model[randomkey])

    def POST(self, key=None, value=None):
        for arg in (key, value):
            if not arg or len(arg) >= 128:
                raise web.HTTPError('400 BAD REQUEST')
        model[key] = value


class list:
    def GET(self, page=0):
        page = 0 if not page else page
        begindex = int(page)*4
        items = model.items()[begindex:begindex+4]
        return "\n".join(["{key} -> {value}".format(key=item[0], value=item[1])
                         for item in items])

if __name__ == "__main__":
    app.run()
