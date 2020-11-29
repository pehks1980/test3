import unittest

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """

        app = web.Application()
        #app.router.add_get('/', hello)
        print (app)
        return app

    # the unittest_run_loop decorator can be used in tandem with
    # the AioHTTPTestCase to simplify running
    # tests that are asynchronous
    @unittest_run_loop
    async def test_example(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200
        text = await resp.text()
        assert "Hello, world" in text

    # a vanilla example
    def test_example_vanilla(self):
        async def test_get_route():
            url = "/"
            resp = await self.client.request("GET", url)
            assert resp.status == 200
            text = await resp.text()
            assert "Hello, world" in text

        self.loop.run_until_complete(test_get_route())

# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
