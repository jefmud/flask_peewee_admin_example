# Simple Flask/FlaskAdmin/Peewee example
# illustrates CRUD database on PeeWee/Flask
import datetime

# third party library imports
from flask import Flask, redirect, render_template, request, session, url_for
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.peewee import ModelView
from peewee import *

# app boilerplate requirements (global)
app = Flask(__name__)
app.secret_key = 'thisIsASecret'
db = SqliteDatabase('simple.db')

class Contact(Model):
    # Contact database model
    uname = CharField(max_length=100, unique=True)
    fname = CharField(max_length=100)
    lname = CharField(max_length=100)
    email = CharField(max_length=100)
    phone = CharField(max_length=50)
    notes = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    
    def __repr__(self):
        return "{}, {}".format(self.lname, self.fname)
    
    class Meta:
        database = db
        
@app.route('/')
def index():
    """A simple text based response"""
    return "<strong>Hello World!</strong>  The time is {} <br /> Goto <a href='{}'>Home</a>".format(datetime.datetime.now(), url_for('home'))

@app.route('/home')
def home():
    """a home page with an example template derived from flask_admin"""
    return render_template('index.html',
                           title='Home',
                           content='Sample homepage content')

@app.route('/list')
def list():
    """A simple list (text based) response"""
    buf = []
    contacts = Contact.select()
    for contact in contacts:
        buf.append(str(contact))
    buf = '<br/>\n'.join(buf)
    return '<h1>Contact list</h1>\n{}'.format(buf)

@app.route('/login')
def login():
    """Simple login, only setting 'group' attibute"""
    session['username'] = 'admin'
    session['group'] = 'admin'
    return 'User is now logged in. Goto <a href="{}">Home Page</li>'.format(url_for('home'))

@app.route('/logout')
def logout():
    """Simple logout, only resetting 'group'"""
    session['username'] = None
    session['group'] = None
    return 'User is logged out. Goto <a href="{}">Home Page</li>'.format(url_for('home'))
    
class MyAdminIndexView(AdminIndexView):
    # overrides the default AdminIndexView, probably should use a template
    # for illustration, I kept it simple
    @expose('/')
    def index(self):
        return 'Click here to adminstrate Contacts <a href="/admin/contact">__contacts__</a>'
    
    def is_accessible(self):
        # admin only accessible to the admin user-group
        return session.get('group') == 'admin'
       
# Flask Admin views
admin = Admin(app, 'Admin Area', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(ModelView(Contact))

def load_sample_data():
    """load database with a few sample rows"""
    try: Contact.create(uname='alpha',fname='Aaron',lname='Alpha',email='aa@alpha.net',phone='none',notes='')
    except Exception as e: print(str(e))
    
    try: Contact.create(uname='beta',fname='Brett',lname='Beta',email='bb@beta.net',phone='none',notes='')
    except Exception as e: print(str(e))
    
    try: Contact.create(uname='charlie',fname='Cindy',lname='Charlie',email='cc@charley.net',phone='555-1212',notes='Nothing of note')
    except Exception as e: print(str(e))    
    
def init():
    """simple connection to database and initilization of data"""
    db.connect()
    db.create_tables([Contact],safe=True)
    
if __name__ == '__main__':
    init()
    load_sample_data()
    app.run(debug=False)