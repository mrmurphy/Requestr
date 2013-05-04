#! /usr/bin/python
import web
import random
from collections import OrderedDict

urls = (
    '/entry/(.+)/(.+)', 'entry',
    '/entry/(.+)', 'entry',
    '/entry/', 'entry',
    '/entry', 'entry',
    '/list/(\d*)', 'list',
    '/list', 'list'
)
app = web.application(urls, globals())
model = OrderedDict()


class entry:
    def GET(self, key=None):
        # Test if no key was specified, return a random entry.
        if not key:
            if not model.keys():
                return app.notfound()
            randomkey = random.choice(model.keys())
            return "{key} -> {value}".format(key=randomkey,
                                             value=model[randomkey])

        # A key was specified, look for it in the model.
        response = model.get(key)
        if response:
            return response
        else:
            return app.notfound()

    def POST(self, key=None, value=None):
        if not self.validate(key, value):
            raise web.HTTPError('400 BAD REQUEST')

        model[key] = value

    def validate(self, *args):
        for arg in args:
            if not arg or len(arg) >= 128:
                return False
        return True


class list:
    def GET(self, page=0):
        page = 0 if not page else page
        retstrings = []
        for i in xrange(0, 4):
            index = int(page) * 4 + i
            if index < len(model.items()):
                item = model.items()[index]
                retstrings.append("{key} -> {value}".format(
                    key=item[0], value=item[1]))
        return "\n".join(retstrings)


if __name__ == "__main__":
    app.run()
