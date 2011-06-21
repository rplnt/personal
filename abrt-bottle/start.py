#! /usr/bin/python

import bottle
from bottle import route, error, run, template, static_file
import xml.dom.minidom
import requests

#data contains following variables
    #headers: dictionary that is sent with each requests' request as headers
    #server: url to the server (with port)
    #path: directory where static files are stored
import data

def fetch_data(url):
    """
    Download and create xml tree from given url.
    Returns dom or None.
    """
    try:
        resp = requests.get(url, headers=data.headers)
    except:
        return None

    if resp.status_code is 200:
        return xml.dom.minidom.parseString(resp.content)

    return None



def api_root(doc, rt={}):
    if doc.childNodes:
        root = doc.childNodes[0]

    for node in root.childNodes:
         if node.nodeName == 'link':
            key = node.attributes['rel'].nodeValue
            value = node.attributes['href'].nodeValue
            rt[key] = value

    return rt



def api_details(doc, rt={}):
    """
    Parses one-level-deep XML into dictionary.
    """
    if doc.childNodes:
        root = doc.childNodes[0]

    for node in root.childNodes:
        if node.nodeName == 'item' and node.attributes['type'].nodeValue == 'txt':
            key = node.attributes['name'].nodeValue
            value = node.childNodes[0].nodeValue
            rt[key] = value

    return rt

            

    
def api_problems(doc, rt=[]):
    """
    Parses /problems' XML into list of tuples.
    """
    if doc.childNodes and doc.childNodes[0].nodeName == 'problems':
        for problem in doc.childNodes[0].childNodes:
            if problem.nodeName == 'problem':
                id = problem.attributes['id'].nodeValue
                time = problem.childNodes[1].childNodes[0].nodeValue
                reason = problem.childNodes[3].childNodes[0].nodeValue
                rt.append((id, time, reason))

    return rt



def bind_routes():
    """
    route request
    """
    @route('/')
    def root():
        content = fetch_data(data.server+'/')
        if content is None:
            return template('error.tpl', text='foo')
        else:
            return template('api_root.tpl', api=api_root(content))


    @route('/problems')
    def problems():
        content = fetch_data(data.server+'/problems/')
        if content is None:
            return template('error.tpl', text='foo2')
        else:
            return template('api_problems.tpl', api=api_problems(content,[]))


    @route('/problems/:id')
    def problem_details(id):
        content = fetch_data(data.server+'/problems/'+id)
        if content is None:
            return template('error.tpl', text='foo3')
        else:
            return template('api_details.tpl', api=api_details(content), pid=id)


    @route('/delete/:id')
    def del_problem(id):
        resp = requests.delete(data.server+'/problems/'+id, headers=data.headers)
        if resp.status_code is 200:
            return template('api_problems.tpl', text='problem deleted')
        else:
            return template('error.tpl', text='boo')


    @route('/static/:path')
    def serve_static(path):
        return static_file(path, root=data.path)

    
    @error(404)
    def error404(error):
        return template('error.tpl', text='404 Not Found')

    


if __name__ == '__main__':
    bind_routes()
    bottle.debug(True)
    run(host='localhost', port=8080, reloader=True)
