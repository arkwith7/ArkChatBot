import os
import random
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import JsonResponse
from django.core.mail import send_mail
from smtplib import SMTPException

from chatapp.ArkChatFramework.ArkChat.chatting_home import ChattingHomepage
from chatapp.ArkChatFramework.ArkChat.chatting_catechism import ChattingCatechism, ReadingBible
from chatapp.ArkChatFramework.ArkChat.conversations import create_conversation, ChattingConversation
from chatapp.ArkChatFramework.DialogManager.ibis_types import Greet
from chatapp.ArkChatFramework.DialogManager.trindikit import Speaker
from chatapp.ArkChatFramework.ArkChat.chatting_home_ishift import ChattingiShiftHomepage

# Create your views here.
context = {}

import logging

logger = logging.getLogger(__name__)
work_dir = os.path.dirname(os.path.realpath(__file__))
bot = ChattingHomepage(work_dir)
catechism_bot = ChattingCatechism(work_dir)
conversation_bot = ChattingConversation(work_dir)
read_bible = ReadingBible(work_dir,"")
travel_ibis =  create_conversation()

ishift_bot = ChattingiShiftHomepage(work_dir)

 
def index(request):
    template = loader.get_template('chatapp/base_contents_kr.html')
#    template = loader.get_template('base_contents.html')
    context = {
#         'login_success' : False,
#         'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))

def chat_home(request):
    template = loader.get_template('chatapp/chat_home_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["아크위드 채팅 홈페이지에 오신것을 환영합니다",
                          "아크위드 홈페이지 설명 챗봇이 회사의  vision, mission, 제품, 서비스, 주요기술, 연락처에 대해 답변합니다."]
    }
    return HttpResponse(template.render(context, request))

def popup_chat_home(request):
    template = loader.get_template('chatapp/popup_chat_home_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["아크위드 채팅 홈페이지에 오신것을 환영합니다",
                          "아크위드 홈페이지 설명 챗봇이 회사의  vision, mission, 제품, 서비스, 주요기술, 연락처에 대해 답변합니다."]
    }
    return HttpResponse(template.render(context, request))


def call_chatbot(request):
    if request.method == 'POST':
        if request.is_ajax():
            userID = request.POST['user']
            sentence = request.POST['message']
            #python은 unicode만을 허용한다
            #bytesThing = sentence.encode(encoding='UTF-8')
            #newStringThing = bytesThing.decode(encoding='UTF-8')
            logger.debug("question[{}]".format(sentence))
#            answer = clean_up_sentence(sentence)
#             answer = bot.response(sentence, userID)
            answer = bot.get_answer(sentence, userID)
            #bytesThing = answer.encode(encoding='UTF-8')
            #newStringThing = bytesThing.decode(encoding='UTF-8')
            logger.debug("answer[{}]".format(answer))
            return HttpResponse(answer)
     
    return render(request)

def chat_catechism(request):
    template = loader.get_template('chatapp/chat_catechism_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["웨스트민스터 소요리 문답 채팅에 오신것을 환영합니다",
                          "기독교 교리를 설명하는 소요리 문답을 학습한 챗봇이  하나님, 사람, 예수그리스도, 신앙생활에 대한 답변과 관련 성경구절을 제시합니다."]
    }
    return HttpResponse(template.render(context, request))

def popup_chat_catechism(request):
    template = loader.get_template('chatapp/popup_chat_catechism_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["웨스트민스터 소요리 문답 채팅에 오신것을 환영합니다",
                          "기독교 교리를 설명하는 소요리 문답을 학습한 챗봇이  하나님, 사람, 예수그리스도, 신앙생활에 대한 답변과 관련 성경구절을 제시합니다."]
    }
    return HttpResponse(template.render(context, request))


def call_catechism_chatbot(request):
    if request.method == 'POST':
        if request.is_ajax():
            userID = request.POST['user']
            sentence = request.POST['message']
            logger.debug("question[%s]" % sentence)
            answer = catechism_bot.get_answer(sentence, userID)
            logger.debug("answer[%s]" % answer)
            return HttpResponse(json.dumps(answer), content_type="application/json")
     
    return render(request)
#셩경구절 일기
def get_bible_paragraph(request):

    if request.method == 'GET':
        if request.is_ajax():
            bible_paragraph_info = request.GET['paragraph']
            logger.debug("bible_paragraph_info[%s]" % bible_paragraph_info)
            bible_paragraph_contents = ""
            paragraph_info = read_bible.get_bible_paragraph_info(bible_paragraph_info.strip())

            if (paragraph_info['bible_name_abbr_kr'] == ReadingBible.bible_info['bible_name_abbr_kr']) and \
                (paragraph_info['chapter'] == ReadingBible.bible_info['chapter']):
                
                logger.debug("get bible_paragraph_contents from cashe")
                if paragraph_info['to_section']:
                    start_verses = int(paragraph_info['from_section'])
                    end_verses = int(paragraph_info['to_section'])
                    for i in range(start_verses, end_verses+1):
                        bible_paragraph_contents += " "
                        bible_paragraph_contents += str(i)
                        bible_paragraph_contents += ". "
                        bible_paragraph_contents += ReadingBible.bible_chapter_contents[str(i)]
                else:
                    bible_paragraph_contents += paragraph_info['from_section']
                    bible_paragraph_contents += ". "
                    bible_paragraph_contents += ReadingBible.bible_chapter_contents[paragraph_info['from_section']]
            else:
                logger.debug("get bible_paragraph_contents from server processing")
                bible_paragraph_contents = read_bible.get_bible_paragraph(bible_paragraph_info.strip())
                
            logger.debug("bible_paragraph_contents[%s]" % bible_paragraph_contents)
            return HttpResponse(json.dumps(bible_paragraph_contents), content_type="application/json")
     
    return render(request)

def contacts(request):
    logger.debug("call contacts...")
    name = request.GET.get('name', None)
    email = request.GET.get('email', None)
    message = request.GET.get('message', None)
    logger.debug("name[%s]" % name)
    logger.debug("email[%s]" % email)
    logger.debug("message[%s]" % message)
    
    subject = '['+email+']' + name
    message = message + '\n['+email+']'
    email_from = email
    recipient_list = ['arkwith7@gmail.com',]
    
    data = {
        'status': 'success'
    }

    try:
        send_mail( subject, message, email_from, recipient_list, fail_silently=False )
    except SMTPException as e:
        logger.error('There was an error sending an email: ', e)
        data['status'] = 'error'  

    if data['status'] == 'error':
        data['error_message'] = '메시지 보내기가 실패하였습니다.'
        
    return JsonResponse(data)

def chat_conversations(request):
    template = loader.get_template('chatapp/chat_conversations_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["국내여행 교통편 가격 문의 채팅에 오신것을 환영합니다.",
                          "이용 하시려는 교통편을 말씀해 주세요? 비행기 또는 기차, 버스로"]
    }
    chat_conversations_init()
    return HttpResponse(template.render(context, request))

def popup_chat_conversations(request):
    template = loader.get_template('chatapp/popup_chat_conversations_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["국내여행 교통편 가격 문의 채팅에 오신것을 환영합니다.",
                          "이용 하시려는 교통편을 말씀해 주세요? 비행기 또는 기차, 버스로"]
    }
    chat_conversations_init()
    return HttpResponse(template.render(context, request))

def call_conversations_chatbot(request):
    
    userID = request.POST['user']
    sentence = request.POST['message']
    logger.debug("question[{}]".format(sentence))
    
    cfg_answer = conversation_bot.get_answer(sentence, userID)

    # CFG 문법에서 정의한 일치하는 인스턴스가 없을 경우 처리
    if cfg_answer == "no_matching":
        if sentence:
            cfg_answer = sentence
        else:
            cfg_answer = ""
    
    travel_ibis.INPUT.set(cfg_answer)
    travel_ibis.LATEST_SPEAKER.set(Speaker.USR)
    #ibis.input()
    travel_ibis.interpret()
    travel_ibis.update()
    #travel_ibis.print_state()

    if not travel_ibis.IS.private.agenda and not travel_ibis.IS.private.plan and not travel_ibis.IS.shared.qud:
        logger.debug("answer[{}]".format("대화다시시작"))
        chat_conversations_init()
        return HttpResponse("이용 하시려는 교통편을 말씀해 주세요? 비행기 또는 기차, 버스로")

    travel_ibis.select()
    answer = " "
    if travel_ibis.NEXT_MOVES:
        travel_ibis.generate()
        answer = travel_ibis.OUTPUT.get()
        travel_ibis.output()
        travel_ibis.update()
        #travel_ibis.print_state()
    else:
        logger.debug("answer[{}]".format("대화종료"))
        chat_conversations_init()
        return HttpResponse("이용 하시려는 교통편을 말씀해 주세요? 비행기 또는 기차, 버스로")
        
    logger.debug("answer[{}]".format(answer))
    return HttpResponse(answer)

def chat_conversations_init():
    
    travel_ibis.reset()
    travel_ibis.IS.private.agenda.push(Greet())
    travel_ibis.print_state()
    travel_ibis.select()
    travel_ibis.generate()
           
    travel_ibis.output()
    travel_ibis.update()
    travel_ibis.print_state()

    travel_ibis.INPUT.set('가격문의')
    travel_ibis.LATEST_SPEAKER.set(Speaker.USR)
    #ibis.input()
    travel_ibis.interpret()
    travel_ibis.update()
    travel_ibis.print_state()
    
    travel_ibis.select()
    if travel_ibis.NEXT_MOVES:
        travel_ibis.generate()
        travel_ibis.output()
        travel_ibis.update()
        travel_ibis.print_state()


def intro_chatbot_service(request):
    template = loader.get_template('chatapp/intro_chatbot_service.html')
    context = {
        'login_success' : False,
        'initMessages' : ["",
                          ""]
    }
    return HttpResponse(template.render(context, request))

def popup_chat_home_ishift(request):
    template = loader.get_template('chatapp/popup_chat_home_ishift_screen.html')
    context = {
        'login_success' : False,
        'initMessages' : ["아이시프트 채팅 홈페이지에 오신것을 환영합니다",
                          "아이시프트 홈페이지 설명 챗봇이 회사의  솔루션과 서비스에 대해 답변합니다."]
    }
    return HttpResponse(template.render(context, request))


def call_ishift_chatbot(request):
    if request.method == 'POST':
        if request.is_ajax():
            userID = request.POST['user']
            sentence = request.POST['message']
            #python은 unicode만을 허용한다
            #bytesThing = sentence.encode(encoding='UTF-8')
            #newStringThing = bytesThing.decode(encoding='UTF-8')
            logger.debug("question[{}]".format(sentence))
#            answer = clean_up_sentence(sentence)
#             answer = bot.response(sentence, userID)
            answer = ishift_bot.get_answer(sentence, userID)
            #bytesThing = answer.encode(encoding='UTF-8')
            #newStringThing = bytesThing.decode(encoding='UTF-8')
            logger.debug("answer[{}]".format(answer))
            return HttpResponse(answer)
     
    return render(request)


def get_answer(sentence, intents, results, userID='123', show_details=False):
#     print ("tf_chat_bot_response_kr response start....")
#     results = classify(sentence, words, classes, model)
#     print ("tf_chat_bot_response_kr results [%s]" % results )
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return random.choice(i['responses'])

            results.pop(0)
