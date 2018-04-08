import tornado.ioloop
import tornado.web
# import tornado.websocket
import tornado.auth
import tornado.options
import tornado.escape
import tornado.httpserver
import os
from login import login_handler
from serverconfig import serverconfig
import ssl
class bookmarks_handler(tornado.web.RequestHandler):
    def get(self):
        pass
# class Application(tornado.web.Application):
#     """
#     Main Class for this application holding everything together.
#     """
#     def __init__(self):
#         pass


class MyApp(tornado.web.Application):

    def __init__(self):
        # (r'/', useless),
        handlers = [
            (r"/login", login_handler),
            (r"/bookmarks", bookmarks_handler),
        ]
        # ssl_context = ssl.create_default_context()
        myconfig = serverconfig()
        # ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # ssl_ctx.load_cert_chain("selfsigned/cert.pem", "selfsigned/key.pem")
        settings = dict(
            cookie_secret= myconfig['global']['securekey'],
            # BAAAD, according to some devs, this cookie secret is as important as a ssl private key, so must be put outside of code
            login_url="/login",
            # template_path=os.path.join(os.path.dirname(__file__), "themes"),
            static_path=os.path.join(os.path.dirname(__file__), "themes"),
            xsrf_cookies=True,
            autoescape="xhtml_escape",
            # Set this to your desired database name.
            db_name='online_bookmark',
            # apptitle used as page title in the template.
            apptitle='Online bookmarks website',
            autoreload=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        # print(settings['template_path'])
        # print(settings)
# print
# 'static path', settings['static_path']
# Call super constructor.
# tornado.web.Application.__init__(self, handlers, **settings)


def main():
    """
    Main function to run the chat application.
    """

    # print('myconfig', myconfig.sections())
    # myapp.listenmyconfig['global']['port'])
    # This line will setup default options.
    # tornado.options.parse_command_line()
    # Create an instance of the main application.
    application = MyApp()
    myconfig = serverconfig()
    # print(myconfig['global']['port'])
    # Start application by listening to desired port and starting IOLoop.
    server = tornado.httpserver.HTTPServer(
        application,
        #There is no need to convert the certificate pem to another format, tornado handle it fine
        ssl_options={
            "certfile": "selfsigned/cert.pem",
            "keyfile": "selfsigned/key.pem"
            }
        )
    server.listen(myconfig['global']['port'])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()