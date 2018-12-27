# Flask Applications the SciComp Way

<!--
The table of contents (TOC) below is automatically generated
(at least on dtenenba's computer) by a pre-commit hook.
Don't edit the TOC or the comments above or below it.
If you want to set this up yourself, see
https://www.npmjs.com/package/markdown-toc
to install the code, then do this:

    touch .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit

then edit .git/hooks/pre-commit to contain this:

#!/bin/bash

node ~/node_modules/markdown-toc/cli.js -i FULL_PATH_TO/README.md
git add FULL_PATH_TO/README.md

-->

<!-- toc -->

- [What is supported/required?](#what-is-supportedrequired)
  * [Python 3](#python-3)
  * [Virtual Environments](#virtual-environments)
  * [Unit Tests](#unit-tests)
  * [Database Access](#database-access)
    + [Which RDBMS should I use?](#which-rdbms-should-i-use)
  * [REST Access](#rest-access)
  * [Other Supported/Recommended Modules](#other-supportedrecommended-modules)
  * [Web Servers](#web-servers)
  * [SSL (https)](#ssl-https)
  * [Interacting with the gizmo cluster](#interacting-with-the-gizmo-cluster)
  * [My app needs to call some R code](#my-app-needs-to-call-some-r-code)
  * [Secrets Management](#secrets-management)
  * [Does your app use PHI?](#does-your-app-use-phi)
  * [Use GitHub for version control](#use-github-for-version-control)
  * [Helpful Tools for code development](#helpful-tools-for-code-development)
    + [Linters](#linters)
    + [Profiling](#profiling)
  * [Continuous Integration (CI)](#continuous-integration-ci)

<!-- tocstop -->

Use these templates to build your own
[Flask](http://flask.pocoo.org/) application in
a way that will be supported by
[SciComp](https://teams.fhcrc.org/sites/citwiki/SciComp/Pages/Home.aspx?TreeField=Wiki_x0020_Page_x0020_Categories).

## What is supported/required?

### Python 3

Python 3 was released in 2008 and Python 3.x should be used for all
new projects. If you have an existing Python 2 codebase, contact
SciComp for help with porting it to Python 3.

### Virtual Environments

Use [Pipenv](https://pipenv.readthedocs.io/en/latest/) to manage the virtual environment for this project.
If `pipenv` is not installed, [install it](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv).

The first time you clone the repository, 
create the virtual environment and install
the dependencies with this command:

```
pipenv install
```

Before each session of working with this app,
activate the virtual environment in your current shell
with:

```
pipenv shell
```




### Unit Tests

Flask makes it easy to add unit tests to your application.
Unit tests give you confidence that your app works the way
it's supposed to.

Every route in a Flask app should have at least one unit test.

### Database Access

For most new applications, we recommend
[SQLAlchemy](http://www.sqlalchemy.org/), which provides
an Object-Relational Mapper (ORM) for Python.

There are some cases where using an ORM is overkill
and you just need to run some simple queries.
In these cases, you can use the
[DB API](https://wiki.python.org/moin/DatabaseInterfaces)
module for your RDBMS (MySQL, PostgreSQL, sqlite).
When using these low-level modules,
you must always write code in such a way as to avoid
[SQL injection](https://en.wikipedia.org/wiki/SQL_injection).
For example, **never do this**:

```python
# Never do this -- insecure!
symbol = 'RHAT' # assume this comes from a form or other untrusted source
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
```

Instead do this:

```python
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
```

#### Which RDBMS should I use?

PostgreSQL is the main supported RDBMS. You may use sqlite3 just
for testing and development(??), but in production you should use
PostgreSQL.

For PostgreSQL, use [myDB](https://mydb.fredhutch.org). If your app lives
outside the Hutch network, use
[Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/).

If you need to use a NoSQL database, use
[MongoDB](https://www.mongodb.com/) and the
[PyMongo](https://api.mongodb.com/python/current/) module.




### REST Access

If your application is meant to expose a service that other
code can consume, use the
[Flast-RESTful](https://flask-restful-cn.readthedocs.io/en/0.3.5/)
module.

### Other Supported/Recommended Modules

(??)

* [SciPy](https://www.scipy.org/)
* [NumPy](http://www.numpy.org/)
* [pandas](http://pandas.pydata.org/)
* ??


### Web Servers

TODO fill this in

* Flask development server - pros & cons
* gunicorn
* apache and nginx via WSGI


### SSL (https)

It's recommended that your web app only be accessible via
SSL (the HTTPS protocol). If your web app will use a `fredhutch.org`
or `fhcrc.org` domain, contact `SciComp` for help setting this up.
If you'll be using an external domain name, consider using
[Let's Encrypt](https://letsencrypt.org/) to set up your
SSL certificates.

### Interacting with the gizmo cluster

?? Do we need this section ?? Are flask apps allowed to submit jobs
to the cluster ??

### My app needs to call some R code

We recommend that you port the R code to Python.

(??)


### Secrets Management

FIXME add to this

### Does your app use PHI?

FIXME add to this



### Use GitHub for version control

Store your code in a GitHub repository (ADD MORE HERE)

### Helpful Tools for code development

#### Linters

We strongly recommend using `linters` when developing
Python code. Linters such as `pylint`, `pyflakes`,
and `flake8` (which combines the first two) will point
out syntactic, stylistic, logical, and many other issues
with your code. Ideally, code should be free of linting
warnings before it's committed to Git.

The [Atom](https://atom.io/) text editor has add-on packages
which enable linting right inside your editing window.

#### Profiling

[Profiling](https://docs.python.org/2/library/profile.html)
helps you find the parts of your code that run slowly and
can be optimized.

### Continuous Integration (CI)

Use [Travis CI](https://travis-ci.org) or
[circleci](https://circleci.com/) to automate the testing
and deployment of your code.

(should we require CI? we can at least illustrate it by
example in this repository)
