'''
Created on 2018. 2. 9.

@author: phs
'''
import sys, json

from DialogManager.tf_chat_bot_response import *


#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    json_data = json.loads(lines[0])
    return json_data

def main():
    #get our data as an array from read_in()
    question = read_in()
    sentence = question.get('message')
    userID = question.get('userId')
    # ???�� 말뭉치�? ???�� ?��?���? ?��?��?�� JSON 문서 집합 ?���?
    input_file_name = '../ArkNLU/DialogIntents/intents.json'
    intents = read_dialog_intents_jsonfile(input_file_name)

    #  ?��?��?��(tensorflow) 모델 ?��?��?�� ?��?��?�� ?��료구조�?? ?��?��?��?��
    input_training_data_file_name = "../ArkNLU/NLUModel/training_data"
    classes, words, train_x, train_y = restore_training_data_structures(input_training_data_file_name)

    #  ?��?��?��(tensorflow)?���? ?��?��?�� ?��?��?�� ?��?�� 모델?�� ?��?��?��?��
    tflearn_logs_dir = '../ArkNLU/tflearn_logs'
    tflearn_model_file_name = '../ArkNLU/NLUModel/model.tflearn'
    model = restore_training_model(train_x, train_y, tflearn_logs_dir, tflearn_model_file_name)

#     sentence = 'is your shop open today?'
#     print("classify('is your shop open today?')[{}]".format(classify(sentence, words, classes, model)))
    answer = response(sentence, intents, words, classes, model, userID)

    print(answer)

# Start process
if __name__ == '__main__':
    main()
