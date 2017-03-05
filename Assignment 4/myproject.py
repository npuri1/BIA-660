import os
import json
import requests
import datetime
import re
from json import load
from urllib2 import urlopen
from flask import Flask, request, Response
from textblob import TextBlob
import time
import random

application = Flask(__name__)

#SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')

slack_inbound_url = 'https://hooks.slack.com/services/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'

@application.route('/slack', methods=['POST'])
def inbound():
    delay = random.uniform(0, 10)
    time.sleep(delay)
    response = {'username': 'nitika_bot', 'icon_emoji': ':computer:'}

    #if request.form.get('token') == SLACK_WEBHOOK_SECRET:
    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = request.form.get('text')
    IP_Address = load(urlopen('http://jsonip.com'))['ip']
    inbound_message = username + " in " + channel + " says: " + text
    owner_name = 'npuri1'
    my_chatbot_name = 'nitika_bot'
    if username in [owner_name, 'zac.wentzell']:
        #response['text'] = text
        if text == "&lt;BOTS_RESPOND&gt;":
            response['text'] = 'Hello, my name is '+str(my_chatbot_name)+'. I belong to '+str(owner_name)+'. I live at '+str(IP_Address)+'.'
            r = requests.post(slack_inbound_url, json=response)
        elif text.find("&lt;I_NEED_HELP_WITH_CODING&gt;")!=-1:
            my_list = text.split(":")
            topic = my_list[1]
            topic=topic.strip()
            my_tags = re.findall(r"\[(.*?)\]", topic)
            if not my_tags:
                stack_url = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=" + topic + "&site=stackoverflow"
            else:
                my_tags = ''.join(str(i) + ';' for i in my_tags)
                stack_url = "https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=" + topic + "&tagged="+my_tags+"&site=stackoverflow"
            r = requests.get(stack_url)
            my_json = json.loads(r.text)
            response = {'username': 'nitika_bot', 'icon_emoji': ':computer:', 'attachments': [{'color': '#36a64f', 'pretext': 'ANSWER 1','fields': [{'title': 'LINK', 'value': my_json['items'][0]['link'], 'short': False},{'title': 'Number of responses', 'value': str(my_json['items'][0]['answer_count']), 'short': True},{'title': 'DATE', 'value': str(datetime.datetime.fromtimestamp(my_json['items'][0]['creation_date'])), 'short': True}]}]}
            r = requests.post(slack_inbound_url, json=response)
            response = {'username': 'nitika_bot', 'icon_emoji': ':computer:', 'attachments': [{'color': '#ad2d91', 'pretext': 'ANSWER 2','fields': [{'title': 'LINK', 'value': my_json['items'][1]['link'], 'short': False},{'title': 'Number of responses', 'value': str(my_json['items'][1]['answer_count']),'short': True}, {'title': 'DATE', 'value': str(datetime.datetime.fromtimestamp(my_json['items'][1]['creation_date'])), 'short': True}]}]}
            r=requests.post(slack_inbound_url, json=response)
            response = {'username': 'nitika_bot', 'icon_emoji': ':computer:', 'attachments': [{'color': '#05afb2', 'pretext': 'ANSWER 3','fields': [{'title': 'LINK', 'value': my_json['items'][2]['link'], 'short': False},{'title': 'Number of responses', 'value': str(my_json['items'][2]['answer_count']),'short': True}, {'title': 'DATE', 'value': str(datetime.datetime.fromtimestamp(my_json['items'][2]['creation_date'])), 'short': True}]}]}
            r = requests.post(slack_inbound_url, json=response)
            response = {'username': 'nitika_bot', 'icon_emoji': ':computer:', 'attachments': [{'color': '#3f00ff', 'pretext': 'ANSWER 4','fields': [{'title': 'LINK', 'value': my_json['items'][3]['link'], 'short': False},{'title': 'Number of responses', 'value': str(my_json['items'][3]['answer_count']),'short': True}, {'title': 'DATE', 'value': str(datetime.datetime.fromtimestamp(my_json['items'][3]['creation_date'])), 'short': True}]}]}
            r = requests.post(slack_inbound_url, json=response)
            response = {'username': 'nitika_bot', 'icon_emoji': ':computer:', 'attachments': [{'color': '#e83006', 'pretext': 'ANSWER 5','fields': [{'title': 'LINK', 'value': my_json['items'][3]['link'], 'short': False},{'title': 'Number of responses', 'value': str(my_json['items'][4]['answer_count']),'short': True}, {'title': 'DATE', 'value': str(datetime.datetime.fromtimestamp(my_json['items'][4]['creation_date'])), 'short': True}]}]}
            r = requests.post(slack_inbound_url, json=response)
        elif text.find("&lt;WHAT'S_THE_WEATHER_LIKE_AT&gt;") != -1:
            my_list = text.split(":")
            topic = my_list[1]
            topic=topic.strip()
            if topic.isdigit():
                weather_url = "http://api.openweathermap.org/data/2.5/weather?zip="+topic+"&units=imperial&APPID=f022cb2b5f2418b86f00ea44453b27a1"
            else:
                geo_url = "http://www.datasciencetoolkit.org/street2coordinates/"+topic
                r=requests.get(geo_url)
                my_json = json.loads(r.text)
                weather_url ="http://api.openweathermap.org/data/2.5/weather?lat="+str(my_json[topic]['latitude'])+"&lon="+str(my_json[topic]['longitude'])+"&units=imperial&APPID=f022cb2b5f2418b86f00ea44453b27a1"
            r = requests.get(weather_url)
            my_json = json.loads(r.text)
            response = {'username': 'nitika_bot', 'icon_emoji': ':computer:','attachments': [{'color': '#36a64f','pretext':'WEATHER REPORT','fields': [{'title': 'Weather Description','value': my_json['weather'][0]['description'],'short': True},{'title': 'Humidity', 'value': str(my_json['main']['humidity'])+'%', 'short': True},{'title': 'Low', 'value': str(my_json['main']['temp_min'])+' Degree F', 'short': True},{'title': 'High', 'value': str(my_json['main']['temp_max'])+' Degree F', 'short': True},{'title': 'Wind Speed', 'value': str(my_json['wind']['speed'])+' MPH', 'short': True},{'title': 'Wind Angle', 'value': str(my_json['wind']['deg'])+' Degrees', 'short': True}]}]}
            r = requests.post(slack_inbound_url, json=response)

    print inbound_message
    print request.form

    return Response(), 200


@application.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)

