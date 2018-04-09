import tornado.web
import tornado.auth
import tornado.options
import tornado.escape
from itertools import chain
from sqlalchemy.orm import *
from db_objects import *
from serverconfig import serverconfig
import sys
import os
# import sqlalchemy.exc
import sqlalchemy.exc
class bookmarks_handler(tornado.web.RequestHandler):
    mycfg = serverconfig()
    engine = create_engine(''.join(
        chain(*mycfg['dbconfig']['sqltype'], '://', mycfg['dbconfig']['user'], ':', mycfg['dbconfig']['pwd'], '@',
              mycfg['dbconfig']['host'], '/', mycfg['dbconfig']['dbname'])))
    def pagerender(self, UserID, bookmark_session):
        bookmarks = bookmark_session.query(Bookmarks.Url, Bookmarks.keywords, Bookmarks.Last_visited, Bookmarks.Screen_path).filter(Bookmarks.UserID == UserID).all()
        categories = bookmark_session.query(Categories.Categorie_name).filter(Categories.UserID == UserID).all()
        # for row in bookmarks:
        #     print('row', row)
        self.render("themes/default/html/bookmarks.html", bookmarks=bookmarks, categories=categories)
    def get(self):
        email = self.get_secure_cookie("user")
        SessionID = self.get_secure_cookie("SessionID")  # Type binary
        bookmark_session = sessionmaker()
        bookmark_session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)
        bookmark_session = bookmark_session()  # Instancing the result of sessionmaker()
        try:
            UserState = bookmark_session.query(User_infos.UserState).filter(User_infos.User_Name == email).one()
            if UserState.UserState == 1:
                print('userstate')
                UserID = bookmark_session.query(User_infos.UserID).filter(User_infos.User_Name == email).one()
                # user_password = loginsession.query(Users.Password).filter(Users.UserID == UserID).one()
                if UserID.UserID:
                    print('userid')
                    Sql_SessionID = bookmark_session.query(Sessions.SessionID).filter(Sessions.UserID == UserID).one()
                    print('cookie sessionid', Sql_SessionID.SessionID)
                    # sleep(10)
                    if Sql_SessionID.SessionID == SessionID.decode('ascii'):
                        print('sessionid')
                        bookmark_session.close()
                        self.pagerender(UserID, bookmark_session)
                    else:
                        print('sessionid else')
                        path = os.getcwd()
                        content = ''
                        info = ''
                        self.redirect('/login')
                else:
                    print('userid else')
                    path = os.getcwd()
                    content = ''
                    info = ''
                    self.redirect('/login')
            else:
                print('userstate else')
                path = os.getcwd()
                content = ''
                info = ''
                self.redirect('/login')
        except:
            print(sys.exc_info())
            self.redirect('/login')
