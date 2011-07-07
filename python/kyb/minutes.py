#!/usr/bin/python

import re
from commons import *
from xml.dom import minidom



#local data
run_node = ''
unwanted = [4830026 , 3777728 , 2176597 , 3660841 , 1522695 , 1569351 , 788016 , 3579407, 4944422, 1603607]


#create logged in handler
def download():
    opener,login_data = prepare_login()
    try:
        page = opener.open(server+run_node, login_data,5)
        result = page.read()
    except IOError:
        print date_now+' ERROR: Could not open connection: ', IOError
        sys.exit(1)
    
    do_logout(opener)

    return result



#download page
def fetch():
    result = download()

    #get out relevant data (if any)
    data = re.search(r'(<nodes>.*?</nodes>)',result)
    if not data:
        print date_now+' ERROR: No valid data found in file.'
        sys.exit(2)
    
    return data.group(0)



#discard commonly populated nodes
def discard_unwanted(nodes):
    result = []
    for item in nodes:
        #  stupid nodes           system nodes     bookmarks                         counted 3x
        if item[0] in unwanted or item[0] < 100 or item[1][:5].lower() == 'bookm' or item[2]>15:
            pass #print 'discarded ',item
        else:
            result.append((item[0],item[1]))
    del nodes
    return result



#parse xml into list of tuples
def parse(data):
    try:
        xml_tree = minidom.parseString(data)
    except:
        print date_now+' ERROR: _probably_ failed to parse data'
        sys.exit(3)
    
    nodes = []
    root = xml_tree.documentElement
    for node in root.childNodes:
        node_id = int(node.getAttribute('path'))
        idle_m  = int(node.getAttribute('idlemin'))
        try:
            node_name = node.childNodes[0].nodeValue
        except IndexError:
            node_name = ' '
        nodes.append((node_id,node_name,idle_m))

    return discard_unwanted(nodes)

        
    
#update id:name dictionary
def update(data):
    c = conn.cursor()
    for i,t in data:
        t = t.replace("\\'",'&#39;')
        x = i,t
        c.execute('insert or replace into dict values (?,?)', x)
    conn.commit()
    c.close()
        

#save counts to db
def save(data):
    summed = sum_visitors(data)

    c = conn.cursor()
    c.execute('insert into dates values (null,?)',[date_now])
    last_id = c.lastrowid+1
    for path,count in summed.items():
        t = last_id,path,count
        c.execute('insert into visits values (?,?,?)',t)
    conn.commit()
    

# __main__
def main():
    result = parse(fetch())
    update(result)
    save(result)
    
    print date_now+' SUCCESS: minutes.py has done its job!'



if __name__ == '__main__':
    main()

