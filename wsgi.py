# -*- coding: utf-8 -*-
from bottle import static_file

def application(environ,start_response):
    if environ['PATH_INFO'] == '/favicon.ico':
       return static_file('favicon.ico',root='./')
    
    data = '''
<head>
<style>
body{
margin: 0px;
}
</style>
</head>
<body>
<iframe border="0" frameborder="0" marginwidth="0" marginheight="0" width="100%" height="100%" src="http://man.jcloud.com/appengine/jae/hello.html">
</iframe>
</body>
</html>
'''
    start_response("200 OK",[
               ("Content-Type","text/html;charset=utf-8"),
               ("Content-Length",str(len(data)))
             ])
    return iter([data])
