'''
Created on 2018.3.16.

@author: phs
'''



import os
import sys, json

from chatapp.ArkChatFramework.DialogManager.tf_learning_model import ChatClient


# import warnings
# warnings.filterwarnings('ignore', '.*do not.*',)
context = {}
# os.path.dirname(filename) - 디렉토리 경로 추출
# os.getcwd() - 현재 프로세스의 작업 디렉토리 얻기
# os.curdir() - 현재 디렉토리 얻기
# os.pardir() - 부모 디렉토리 얻기
# ['English',         ['en-US', 'United States']],
# ['한국어',            ['ko-KR']],
# ['中文',             ['cmn-Hans-CN', '普通话 (中国大陆)']],
# ['日本語',           ['ja-JP']],

def get_intents():
    pass
def get_classify(sentence):
    pass
def get_answer(sentence, intents, results, userID='123', show_details=False):
    pass

def test_ChatClient():
#     def __init__(self, language, intents_file, training_data_file, tflearn_logs_dir, tflearn_model_file):
# os.getcwd() - 현재 프로세스의 작업 디렉토리 얻기
# os.curdir() - 현재 디렉토리 얻기
# os.pardir() - 부모 디렉토리 얻기
#특정 경로에 대해 절대 경로 얻기    os.path.abspath(".\\Scripts") 
    print("현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
    print("현재  디렉토리[%s]" % os.curdir)
    print("부모 디렉토리[%s]" % os.pardir)
    print("부모 디렉토리로 변경[%s]" % os.chdir(os.pardir))
#     print("변경후 현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
    print("ArkChatFramework디렉토리 [%s]" % os.path.abspath("ArkChatFramework"))
    
    
    print("intents 파일 디렉토리[%s]" % os.path.abspath("ArkNLU/DialogIntents/intents_home_kr.json"))

    input_file_name = os.path.abspath("ArkNLU/DialogIntents/intents_home_kr.json")
    print("intents       파일 디렉토리[%s]" % input_file_name)
    
    input_training_data_file_name = os.path.abspath("ArkNLU/NLUModel/training_data_home_kr")
    print("training      파일 디렉토리[%s]" % input_training_data_file_name)
    
    tflearn_logs_dir = os.path.abspath('ArkNLU/NLUModel/home_tflearn_kr_logs')
    print("tflearn_logs     디렉토리[%s]" % tflearn_logs_dir)
    
    tflearn_model_file_name = os.path.abspath('ArkNLU/NLUModel/model_home_kr.tflearn')
    print("tflearn_model 파일 디렉토리[%s]" % tflearn_model_file_name)
    
#     intents_file, training_data_file, tflearn_logs_dir, tflearn_model_file
    learning_model_files = dict(intents_file=input_file_name, 
                                training_data_file=input_training_data_file_name, 
                                tflearn_logs_dir=tflearn_logs_dir, 
                                tflearn_model_file=tflearn_model_file_name)

    bot = ChatClient('ko-KR', learning_model_files)
    print("ChatClient instance...")
#     bot.read_dialog_intents_jsonfile()
#     bot.restore_training_data_structures()
#     bot.restore_training_model()
    
    userID = 'arkwith7'
    sentence = '미션이 무엇입니까?'
     
    results = bot.get_classify(sentence)
    print("미션이 무엇입니까? 사용자의도분류[%s]" % results)
 
    # 대화 말뭉치와 대화 의도가 정의된 JSON 문서 집합 읽기
    print("미션이 무엇입니까? 응답[%s]" % bot.response(sentence, userID, show_details=True))

def test_NLULearning():

    print("현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
    print("부모 디렉토리로 변경[%s]" % os.chdir(os.pardir))
    print("변경후 현재 프로세스의 작업 디렉토리 [%s]" % os.getcwd())
 
    print("intents 파일 디렉토리[%s]" % os.path.abspath("ArkNLU/DialogIntents/intents_home_kr.json"))

    input_file_name = os.path.abspath("ArkNLU/DialogIntents/intents_home_kr.json")
    print("intents       파일 디렉토리[%s]" % input_file_name)
    
    input_training_data_file_name = os.path.abspath("ArkNLU/NLUModel/training_data_home_kr")
    print("training      파일 디렉토리[%s]" % input_training_data_file_name)
    
    tflearn_logs_dir = os.path.abspath('ArkNLU/NLUModel/home_tflearn_kr_logs')
    print("tflearn_logs     디렉토리[%s]" % tflearn_logs_dir)
    
    tflearn_model_file_name = os.path.abspath('ArkNLU/NLUModel/model_home_kr.tflearn')
    print("tflearn_model 파일 디렉토리[%s]" % tflearn_model_file_name)

#     intents_file, training_data_file, tflearn_logs_dir, tflearn_model_file
    learning_model_files = dict(intents_file=input_file_name, 
                                training_data_file=input_training_data_file_name, 
                                tflearn_logs_dir=tflearn_logs_dir, 
                                tflearn_model_file=tflearn_model_file_name)

    bot = ChatClient('ko-KR', learning_model_files)
    print("NLULearning instance...")
    
    if bot.create_learning_model(show_details=True):
        print("model creation success....")
    else:
        print("model creation fail....")
        
    
    
# Start process
if __name__ == '__main__':
#     test_ChatClient()
    test_NLULearning()
#     pwd = os.getcwd()
#     for (path, dirs, files) in os.walk(pwd):
#         for dirname in dirs:
#             if dirname == 'ArkChatFramework':
#                 print("[%s]==>%s" % (dirs, os.path.abspath("ArkChatFramework")))
#                 break
