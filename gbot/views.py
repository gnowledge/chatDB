# -*- coding: utf8 -*-B
import json
import logging
import requests
import telepot
import urllib2
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
#from .utils import parse_planetpy_rss


TelegramBot = telepot.Bot(settings.TELEGRAM_BOT_TOKEN)

logger = logging.getLogger('telegram.bot')


def _display_help():
    
    return "Welcome to gstudio bot"

def _display_planetpy_feed():
    return render_to_string('feed.md', {'items': parse_planetpy_rss()})


def _get_all_workspaces():
    response = requests.get("http://nroer.gov.in/api/v1/workspace")
    rc = eval(unicode(response.content, 'utf_16'))
    print "9999999999999999999999999999999999999999999",rc
    return rc


class CommandReceiveView(View):
    #keyboard = TelegramBot.types.InlineKeyboardButton()
    site_var = ""
    #print "###########",site_varOB
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')
        commands = {
            '/start': _display_help,
            'help': _display_help,
            'feed': _display_planetpy_feed,
            '/getworkspaces':_get_all_workspaces,
        }

        raw = request.body.decode('utf-8')
        logger.info(raw)

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
    
        else:
            try:
                if 'document' in payload['message']:
                    document = payload['message']['document']
                    if payload['message']['document']['thumb']['file_path']:
                        file_path = str("https://api.telegram.org/file/bot402840205:AAHyxQfL_OeXiVwNSQkV2v1dJvQcmhlir5g/" + payload['message']['document']['thumb']['file_path'])
                        files = urllib2.urlopen(file_path)
            except urllib2.URLError,e:
                pass
            buttons = []
            if 'message' in payload.keys():
                chat_id = payload['message']['chat']['id']
                cmd = payload['message'].get('text')  # command
                
            if cmd and  cmd == "/start":
                buttons.append([KeyboardButton(text="nroer.gov.in")])
                buttons.append([KeyboardButton(text="abcde.metastudio.org")])

                TelegramBot.sendMessage(chat_id,"Welcome to gstudio please select websites to connect",reply_markup=ReplyKeyboardMarkup(
                   keyboard=buttons ))
            
            if cmd and cmd == "nroer.gov.in":
                site_var = "http://nroer.gov.in"
                response = requests.get("http://nroer.gov.in/api/v1/workspace")
                rc = eval(unicode(response.content, 'utf_16'))
                TelegramBot.sendMessage(chat_id,"Please upload file!",reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            
            if cmd and cmd == "abcde.metastudio.org":
                site_var = "abcde.metastudio.org"
                TelegramBot.sendMessage(chat_id,site_var)
                        
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
