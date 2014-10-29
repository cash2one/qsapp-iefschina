# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template_string
from jinja2 import Markup
from ..models import NaviModel, SlideModel, ArticleModel


navi_str = '''
{% for channel in navi.channels %}
    <li class=""><a href="{{ channel.url }}">{{ channel.name }}</a></li>
{% endfor %}
'''

slide_str = '''
{% if slides %}
<div class="banner">
   	<ul>
   		{% for slide in slides %}
       	<li style="width: 25%; background-image: url({{ slide.image }}); background-size: 100% 100%;">
       		<div class="inner">
				{% if slide.title %}<h1>{{ slide.title }}</h1>{% endif %}
				{% if slide.describe %}<p>{{ slide.describe }}</p>{% endif %}
				{% if slide.link %}<a class="btn" href="{{ slide.link }}">了解详情</a>{% endif %}
			</div>
       	</li>
       	{% endfor %}
   	</ul>
</div>
{% endif %}
'''

event_str = '''
<div class="panel panel-default">
    <div class="panel-heading">
        <h3 class="panel-title">年会&活动</h3>
    </div>
    <div class="panel-body">
        <table class="table">
        <tbody>
            {% for article in articles %}
            <a href="{{ article.url }}" target="_blank">
            <tr>
                <td><a href="{{ article.url }}" target="_blank">{{ article.title }}</a></td>
                <td>{{ article.date_published|strfdate }}</td>
            </tr>
            </a>
            {% endfor %}
        </tbody>
        </table>
    </div>
</div>
'''

def render_navi(navi_id):
    navi = NaviModel.query.get(1)
    return Markup(render_template_string(navi_str, navi=navi))


def render_slide():
    slides = SlideModel.query.order_by(SlideModel.order).all()
    return Markup(render_template_string(slide_str, slides=slides))


def render_event(language='cn'):
    cids = [6, 8] if language == 'en' else [1, 3]
    query = ArticleModel.get_article_query(cids=cids, limit=5)
    return Markup(render_template_string(event_str, articles=query.all()))