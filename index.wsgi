# coding: UTF-8
import os

import sae
import web

web.config.debug = True

from weixinInterface import WeixinInterface
#from oauth import Oauth
urls = (
'/','WeixinInterface',
'/oauth','Oauth'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)

