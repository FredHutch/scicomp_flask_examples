"""
A trivial web app intended to illustrate the use
of flask_login for logging in and out.
For the most part, I just followed the documentation at
https://flask-login.readthedocs.io/en/latest/
when writing this; but there were a few missing
bits of information (see
https://github.com/maxcountryman/flask-login/issues/349)
which I have expanded on in comments below.
"""

# standard library imports
from urllib.parse import urlparse, urljoin

# third-party imports
from flask_login import (LoginManager, UserMixin, login_user, current_user,
                         logout_user, login_required)
from flask import (Flask, redirect, render_template, url_for,
                   flash, request, abort)
from flask_wtf import Form

# Some examples online use Required but that's deprecated:
from wtforms.validators import DataRequired

# Some examples online show these being imported from flask_wtf
# but in recent versions, all *Field types should be imported from
# wtforms.
from wtforms import TextField, PasswordField, HiddenField


app = Flask(__name__) # pylint: disable=invalid-name

# In a 'real', nontrivial app, you would NOT hardcode the next
# two values. Instead, see the README about secrets management.
app.config['WTF_CSRF_SECRET_KEY'] = 'a random stringsdslkdjfjldkghlfkj'
app.secret_key = 'dsjhglfkjghflkjhflgfhlkj'


def is_safe_url(target):
    """
    A helper method to ensure that the 'next' url
    passed in (when the user requests a page that requires
    authentication) is relative to our site/app.
    See http://flask.pocoo.org/snippets/62/
    for more information.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


class LoginForm(Form):
    """
    Login form. Derived from an example at
    https://wtforms.readthedocs.io/en/latest/crash_course.html
    """
    username = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    nexturl = HiddenField('next')

    def __init__(self, *args, **kwargs):
        """Constructor. Not used???"""
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """Validate form contents."""
        print("errors are\n{}".format(self.errors))
        if not Form.validate(self):
            print("validation failed")
            return False

        # In this trivial app, a login is valid if
        # 1) the username and password fields are not empty, and
        # 2), the password is the username backwards.
        if self.username.data == self.password.data[::-1]:
            self.user = UserMixin()
            self.user.id = self.username.data
            users[self.user.id] = self.user
            print("we are good")
            # The `remember` flag means our app will remember
            # users even if they close their browser. It uses
            # cookies to accomplish this.
            login_user(self.user, remember=True)
            print("current_user: {}".format(current_user.get_id()))
            return True
        print("invalid password")
        # See this link for why the following pattern is necessary:
        # https://stackoverflow.com/questions/22889295/flask-self-errors-append-attributeerror-tuple-object-has-no-attribute-ap#comment74244200_22889381
        errorlist = list(self.username.errors) # issue
        errorlist.append('Invalid password')
        self.username.errors = errorlist
        flash('invalid passwird')
        print(self.username.errors)
        return False



login_manager = LoginManager() # pylint: disable=invalid-name
login_manager.init_app(app)
login_manager.login_view = "login"
users = {} # pylint: disable=invalid-name

@app.route('/')
def hello_world():
    """
    A simple route. This is where you go by default after authenticating.
    But this route does not require authentication.
    """
    return render_template("index.html")

@app.route('/logout')
def logout():
    """
    Route for logging out.
    """
    logout_user()
    return redirect(url_for('hello_world'))

@login_manager.user_loader
def load_user(user_id):
    """
    Function required by flask_login to load the logged-in user
    from the user 'store'. In this case the 'store' is a non-persistent
    dictionary, in a real app it would be a SQLAlchemy model or
    something similar.
    """
    if user_id in users:
        return users[user_id]
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    The /login route. When called with the 'GET' method it
    shows the login form; when called with POST it tries to
    log you in.
    """
    form = LoginForm()
    if request.method == 'GET':
        # The 'next' parameter does not automatically
        # make it from the GET to the POST, so we have
        # a hidden form element that we populate here:
        form.nexturl.data = request.args.get('next')
    if form.validate_on_submit():
        flash('Logged in successfully')

        nexturl = form.nexturl.data
        print("next is {}".format(nexturl))
        if nexturl:
            if is_safe_url(nexturl):
                return redirect(nexturl)
            return abort(400)
        return redirect(url_for("hello_world"))
    return render_template('login.html', form=form)

@app.route('/settings')
@login_required
def settings():
    """
    An example of a route that requires authentication.
    If you go here without being authenticated, the login
    view is shown, and the 'next' parameter & its value
    are added to the URL.
    """
    return 'secret sauce!'
