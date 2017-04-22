from pprint import pformat
from urllib.parse import parse_qsl

def simpleapp(environ, start_response):
    output = ["Hello, world!"]

    parse_q_string = parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'POST':
        output.append('POST  DATA:')
        output.append(pformat(environ['wsgi.input'].read().decode()))

    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            output.append('<p> GET DATA: </p>')
            for ch in parse_q_string:
                output.append(' = '.join(ch))
                output.append('<br>')

    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])
    string_output = "".join(output)
    byte_output = string_output.encode('utf-8')
    return [byte_output]
