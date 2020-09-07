'''
Created on 2018. 2. 14.

@author: phs
'''



import sys, json

import DialogManager.tf_chat_bot_response_kr as chat_bot


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
    project_path = question.get('projectPath')

    # ???™” ë§ë­‰ì¹˜ì? ???™” ?˜?„ê°? ? •?˜?œ JSON ë¬¸ì„œ ì§‘í•© ?½ê¸?
    input_file_name = project_path + 'ArkChatFramework/ArkNLU/DialogIntents/intents_kr.json'
    intents = chat_bot.read_dialog_intents_jsonfile(input_file_name)

    #  ?”¥?Ÿ¬?‹(tensorflow) ëª¨ë¸ ?ƒ?„±?— ?‚¬?š©?•œ ?ë£Œêµ¬ì¡°ë?? ?½?–´?“¤?„
    input_training_data_file_name = project_path + "ArkChatFramework/ArkNLU/NLUModel/training_data_kr"
    classes, words, train_x, train_y = chat_bot.restore_training_data_structures(input_training_data_file_name)

    #  ?”¥?Ÿ¬?‹(tensorflow)?œ¼ë¡? ?ƒ?„±?•œ ??—°?–´ ?´?•´ ëª¨ë¸?„ ?½?–´?“¤?„
    tflearn_logs_dir = project_path + 'ArkChatFramework/ArkNLU/tflearn_kr_logs'
    tflearn_model_file_name = project_path + 'ArkChatFramework/ArkNLU/NLUModel/model_kr.tflearn'
    model = chat_bot.restore_training_model(train_x, train_y, tflearn_logs_dir, tflearn_model_file_name)

#     sentence = 'is your shop open today?'
#     print("classify('is your shop open today?')[{}]".format(classify(sentence, words, classes, model)))
    answer = chat_bot.response(sentence, intents, words, classes, model, userID)

    print(answer)

# Start process
if __name__ == '__main__':
    main()
