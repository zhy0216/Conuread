import requests


# http://stackoverflow.com/a/5776659/847357
# http://s2.googleusercontent.com/s2/favicons?domain_url=



def get_favicon(domain_url, filename="test"):
    r = requests.get('http://s2.googleusercontent.com/s2/favicons?domain_url=%s'%domain_url,
                     stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(128):
            fd.write(chunk)

