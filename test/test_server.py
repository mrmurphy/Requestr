from nose.tools import *
from server import app

"""
Here are the testing crieteria:
POST /entry/ffff/3456 http/1.1      # should return a 200 OK response
POST /entry/ http/1.1       # should return 400 BAD REQUEST
POST /entry/12 http/1.1     # should return 400 BAD REQUEST
POST /entry/12/qqqq http/1.1    # 200 OK, 'qqqq' stored under '12' internally
GET /entry/ffff http/1.1        # 200 OK,
                                    with '3456' in the body of the response
GET /entry/fffe http/1.1        # should return 404 NOT FOUND
GET /entry/ http/1.1     # 200 OK, with either
                            '12 -> qqqq' or 'ffff -> 3456' as the body
POST /entry/zz/zyx http/1.1     # 200 OK
POST /entry/az/zyx http/1.1     # 200 OK
POST /entry/34/zyx http/1.1     # 200 OK
POST /entry/AF/zyx http/1.1     # 200 OK
POST /entry/zez/zyx http/1.1    # 200 OK
GET /list/0 http/1.1       # 200 OK, body is
                            ffff -> 3456
                            12 -> qqqq
                            zz -> zyx
                            az -> zyx
GET /list/1 http/1.1      # 200 OK, body is
                            34 -> zyx
                            AF -> zyx
                            zez -> zyx
"""


class TestCode():
    def test_POST_valid1(self):
        r = app.request('/entry/ffff/3456', method='POST')
        assert_equal(r.status, '200 OK')

    def test_POST_empty(self):
        r = app.request('/entry/', method='POST')
        assert_equal(r.status, '400 BAD REQUEST')

    def test_POST_keyonly(self):
        r = app.request('/entry/12', method='POST')
        assert_equal(r.status, '400 BAD REQUEST')

    def test_POST_valid2(self):
        r = app.request('/entry/12/qqqq', method='POST')
        assert_equal(r.status, '200 OK')

    def test_GET_valid1(self):
        r = app.request('/entry/ffff/3456', method='POST')
        r = app.request('/entry/ffff')
        assert_equal(r.status, '200 OK')
        ok_('3456' in r.data)

    def test_GET_notfount1(self):
        r = app.request('/entry/fffe')
        assert_equal(r.status, '404 Not Found')

    def test_GET_random(self):
        r = app.request('/entry/ffff/3456', method='POST')
        r = app.request('/entry/12/qqqq', method='POST')
        r = app.request('/entry/')
        assert_equal(r.status, '200 OK')
        ok_('12 -> qqqq' in r.data or 'ffff -> 3456' in r.data)
        r = app.request('/entry')
        assert_equal(r.status, '200 OK')
        ok_('12 -> qqqq' in r.data or 'ffff -> 3456' in r.data)

    def test_POST_and_GET_list(self):
        r = app.request('/entry/ffff/3456', method='POST')
        r = app.request('/entry/12/qqqq', method='POST')
        r = app.request('/entry/zz/zyx', method='POST')
        r = app.request('/entry/az/zyx', method='POST')
        r = app.request('/entry/34/zyx', method='POST')
        r = app.request('/entry/AF/zyx', method='POST')
        r = app.request('/entry/zez/zyx', method='POST')
        r = app.request('/list/0')
        assert_equal(r.status, '200 OK')
        assert_equal(r.data,
                     "ffff -> 3456\n" +
                     "12 -> qqqq\n" +
                     "zz -> zyx\n" +
                     "az -> zyx")
        r = app.request('/list/1')
        assert_equal(r.status, '200 OK')
        assert_equal(r.data,
                     "34 -> zyx\n" +
                     "AF -> zyx\n" +
                     "zez -> zyx")
