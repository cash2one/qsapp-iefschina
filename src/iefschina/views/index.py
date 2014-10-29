# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request, views, render_template

import re
from studio.core.engines import db
from iefschina.blueprints import blueprint_www
from iefschina.models import (ChannelModel, ChannelSummaryModel,
                              ArticleModel, ArticleContentModel)


class WelcomeView(views.MethodView):
    '''
        欢迎页
    '''

    def get(self):
        return render_template('www/welcome.html')


blueprint_www.add_url_rule('/', view_func=WelcomeView.as_view(b'welcome'),
                                endpoint='welcome', methods=['GET'])


class IndexView(views.MethodView):
    '''
        首页
    '''

    def get(self, language):
        channels = ChannelModel.query.all()
        if language=='en':
            channels = filter(lambda x: re.match(r'[a-zA-Z\b]+', x.name),
                              channels)
        else:
            channels = filter(lambda x: not re.match(r'[a-zA-Z\b]+', x.name),
                              channels)
        return render_template('www/index.html', channels=channels)


blueprint_www.add_url_rule('/l/<language>/',
                            view_func=IndexView.as_view(b'index'),
                            endpoint='index', methods=['GET'])


class SearchView(views.MethodView):
    '''
        搜索
    '''

    def _search(self, kw):
        channels = (ChannelModel.query
                                .join('_summary')
                                .filter(db.or_(ChannelModel.name.like('%'+kw+'%'),
                                               ChannelSummaryModel.content.like('%'+kw+'%')))
                                .all())
        articles = (ArticleModel.query
                                .join('_content')
                                .filter(db.or_(ArticleModel.title.like('%'+kw+'%'),
                                               ArticleContentModel.content.like('%'+kw+'%')))
                                .all())

        return channels+articles

    def get(self, category):
        kw = request.args.get('kw', '')
        result = self._search(kw) if kw else []
        return render_template('www/search.html', kw=kw, result=result)

blueprint_www.add_url_rule('/search/<category>/',
                            view_func=SearchView.as_view(b'search'),
                            endpoint='search', methods=['GET'])
