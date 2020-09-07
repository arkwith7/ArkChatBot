'''
Created on 2018. 2. 14.

@author: phs
'''



import os
import random

from chatapp.ArkChatFramework.DialogManager import tf_chat_bot_response_kr


#Read data from stdin
# def read_in():
#     lines = sys.stdin.readlines()
#     json_data = json.loads(lines[0])
#     return json_data
context = {}
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def get_intents():
    # 대화 말뭉치와 대화 의도가 정의된 JSON 문서 집합 읽기
#     input_file_name = '../ArkNLU/DialogIntents/intents_kr.json'
    input_file_name = os.path.join(BASE_DIR, "ArkNLU/DialogIntents/intents_kr.json")
    intents = tf_chat_bot_response_kr.read_dialog_intents_jsonfile(input_file_name)
#     print ("input_file_name [%s]" % input_file_name )#파일이 위치한 디렉토리
    return intents

def get_classify(sentence):
    print ("bot_response_kr [%s]" % os.getcwd()) #현재 디렉토리의
#     print ("bot_response_kr [%s]" % os.path.dirname(os.path.realpath(__file__)) )#파일이 위치한 디렉토리
    print ("bot_response_kr BASE_DIR[%s]" % os.path.dirname(BASE_DIR) )#파일이 위치한 디렉토리


    #  딥러닝(tensorflow) 모델 생성에 사용한 자료구조를 읽어들임
    input_training_data_file_name = os.path.join(BASE_DIR, "ArkNLU/NLUModel/training_data_kr")
    classes, words, train_x, train_y = tf_chat_bot_response_kr.restore_training_data_structures(input_training_data_file_name)
#     print ("input_training_data_file_name [%s]" % input_training_data_file_name )#파일이 위치한 디렉토리

    #  딥러닝(tensorflow)으로 생성한 자연어 이해 모델을 읽어들임
    tflearn_logs_dir = os.path.join(BASE_DIR, 'ArkNLU/NLUModel/tflearn_kr_logs')
    model = tf_chat_bot_response_kr.restore_training_model(train_x, train_y, tflearn_logs_dir)
#     print ("tflearn_logs_dir [%s]" % tflearn_logs_dir )#파일이 위치한 디렉토리

    # load our saved model
    tflearn_model_file_name = os.path.join(BASE_DIR, 'ArkNLU/NLUModel/model_kr.tflearn')
    model.load(tflearn_model_file_name)
#     print ("tflearn_model_file_name [%s]" % tflearn_model_file_name )

#     answer = tf_chat_bot.response(sentence, intents, words, classes, model, userID)
    results = tf_chat_bot_response_kr.classify(sentence, words, classes, model)
#     print ("results [%s]" % results )#파일이 위치한 디렉토리

    return results

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

# Start process
if __name__ == '__main__':
    userID = 'arkwith7'
    sentence = '오늘 가게문 여나요?'
    
    results = get_classify(sentence)
    print("오늘 가게문 여나요? 사용자의도분류[%s]" % results)

    # 대화 말뭉치와 대화 의도가 정의된 JSON 문서 집합 읽기
    intents = get_intents()
    print("오늘 가게문 여나요? 응답[%s]" % get_answer(sentence, intents, results))
