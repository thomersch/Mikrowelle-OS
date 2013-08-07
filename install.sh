#!/bin/sh

pip install -U virtualenv
virtualenv mw_os_python
source mw_os_python/bin/activate
./mw_os_python/bin/pip install lxml jinja2 markdown

git clone https://github.com/thomersch/Mikrowelle-OS.git