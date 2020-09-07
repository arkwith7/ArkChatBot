# -*- encoding: utf-8 -*-

#
# travel.py
#
# The author or authors of this code dedicate any and all 
# copyright interest in this code to the public domain.

import os
import logging
import random

from chatapp.ArkChatFramework.DialogManager.tf_learning_model import ChatClient
from chatapp.ArkChatFramework.DialogManager.cfg_grammar import *
from chatapp.ArkChatFramework.DialogManager.ibis import *

# 기계학습자료 삭제후 재학습 기능 보완
# 가격데이타베이스에 가격이 등록되지 않았을때 처리
# 의도 등록시 개체명과 의도로 나누어 등록 여행문의 문장 입력시 장소 인디비주얼로 매칭되는 문제 해결 필요
class ChattingConversation(ChatClient):
    '''
    classdocs
    '''


    def __init__(self, work_dir):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        # logger.info("작업디렉토리 : %s" % os.getcwd())
        self.intents_file_name = os.path.join(work_dir, "ArkChatFramework/ArkNLU/DialogIntents/intents_conversations_kr.json")
        # logger.info("intents       파일 디렉토리[%s]" % input_file_name)
        self.input_training_data_file_name = os.path.join(work_dir, "ArkChatFramework/ArkNLU/NLUModel/training_data_conversations_kr")
        # logger.info("training      파일 디렉토리[%s]" % input_training_data_file_name)
        self.tflearn_logs_dir = os.path.join(work_dir, 'ArkChatFramework/ArkNLU/NLUModel/conversations_tflearn_kr_logs')
        # logger.info("tflearn_logs     디렉토리[%s]" % tflearn_logs_dir)
        self.tflearn_model_file_name = os.path.join(work_dir, 'ArkChatFramework/ArkNLU/NLUModel/model_conversations_kr.tflearn')
        # logger.info("tflearn_model 파일 디렉토리[%s]" % tflearn_model_file_name)
        #     intents_file, training_data_file, tflearn_logs_dir, tflearn_model_file
        learning_model_files = dict(intents_file = self.intents_file_name, 
                                    training_data_file = self.input_training_data_file_name, 
                                    tflearn_logs_dir = self.tflearn_logs_dir, 
                                    tflearn_model_file = self.tflearn_model_file_name)
        
        ChatClient.__init__(self, 'ko-KR', learning_model_files)
        self.context = {}
        self.criteria_coincidence = 0.50
        self.not_matching_count = 1
        self.previous_not_matching = False
        self.slang_matching_count = 1
        self.previous_slang_matching = False

    def get_answer(self, sentence, userID='123', show_details=False):

        results = ChatClient.get_classify(self, sentence)
        
        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in self.dialog_intents['intents']:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        # send "no_matching" message when the matching rate of the message is lower than self.criteria_coincidence.
                        if self.criteria_coincidence > results[0][1]:
                            return "no_matching"
                            
                        # set context for this intent if necessary
                        if 'context_set' in i:
                            if show_details: self.logger.debug('context:', i['context_set'])
                            self.context[userID] = i['context_set']
    
                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or \
                            (userID in self.context and 'context_filter' in i and i['context_filter'] == self.context[userID]):
                            if show_details: self.logger.debug ('tag:', i['tag'])
                            # a random response from the intent
                            return random.choice(i['responses'])
    
                results.pop(0)

def conversation_NLULearning():

    print("현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
    print("부모 디렉토리로 변경[%s]" % os.chdir(os.pardir))
    print("변경후 현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
 
    print("intents 파일 디렉토리[%s]" % os.path.abspath("ArkNLU/DialogIntents/intents_conversations_kr.json"))

    input_file_name = os.path.abspath("ArkNLU/DialogIntents/intents_conversations_kr.json")
    print("intents       파일 디렉토리[%s]" % input_file_name)
    
    input_training_data_file_name = os.path.abspath("ArkNLU/NLUModel/training_data_conversations_kr")
    print("training      파일 디렉토리[%s]" % input_training_data_file_name)
    
    tflearn_logs_dir = os.path.abspath('ArkNLU/NLUModel/conversations_tflearn_kr_logs')
    print("tflearn_logs     디렉토리[%s]" % tflearn_logs_dir)
    
    tflearn_model_file_name = os.path.abspath('ArkNLU/NLUModel/model_conversations_kr.tflearn')
    print("tflearn_model 파일 디렉토리[%s]" % tflearn_model_file_name)

#     intents_file, training_data_file, tflearn_logs_dir, tflearn_model_file
    learning_model_files = dict(intents_file=input_file_name, 
                                training_data_file=input_training_data_file_name, 
                                tflearn_logs_dir=tflearn_logs_dir, 
                                tflearn_model_file=tflearn_model_file_name)

    bot = ChatClient('ko-KR', learning_model_files)
    print("conversations NLULearning instance...")
    
    if bot.create_learning_model(show_details=True):
        print("conversations model creation success....")
    else:
        print("conversations model creation fail....")


class TravelDB(Database):

    def __init__(self):
        self.entries = []

    def consultDB(self, question, context):
        depart_city = self.getContext(context, "depart_city")
        dest_city = self.getContext(context, "dest_city")
        day = self.getContext(context, "depart_day")
        entry = self.lookupEntry(depart_city, dest_city, day)
        if entry:
            print("entry : [{}]".format(entry))
            price = entry['price']
            print("price : [{}]".format(price))
            return Prop(Pred1("price"), Ind(price), True)
        else:
            return Prop(Pred1("price"), Ind(0), True)

    def lookupEntry(self, depart_city, dest_city, day):
        for e in self.entries:
            if e['from'] == depart_city and e['to'] == dest_city and e['day'] == day:
                return e
        #assert False
        return False

    def getContext(self, context, pred):
        for prop in context:
            if prop.pred.content == pred:
                return prop.ind.content
        assert False

    def addEntry(self, entry):
        self.entries.append(entry)

class TravelGrammar(SimpleGenGrammar, CFG_Grammar):
    def generateMove(self, move):
        try:
            assert isinstance(move, Answer)
            prop = move.content
            assert isinstance(prop, Prop)
            assert prop.pred.content == "price"
            if (prop.ind.content > 0):
                return "가격은 " + str(prop.ind.content) + "원  입니다."
            else:
                return "죄송합니다. 가격을 확인 할 수 없습니다."
        except:
            return super(TravelGrammar, self).generateMove(move)
        
def create_conversation():
    
    # 도메인 정의
    preds0 = 'return', 'need-visa'
    
    preds1 = {'price': 'int',
              'how': 'means',
              'dest_city': 'city',
              'depart_city': 'city',
              'depart_day': 'day',
              'class': 'flight_class',
              'return_day': 'day',
              }
    
    means = 'plane', 'train', 'bus'
    cities = 'seoul', 'pusan', 'daegu', 'gwangju', 'Gangneung', 'jeju'
    days = 'today', 'tomorrow'
    classes = 'first', 'second'
    
    sorts = {'means': means,
             'city': cities,
             'day': days,
             'flight_class': classes,
             }
    
    domain = Domain(preds0, preds1, sorts)
    
    domain.add_plan("?x.price(x)",
                   [Findout("?x.how(x)"),
                    Findout("?x.dest_city(x)"),
                    Findout("?x.depart_city(x)"),
                    Findout("?x.depart_day(x)"),
                    Findout("?x.class(x)"),
                    #Findout("?return()"),
                    # If("?return()", 
                    #    [Findout("?x.return_day(x)")]),
                    ConsultDB("?x.price(x)")
                     ])
    
    
    # 데이타베이스 정의
    database = TravelDB()
    database.addEntry({'price':'99400', 'from':'seoul', 'to':'pusan', 'day':'today'})
    database.addEntry({'price':'88400', 'from':'seoul', 'to':'gwangju', 'day':'today'})
    database.addEntry({'price':'68000', 'from':'seoul', 'to':'daegu', 'day':'today'})
    database.addEntry({'price':'99400', 'from':'pusan', 'to':'seoul', 'day':'today'})
    database.addEntry({'price':'88400', 'from':'gwangju', 'to':'seoul', 'day':'today'})
    database.addEntry({'price':'68000', 'from':'daegu', 'to':'seoul', 'day':'today'})
    
    #대화 문법 정의
    grammar = TravelGrammar()
    # NLTK_DATA가 설치된 패쓰를 찾아서 fcfg파일을 grammars 디렉토리에 복사하고 아래와 같이 패쓰지정
    grammar.loadGrammar("grammars/travel_kr.fcfg")
    #grammar.loadGrammar("file:travel_kr.fcfg")
    grammar.addForm("Ask('?x.how(x)')", "이용 하시려는 교통편을 말씀해 주세요? 비행기 또는 기차, 버스로")
    grammar.addForm("Ask('?x.dest_city(x)')", "도착지가 어디입니까?")
    grammar.addForm("Ask('?x.depart_city(x)')", "출발은 어디에서 하십니까?")
    grammar.addForm("Ask('?x.depart_day(x)')", "언제 출발 하세요?")
    grammar.addForm("Ask('?x.return_day(x)')", "언제 돌아 오시나요?")
    grammar.addForm("Ask('?x.class(x)')", "좌석 등급은 어느것을 원하세요? 일등석 ,일반석등 ")
    grammar.addForm("Ask('?return()')", "왕복표를 원하십니까?")
    
    return IBIS1(domain, database, grammar)





######################################################################
# Running the dialogue system
######################################################################

if __name__=='__main__':
    
    conversation_NLULearning()

#     ibis = create_conversation()
# 
#     #ibis.run()
#     ibis.reset()
#     #ibis.control()
#     """The IBIS control algorithm."""
#     ibis.IS.private.agenda.push(Greet())
#     ibis.print_state()
#     while True:
#         ibis.select()
#         if ibis.NEXT_MOVES:
#             ibis.generate()
#             print("---------------------------------------")
#             print("System>", ibis.OUTPUT.get() or "[---]")
#             print("---------------------------------------")
# 
#             ibis.output()
#             ibis.update()
#             ibis.print_state()
#         if ibis.PROGRAM_STATE.get() == ProgramState.QUIT:
#             break
#         promptStr = input("User> ")
#         ibis.INPUT.set(promptStr)
#         ibis.LATEST_SPEAKER.set(Speaker.USR)
#         #ibis.input()
#         ibis.interpret()
#         ibis.update()
#         ibis.print_state()

