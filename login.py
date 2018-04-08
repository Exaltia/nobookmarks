from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
import tornado.ioloop
import os,sys
import tornado.web
from itertools import chain
import tornado.websocket
import tornado.auth
import tornado.options
import tornado.escape
from time import sleep
from serverconfig import serverconfig
from db_objects import *
from passlib.hash import pbkdf2_sha256
from time import time
import random
import string
from datetime import datetime

class login_handler(tornado.web.RequestHandler):
    mycfg = serverconfig()
    # db_parameters =
    # print(db_parameters)
    # print('in login.py', mycfg['global']['port'])
    print(''.join(chain(*mycfg['dbconfig']['sqltype'], '://', mycfg['dbconfig']['user'], ':', mycfg['dbconfig']['pwd'], '@', mycfg['dbconfig']['host'], '/', mycfg['dbconfig']['dbname'])))
    engine = create_engine(''.join(chain(*mycfg['dbconfig']['sqltype'], '://', mycfg['dbconfig']['user'], ':', mycfg['dbconfig']['pwd'], '@', mycfg['dbconfig']['host'], '/', mycfg['dbconfig']['dbname'])))
    def post(self):
        if self.get_arguments('create'):
            try:
                email = self.get_arguments('email')
                pwd = self.get_arguments('password')
                first_name = self.get_arguments('first_name')
                last_name = self.get_arguments('last_name')
                address = self.get_arguments('address')
                postal_code = self.get_arguments('postal_code')
                state = self.get_arguments('state')
                country = self.get_arguments('country')
                # pwd =
                print('pwd', pwd)
                # sleep(10)
                #Do not forget that we get a tuple from self.get_arguments
                pwd = pbkdf2_sha256.encrypt(pwd[0], rounds=2000000, salt_size=16) #variable overwritten to be sure it won't stay in memory

                user_infos = User_infos(User_Name=email, First_name=first_name, Last_name=last_name, Address=address, Postal_code=postal_code, State=state, Country=country, Plan=0, UserState=2)
                # Plan = 0
                # user.plan = Plan
                db_user_create = sessionmaker()
                db_user_create.configure(bind=self.engine)
                Base.metadata.create_all(self.engine)
                db_user_create = db_user_create() #Instancing the result of sessionmaker()
                db_user_create.add(user_infos)
                # loginsession.
                db_user_create.flush()
                User_ID = db_user_create.query(User_infos.UserID).filter(User_infos.User_Name == email).one()
                # print(User_ID.getvalue())
                User_ID = Users(UserID=User_ID, Password=pwd)
                print('User ID', User_ID)
                db_user_create.add(User_ID)
                db_user_create.commit()
                db_user_create.close()
                info = 'User creation successfull, you can login'
                self.render('themes/default/html/index.html', content='', info=info)
            except:
                print('except pwd', pwd)
                info = 'User creation failed'
                print(sys.exc_info())
                self.render('themes/default/html/index.html', content='', info=info)
        else:
            email = self.get_arguments('email')
            pwd = self.get_arguments('password')
            loginsession = sessionmaker()
            loginsession.configure(bind=self.engine)
            Base.metadata.create_all(self.engine)
            loginsession = loginsession() #Instancing the result of sessionmaker()
            UserState = loginsession.query(User_infos.UserState).filter(User_infos.User_Name == email).one()
            UserID = loginsession.query(User_infos.UserID).filter(User_infos.User_Name == email).one()
            user_password = loginsession.query(Users.Password).filter(Users.UserID == UserID).one()
            # Do not forget that we get a tuple from self.get_arguments
            # print(user_password.Password)
            # pwd[0] = pbkdf2_sha256.encrypt(pwd[0], rounds=2000000, salt_size=16)
            # print(pwd[0])
            # sleep(10)
            result = pbkdf2_sha256.verify(pwd[0], user_password.Password) #result is True or False
            print('result', result, UserState)
            if UserState[0] == 1:
                if result:
                    SessionID = ''.join(random.choice(string.ascii_uppercase) for i in range(64))
                    SessionDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    Session_Infos = Sessions(UserID=UserID, SessionID=SessionID, SessionDate=SessionDate)
                    session_db = sessionmaker()
                    session_db.configure(bind=self.engine)
                    Base.metadata.create_all(self.engine)
                    session_db = session_db()  # Instancing the result of sessionmaker()
                    session_db.add(Session_Infos)
                    session_db.commit()
                    session_db.close()
                    domain = self.request.host #We need a domain name for the secure cookie
                    # domain = domain.split('.')
                    # domain = domain[1] + '.' + domain[2]
                    if ':' in domain:
                        domain = domain.split(':')
                        domain = domain[0]
                    print(domain)
                    print(email[0])
                    self.set_secure_cookie("user", email[0], domain=domain)
                    self.set_secure_cookie("SessionID", SessionID, domain=domain)
                    self.redirect('/bookmarks')
                else:
                    self.send_error(401)
            else:
                self.send_error(401)
            # print('credentials,', email, pwd)
    def get(self):
        path = os.getcwd()
        content = ''
        info = ''
        self.render("themes/default/html/index.html", info=info, path=path, content=content)