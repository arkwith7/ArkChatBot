'''
Created on 2018. 3. 24.

@author: phs
'''
import os
import logging
import random
 
import json
import requests
from bs4 import BeautifulSoup

from chatapp.ArkChatFramework.DialogManager.tf_learning_model import ChatClient

class ChattingCatechism(ChatClient):
    '''
    classdocs
    '''


    def __init__(self, work_dir):
        '''
        Constructor
        '''
        self.logger = logging.getLogger(__name__)
        # logger.info("작업디렉토리 : %s" % os.getcwd())
        self.intents_file_name = os.path.join(work_dir, "ArkChatFramework/ArkNLU/DialogIntents/intents_catechism_kr.json")
        # logger.info("intents       파일 디렉토리[%s]" % input_file_name)
        self.input_training_data_file_name = os.path.join(work_dir, "ArkChatFramework/ArkNLU/NLUModel/training_data_catechism_kr")
        # logger.info("training      파일 디렉토리[%s]" % input_training_data_file_name)
        self.tflearn_logs_dir = os.path.join(work_dir, 'ArkChatFramework/ArkNLU/NLUModel/catechism_tflearn_kr_logs')
        # logger.info("tflearn_logs     디렉토리[%s]" % tflearn_logs_dir)
        self.tflearn_model_file_name = os.path.join(work_dir, 'ArkChatFramework/ArkNLU/NLUModel/model_catechism_kr.tflearn')
        # logger.info("tflearn_model 파일 디렉토리[%s]" % tflearn_model_file_name)
        #     intents_file, training_data_file, tflearn_logs_dir, tflearn_model_file
        learning_model_files = dict(intents_file = self.intents_file_name, 
                                    training_data_file = self.input_training_data_file_name, 
                                    tflearn_logs_dir = self.tflearn_logs_dir, 
                                    tflearn_model_file = self.tflearn_model_file_name)
        
        ChatClient.__init__(self, 'ko-KR', learning_model_files)
        self.context = {}
        self.criteria_coincidence = 0.80
        self.not_matching_count = 1
        self.previous_not_matching = False
        self.slang_matching_count = 1
        self.previous_slang_matching = False
        self.context_filter_message = "상위 질문 이후 가능합니다."
        self.not_matching_message = "에 대해 이해하지 못했습니다."
        self.usage_guide_message = "여기서는 음성과 문자 채팅으로 웨스트민스터 소요리 문답의 내용인 하나님에 대하여, 사람에 대하여, 예수그리스도에 대하여, 신앙생활에 대하여와  관련된 내용만 채팅이 가능합니다."
        self.previous_context_set = ''
        self.previous_responses = ''

    def set_answer(self, category, title, answer, explanation):

# {
# "category" : "list"|"qna"|"abnormal"
# "title" : "",
# "answer": [""],
# "explanation" :[]
# }
        response = {}
        response["category"] = ''
        response["title"] = ''
        response["answer"] = []
        response["explanation"] = []
        
        
        response["category"] = category
        response["title"] = title
        
        if type(answer) is list:
            response["answer"] = answer[:]
        else:
            response["answer"].append(answer)
            
        if type(explanation) is list:
            response["explanation"] = explanation[:]
        else:
            response["explanation"].append("")
        #한글이 안보이고 코드로 보이는것을 ensure_ascii=False라는 속성을 추가하여 해결 
        return json.dumps(response, ensure_ascii=False)
        
    
    def get_answer(self, sentence, userID='123', show_details=False):

        #If a conversation that is not understood during the chatting is in progress more than 3 times,
        # send a usage guide message.
        if self.not_matching_count >= 3:
            self.not_matching_count = 1
            self.previous_not_matching = False
            return self.set_answer("abnormal", "guide_message", self.usage_guide_message, "")

        results = ChatClient.get_classify(self, sentence)
        
        #Echo processing when using bad language three times in a row.
        if self.slang_matching_count >= 3:
            if results[0][0] != 'Slang':
                self.slang_matching_count = 1
                self.previous_slang_matching = False
            else:
                return self.set_answer("abnormal", "not_matching", sentence, "")

        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in self.dialog_intents['intents']:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        self.logger.debug("previous_context_set : [%s] ", self.previous_context_set)
                        # send message when the matching rate of the message is lower than self.criteria_coincidence.
                        if self.criteria_coincidence > results[0][1]:
                            return_message = '"' + sentence + '"' + self.not_matching_message
                            if self.previous_not_matching:
                                self.not_matching_count += 1
                            self.previous_not_matching = True
                            return self.set_answer("abnormal", "not_matching", return_message, "")
                            
                        # check when using bad language three times in a row.
                        if results[0][0] == 'Slang':
                            if self.previous_slang_matching:
                                self.slang_matching_count += 1
                            self.previous_slang_matching = True

                        # set context for this intent if necessary
                        if 'context_set' in i:
                            if show_details: self.logger.debug('context:', i['context_set'])
                            self.context[userID] = i['context_set']
    
                        # check context_set for this intent
                        if i['context_set']:
                            self.previous_context_set = i['context_set']
                            self.previous_responses = i['responses']
                            self.logger.debug("context_set : [%s] ",i['context_set'])
                            response = {}
                            response["response"] = i['responses']
                            return self.set_answer("list", i['patterns'][0], i['responses'], "")
    
                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or \
                            (userID in self.context and 'context_filter' in i and i['context_filter'] == self.context[userID]):
                            
                            if show_details: self.logger.debug ('tag:', i['tag'])
                            
                            # a random response from the intent
                            self.previous_context_set = i['context_set']
                            self.previous_responses = i['responses']
                            
                            explanation = []
                            if ('responses_ref' in i): explanation = i['responses_ref']
                                
                            return self.set_answer("qna", i['patterns'][0], random.choice(i['responses']), explanation)
                        
                        elif self.previous_context_set == i['context_filter']:
                            self.logger.debug("context_set : [%s] ",i['context_set'])
                            self.logger.debug("context_filter : [%s] ",i['context_filter'])
                            self.logger.debug("previous_context_set : [%s] ",self.previous_context_set)
                            self.previous_context_set = i['context_set']
                            self.previous_responses = i['responses']
                            return self.set_answer("list", i['patterns'][0], i['responses'], "")
                        else:
                            if not self.previous_responses:
                                self.previous_responses = i['context_filter']
                                return_values = i['context_filter']
                            else:
                                return_values = ""
                                for value in self.previous_responses:
                                    return_values += value + ' '
                                self.previous_responses = i['context_filter']
                                
                            # context_filter와 같은 tag의 responses값을 보여 주고 선택하게 함
                                
                            return self.set_answer("abnormal", "not_matching", return_values + "와 같은 " + self.context_filter_message, "")
    
                results.pop(0)

class ReadingBible(object):
    '''
    classdocs
    '''
    bible_info = {
         "class" : "",                    # Old|New
         "bible_name_kr" : "",            # 창세기
         "bible_name_abbr_kr" : "",       # 창
         "bible_name_en" : "",            # Genesis
         "bible_name_abbr_en" : "",       # GEN
         "bskorea_name" : "",             # gen
         "chapter" : "",
         "from_section" : "",
         "to_section" : ""
        }
    bible_chapter_contents = {}

    def __init__(self, work_dir, bible_paragraph_info):
        '''
        성경  읽기를 위해 성경구절정보를 성경, 장, 절 정보로 속성 정의
        '''
        self.logger = logging.getLogger(__name__)

        # 사용할 클래스 내부 변수 선언
        self.bible_name_abbr_kr = ""
        self.chapter = ""
        self.from_section = ""
        self.to_section = ""
        
        # 셩경 약어로 성경정보 알아내는 성경정보 JSON파일 경로 설정
        self.bible_abbr_file_name = os.path.join(work_dir, "ArkChatFramework/ArkNLU/DialogIntents/bible_abbr.json")

        if bible_paragraph_info:
            # '창 1:1~10'과 bible_paragraph_info에서  성경 약어 분리
            first_processing_list = bible_paragraph_info.split(' ')
            self.bible_name_abbr_kr = first_processing_list[0]
        
            # '1:1~10'과 bible_paragraph_info의 성경 장 절 정보에서 장 분리  
            second_processing_list = first_processing_list[1].split(':')
            self.chapter = second_processing_list[0]
        
        
            if '~' in second_processing_list[1]:
                third_processing_list = second_processing_list[1].split('~')
                self.from_section = third_processing_list[0]
                self.to_section = third_processing_list[1]
            elif '∼' in second_processing_list[1]:
                third_processing_list = second_processing_list[1].split('∼')
                self.from_section = third_processing_list[0]
                self.to_section = third_processing_list[1]
            else:
                self.from_section = second_processing_list[1]

    def get_bible_paragraph_info(self, bible_paragraph_info):
        '''
        성경구절을 분해하여 성경, 장, 절 정보로 분류 하여  Return
        '''
        paragraph_info = {
            "bible_name_abbr_kr" : "",  # 성경 한글 약어명
            "chapter" : "",             # 성경 장
            "from_section" : "",        # 시작구절
            "to_section" : ""           # 종료구절
        }
        # '창 1:1~10'과 bible_paragraph_info에서  성경 약어 분리
        first_processing_list = bible_paragraph_info.split(' ')
        paragraph_info['bible_name_abbr_kr'] = first_processing_list[0]
        
        # '1:1~10'과 bible_paragraph_info의 성경 장 절 정보에서 장 분리  
        second_processing_list = first_processing_list[1].split(':')
        paragraph_info['chapter'] = second_processing_list[0]
        
        
        if '~' in second_processing_list[1]:
            third_processing_list = second_processing_list[1].split('~')
            paragraph_info['from_section'] = third_processing_list[0]
            paragraph_info['to_section'] = third_processing_list[1]
        elif '∼' in second_processing_list[1]:
            third_processing_list = second_processing_list[1].split('∼')
            paragraph_info['from_section'] = third_processing_list[0]
            paragraph_info['to_section'] = third_processing_list[1]
        else:
            paragraph_info['from_section'] = second_processing_list[1]
            
        return paragraph_info
            
    def set_bible_paragraph_info(self, bible_paragraph_info):
        '''
        성경구절을 분해하여 성경, 장, 절 정보로 분류 
        '''
        # '창 1:1~10'과 bible_paragraph_info에서  성경 약어 분리
        first_processing_list = bible_paragraph_info.split(' ')
        self.bible_name_abbr_kr = first_processing_list[0]
        ReadingBible.bible_info['bible_name_abbr_kr'] = self.bible_name_abbr_kr
        
        # '1:1~10'과 bible_paragraph_info의 성경 장 절 정보에서 장 분리  
        second_processing_list = first_processing_list[1].split(':')
        self.chapter = second_processing_list[0]
        
        
        if '~' in second_processing_list[1]:
            third_processing_list = second_processing_list[1].split('~')
            self.from_section = third_processing_list[0]
            self.to_section = third_processing_list[1]
        elif '∼' in second_processing_list[1]:
            third_processing_list = second_processing_list[1].split('∼')
            self.from_section = third_processing_list[0]
            self.to_section = third_processing_list[1]
        else:
            self.from_section = second_processing_list[1]
            
    def get_query_info(self):
        '''
        대한 성서 공회 개역한글 성경을 크롤링하기위한 질의정보 생성
        '''
        query_info = {
            "bskorea_name" : "", # 대한성서공회에서 사용한 성경 영문약어명
            "chapter" : "",      # 성경 장
            "from_section" : "", # 시작구절
            "to_section" : ""    # 종료구절
        }
        
        # 요청한 성경 약어 획득
        
        # 성경영문약어를 Key로 성경이름정보를 정의한 JSON파일을 읽어들임
        with open(self.bible_abbr_file_name, 'rt', encoding='UTF8') as json_data:
            biblical_abbreviation = json.load(json_data)
        
        # 성경이름정보를 정의한 JSON파일에서 요청 성경 약어로부터 대한성서공회 성경영문약어 획득하여 질의정보에 정의
        bible_name_info = biblical_abbreviation[self.bible_name_abbr_kr]

        # 현재 셩 이름경정보를 클래스 속성 정보에 할당
        ReadingBible.bible_info['class'] = bible_name_info['class']
        ReadingBible.bible_info['bible_name_kr'] = bible_name_info['bible_name_kr']
        ReadingBible.bible_info['bible_name_abbr_kr'] = self.bible_name_abbr_kr
        ReadingBible.bible_info['bible_name_en'] = bible_name_info['bible_name_en']
        ReadingBible.bible_info['bible_name_abbr_en'] = bible_name_info['bible_name_abbr_en']
        
        # 질의정보에 성경구절 질의 정보 정의
        query_info['bskorea_name'] = bible_name_info['bskorea__name']
        query_info['chapter'] = self.chapter
        query_info['from_section'] = self.from_section
        query_info['to_section'] = self.to_section
        
        return query_info
        
    def create_bible_chapter(self, query_info):
        '''
        대한 성서 공회 개역한글 성경을 셩경별 장단위로 크롤링하여 구절정보을 포함하는 딕셔너리 생성
        '''
        # 대한성서공회  url setting을 위한 필요정보
        #version = 'HAN'         # 개역한글
        #book = 'gen'            # 창세기
        #chapter = 1             # 1장을 가져온다.
        
        # 목표 url
        # url = "http://www.bskorea.or.kr/bible/korbibReadpage.php?version=HAN&book=gen&chap=1"
        # 웹 서버에 요청 보내고 응답 받기
        resp = requests.get("https://www.bskorea.or.kr/bible/korbibReadpage.php?version=HAN&book={}&chap={}".format(query_info['bskorea_name'], query_info['chapter']), verify=False)
        # 전송된 HTML 문서 얻기
        html = resp.text
        # HTML 문서를 DOM으로 변환하기
        soup = BeautifulSoup(html, "lxml")
        # 목표 HTML 요소 선택(DIV tag중 ID가 tdBible1인 요소의 하위에 SPAN tag 모두)
        html_element = soup.find("div", {"id" : "tdBible1"}).find_all("span")

        # 크롤링한 성경 장의 구절정보을 담을 딕셔너리 선언
        bible_chapter_table = {}
 
        # 목표 텍스트 추출
        for bible_chapter_verses in html_element:
            # HTML DIV tag중 ID가 tdBible1인 요소의 하위에 SPAN tag 모두를 가지고 와서
            # SPAN tag의 텍스트 성경 구절들을 List객체로 만듬
            table0 = bible_chapter_verses.get_text().strip().split("  ")
            # List객체중 " \xa0\xa0\xa0"로 좌우 분리
            table1 = table0[0].split(" \xa0\xa0\xa0")
        
            # List객체중 구절 번호와 내용의 쌍으로 된것만 선택
            if len(table1) > 1:
                # List객체중 ""\n\n"가 들어 있는것을 좌우 분리하여 죄측내용만 선택
                tmp = table1[1].rsplit("\n\n")
                if len(tmp) > 1:
                    verses = tmp[0]
                else:
                    verses = table1[1]
        
                bible_chapter_table[table1[0]] = verses

        return bible_chapter_table

    def get_bible_paragraph(self, bible_paragraph_info):
        '''
        성경구절 내용 획득하여 Return
        '''
        # 셩경구절정보 초기화
        self.bible_name_abbr_kr = ""
        self.chapter = ""
        self.from_section = ""
        self.to_section = ""
        
        # 셩경구절내용
        response_value = ""
        
        self.set_bible_paragraph_info(bible_paragraph_info)
        query_info = self.get_query_info()
        bible_chapter_contents = self.create_bible_chapter(query_info)
        self.logger.debug("success creating bible_paragraph_contents")
        
        if query_info['to_section']:
            start_verses = int(query_info['from_section'])
            end_verses = int(query_info['to_section'])
            for i in range(start_verses, end_verses+1):
                response_value += " "
                response_value += str(i)
                response_value += ". "
                response_value += bible_chapter_contents[str(i)]
        else:
            response_value += query_info['from_section']
            response_value += ". "
            response_value += bible_chapter_contents[query_info['from_section']]
            
        # 현재 셩경장절과 내용정보를 클래스 속성 정보에 할당
        ReadingBible.bible_info['bskorea_name'] = query_info['bskorea_name']
        ReadingBible.bible_info['chapter'] = query_info['chapter']
        ReadingBible.bible_info['from_section'] = query_info['from_section']
        ReadingBible.bible_info['to_section'] = query_info['to_section']
        ReadingBible.bible_chapter_contents = bible_chapter_contents
        
        return response_value.strip()
        
            
    
def catechism_NLULearning():

    print("현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
    print("부모 디렉토리로 변경[%s]" % os.chdir(os.pardir))
    print("변경후 현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
 
    print("intents 파일 디렉토리[%s]" % os.path.abspath("ArkNLU/DialogIntents/intents_catechism_kr.json"))

    input_file_name = os.path.abspath("ArkNLU/DialogIntents/intents_catechism_kr.json")
    print("intents       파일 디렉토리[%s]" % input_file_name)
    
    input_training_data_file_name = os.path.abspath("ArkNLU/NLUModel/training_data_catechism_kr")
    print("training      파일 디렉토리[%s]" % input_training_data_file_name)
    
    tflearn_logs_dir = os.path.abspath('ArkNLU/NLUModel/catechism_tflearn_kr_logs')
    print("tflearn_logs     디렉토리[%s]" % tflearn_logs_dir)
    
    tflearn_model_file_name = os.path.abspath('ArkNLU/NLUModel/model_catechism_kr.tflearn')
    print("tflearn_model 파일 디렉토리[%s]" % tflearn_model_file_name)

#     intents_file, training_data_file, tflearn_logs_dir, tflearn_model_file
    learning_model_files = dict(intents_file=input_file_name, 
                                training_data_file=input_training_data_file_name, 
                                tflearn_logs_dir=tflearn_logs_dir, 
                                tflearn_model_file=tflearn_model_file_name)

    bot = ChatClient('ko-KR', learning_model_files)
    print("catechism NLULearning instance...")
    
    if bot.create_learning_model(show_details=True):
        print("catechism model creation success....")
    else:
        print("catechism model creation fail....")


if __name__ == '__main__':
#     test_ChatClient()
    catechism_NLULearning()
        