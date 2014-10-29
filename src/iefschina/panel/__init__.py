# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .channel import Navi, Channel
from .article import Slide, Article

from flask.ext.admin import Admin


admin = Admin(name='后台管理', url='/trade')


# 频道管理
admin.add_view(Navi(name='导航栏', category='频道管理', endpoint='navi'))
admin.add_view(Channel(name='频道项', category='频道管理', endpoint='channel'))


# 文章管理
admin.add_view(Slide(name='幻灯片', category='文章管理', endpoint='slide'))
admin.add_view(Article(name='文章', category='文章管理', endpoint='article'))