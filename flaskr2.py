# -*- coding: utf-8 -*-
"""
    Flaskr2
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and mysql.

    :copyright: (c) 2019 by Roberson Young.
    :license: BSD, see LICENSE for more details.
"""

import os
import pymysql
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DB_NAME='flaskr2',
    DB_HOST='host.docker.internal',
    DB_USER='root',
    DB_PWD='rst2012',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    db = pymysql.connect(app.config['DB_HOST'], app.config['DB_USER'], app.config['DB_PWD'], app.config['DB_NAME'])
    return db


def init_db():
    """Initializes the database."""
    db = get_db()
    db.cursor().execute('DROP TABLE IF EXISTS entries')
    sql = """CREATE TABLE `entries` (
              `id` int NOT NULL AUTO_INCREMENT,
              `title` text NOT NULL,
              `text` text NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    db.cursor().execute(sql)


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select title, text from entries order by id desc')
    entries = cursor.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    if request.form['title'] == '':
        flash("title can't be empty")
        return redirect(url_for('show_entries'))
    if request.form['text'] == '':
        flash("content can't be empty")
        return redirect(url_for('show_entries'))
    db.cursor().execute("insert into entries (title, text) values ('%s', '%s')" % \
                        (request.form['title'], request.form['text']))
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
