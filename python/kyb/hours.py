#!/usr/bin/python

from commons import *
import re


node = ''


#upload data to server
def post_data(data):
    opener,login_data = prepare_login()
    post_data = urllib.urlencode({'node_content' : data, 'event' : 'configure_content'})
    try:
        opener.open(server, login_data,5)
        time.sleep(0.5)
        page = opener.open(server+node, post_data,8)
    except IOError:
        print date_now+' ERROR: Could not open connection: ', IOError
        sys.exit(1)
    do_logout(opener)



#load data from database
def load_data():
    c = conn.cursor()
    c.execute('select max(date_id) from visits')
    latest, = c.fetchone()
    #seriously?
    latest = latest-15
    latest = latest,
    result = c.execute('select id,visits from visits where date_id>?',latest).fetchall()
    c.close()

    return sum_visitors(result,True)
    


#retrieve names from database
def get_names(data):
    c = conn.cursor()

    result = {}
    for path,count in data.items():
        t = path,
        c.execute('select name from dict where id=?',t)
        name, = c.fetchone()
        result[path] = [name,count]
    c.close()

    return result

def dict2str(data):
    result = re.sub('\[u\'','[\'',str(data))
    result = u''+re.sub('\[u\"','["',result)
    return result


#prepare data to be posted (there shall be some magic)
def prepare_data(entry_data): #id:count dictionary
    #some magic here
    data = {}
    for path,count in entry_data.items():
        count = count/15
        if count > 0:
            data[path] = count

    result = get_names(data)
    return dict2str(result)



#I just like this color
def main():
    db_content = load_data()
    to_upload = prepare_data(db_content)
    post_data(to_upload)
    print date_now+' SUCCESS: hourly results were updated!'



if __name__ == '__main__':
    main()

