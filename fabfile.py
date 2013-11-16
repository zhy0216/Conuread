# -*- coding: utf-8 -*-

import os
import logging

from fabric.api import local
from fabric.context_managers import lcd

_warn = logging.warn
CURRENT_PATH = os.path.join(os.getcwd(),os.path.dirname(__file__))

def cleaning():
    """Delete all pyc and *.orig files in project directories."""
    local("find . -name '*.orig' -exec rm -i {} \;")
    local("find . -type f -name '*.pyc' -exec rm {} \;")

def update_req():
    """Updating requirements for pip"""
    # check whether in virtualenv
    if not os.environ.get("VIRTUAL_ENV"):
        _warn("You are not in an Virtualenv, please activate it first")
        return
    local("pip freeze|grep -v distribute > %s/pip_requirements.txt" % CURRENT_PATH)

def test():
    """Run nose test"""
    import os
    import sys
    lastone = os.path.split(CURRENT_PATH)[0]
    with lcd("unittests"):
        local("nosetests --nocapture --with-path=%s --with-path=%s"%(lastone,CURRENT_PATH))
    
    
def coverage():
    """Run nose test with coverage"""
    local("nosetests --with-coverage --cover-package=botan")

    
    
    
