# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request, views, render_template
from flask.ext.paginate import Pagination
from iefschina.blueprints import blueprint_www

from iefschina.models import ChannelModel


article_per_page = 10


class ChannelView(views.MethodView):
    '''
        频道页
    '''

    @property
    def page(self):
        try:
            return int(request.args.get('page', 1))
        except ValueError:
            return 1

    def get(self, cid):
        channel = ChannelModel.query.get(cid)
        query = ChannelModel.get_channel_query('cn')
        pager = Pagination(bs_version=3, page=self.page,
                           total=channel.articles.count())

        return render_template('www/channel.html',
                                channels=query.all(),
                                channel=channel,
                                pager=pager)


blueprint_www.add_url_rule('/channel/<int:cid>/',
                            view_func=ChannelView.as_view(b'channel'),
                            endpoint='channel', methods=['GET'])
