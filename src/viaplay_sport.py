#!/usr/bin/python
# -*- coding: utf-8 -*-
#author: Robert Herber (thanks to Peter Okma for template)

#TODO:
#1. Fix Unicode and space input issues
#Future:
#1. More meaningful info depending on type of content
#2. Multiple actions (view, go to page, go to series overview etc)
#3. Web images (seems to require download, how to do this async?)

from alfred_utils.feedback import Feedback
import urllib
import json
import sys
import logging
import datetime

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time 
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff == 0 and second_diff < 0:
        if second_diff > -10:
            return "any moment"
        if second_diff > -60:
            return "in " + str(-second_diff) + " seconds"
        if second_diff > -120:
            return "in a minute"
        if second_diff > -3600:
            return "in " + str( -second_diff / 60 ) + " minutes"
        if second_diff > -86400:
            return "Today at " + time.strftime("%H:%M")
            #return "in " + str( -second_diff / 3600 ) + " hours"

    if day_diff == 0 and second_diff >= 0:
        if second_diff < 10:
            return "a moment ago"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours ago"

    if day_diff == -1:
        return "Tomorrow at " + time.strftime("%H:%M")
    if day_diff > -7:
        return "in " + str(-day_diff) + " days"
    if day_diff > -31:
        return "in " + str(-day_diff/7) + " weeks"
    if day_diff > -365:
        return "in " + str(-day_diff/30) + " months"

    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff/7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff/30) + " months ago"
    return str(day_diff/365) + " years ago"

logging.basicConfig(filename='example2.log',level=logging.DEBUG)
                                                                                                                                           
url = 'http://content.viaplay.se/pc-se/sport'
response = json.load(urllib.urlopen(url))

blocks = response['_embedded']['viaplay:blocks']

fb = Feedback()
for block in blocks:
    if block['title'] == u'Tablå':
        products = block['_embedded']['viaplay:products']
        category = block['title']
        linktosearch = response['_links']['self']['href'].replace('http://content.viaplay.se/pc-se/', 'http://viaplay.se/')
        #fb.add_item(category, icon="", arg=linktosearch, valid="no", autocomplete=arg)
        fb.add_item(category, icon="", arg=linktosearch)
        for product in products:
            genre = ''
            series = ''
            if '_links' in product and 'viaplay:genres' in product['_links']:
                genre = ' (' + (', '.join(map( lambda x: x['title'], product['_links']['viaplay:genres']))) + ')'
                
            title = product['content']['title'] + genre

            url = product['_links']['viaplay:page']['href'].replace('https://content.viaplay.se/pc-se/', 'http://viaplay.se/')
            
            shouldDisplay = False

            subtitle = ''
            if 'epg' in product and 'start' in product['epg']:
                #subtitle = 'Stream starts at %s ' % product['epg']['start'].replace('T', ' ').replace(':00.000Z', '')
                #logging.debug(product['epg']['start'])
                starttime = datetime.datetime.strptime(product['epg']['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
                endtime = datetime.datetime.strptime(product['epg']['streamEnd'], '%Y-%m-%dT%H:%M:%S.%fZ')
                #logging.debug(starttime)
                subtitle = pretty_date(starttime)
                if starttime < datetime.datetime.now():
                    subtitle = "LIVE " + subtitle
                shouldDisplay = endtime > datetime.datetime.now()
            elif 'content' in product and 'duration' in product['content'] and 'readable' in product['content']['duration']:
                subtitle = product['content']['duration']['readable']
                
            if shouldDisplay:
                fb.add_item(title, subtitle=subtitle, arg=url)
            #logging.debug(fb)
print fb