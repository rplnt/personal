#!/usr/bin/python

import sys
import time
import urllib
import urllib2
import cookielib
import sqlite3 as sql


#global data
db = 'main.db'
server = ''
username = ''
password = '' #use cookie if possible
login = {'login' : username, 'password' : password, 'event' : 'login', 'login_type' : 'name'}
logout = {'event' : 'logout'}
date_now = time.strftime('%d. %m. %Y %H:%M:%S')
conn = sql.connect(db)



#just to remember db structure
def create_tables():
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS dict (id int primary key, name text)') #delete some sometime?
    c.execute('CREATE TABLE IF NOT EXISTS visits (date_id int, id int, visits int)') #sum to hours -> delete
    c.execute('CREATE TABLE IF NOT EXISTS dates (date_id int primary key, date text)') #4MB?
    c.execute('CREATE TABLE IF NOT EXISTS hours (date_id int, id int, visits)') #date id - first date id from given hour; sum to days -> delete
    conn.commit()
    c.close()



#will sum visitors and create dictionary; if multi is True seconf part of tuple is used instead of 1
def sum_visitors(data, multi=False):
    temp = {}
    for path,count in data:
        if not multi: count = 1
        if path in temp:
            temp[path] += count
        else:
            temp[path] = count

    return temp
    


#todo save connection data and use them
def prepare_login():
    cj = cookielib.CookieJar() #we don't really use this atm
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    login_handler = urllib.urlencode(login)
    
    return opener,login_handler
    


#todo - see prepare_login()
def do_logout(opener):
    time.sleep(0.25) #be nice to the allmighty kybca
    logout_data = urllib.urlencode(logout)
    try:
        opener.open(server,logout_data,3)
        opener.close()
    except IOError:
        print date_now+' WARNING: Could not logout: ', IOError

