'''
Created on 2018. 3. 12.

@author: phs

1. ???�� 말뭉�? ?��?��?�� ?��?��?��?��?��.
2. ?��?��?��(tensorflow) 모델 ?��?��?�� ?��?��?�� ?��료구조�?? ?��?�� ?��?��?�� 반환?��?��.
3. ?��?��?��(tensorflow)?���? ?��?��?�� ?��?��?�� ?��?�� 모델?�� ?��?��?��?��?�� 반환?��?��.
4. ?��?��받�? 문장?�� ?��?��?�� 처리?��?��(?��?��?��?��??, ?��?���?).
5. ?��?��?�� 처리?�� 문장?�� Bag of word ?��?��?��?�� 반환?��?��.
6. ?��?��받�? 문장?�� ?��?�� 모델(?��?��?�� ?��?�� 모델)?�� ?��?�� 분류?��?��  결과�? 반환?��?��.
7. 분류?�� 말뭉�? ???��?��?�� ?��?���? ?�� 문장?�� ?��?��?��?�� ?��?��받�? 문장?�� ???��?���? 반혼?��?��.

'''
import json
import os
import pickle
import random

from konlpy.tag import Twitter
import tflearn

import numpy as np


os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

# things we need for NLP

# import nltk
# from nltk.stem.lancaster import LancasterStemmer
# stemmer = LancasterStemmer()

# from konlpy.tag import Komoran
# komoran = Komoran()
twitter = Twitter()


# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.25

# import our chat-bot intents file
def read_dialog_intents_jsonfile(input_file_name):
    """
    input : JSON?��?��경로?? ?��?��?���?
    processing : ???�� ?��?��?? ???�� 말뭉치�? ?��?��?�� JSON?��?��?�� ?��?�� JSON객체?�� ?��?��.
    return : JSON객체
    """
    with open(input_file_name, 'rt', encoding='UTF8') as json_data:
        intents = json.load(json_data)
        
    return intents

# restore all of our data structures
def restore_training_data_structures(input_training_data_file_name):
    """
     ?��?��?��(tensorflow) 모델 ?��?��?�� ?��?��?�� ?��료구조�?? ?��?�� ?��?��?�� 반환?��?��.
    """
    # restore all of our data structures
    data = pickle.load( open( input_training_data_file_name, "rb" ) )
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']
    
    return classes, words, train_x, train_y

# restore all of trained tflearn model file
def restore_training_model(train_x, train_y, tflearn_logs_dir):
    """
     ?��?��?��(tensorflow)?���? ?��?��?�� ?��?��?�� ?��?�� 모델?�� ?��?��?��?��?�� 반환?��?��.
    """
    # Build neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)
    
    # Define model and setup tensorboard
    model = tflearn.DNN(net, tensorboard_dir=tflearn_logs_dir)

    return model

def clean_up_sentence(sentence):
    # tokenize the pattern
#     sentence_words = nltk.word_tokenize(sentence)
    pos_result = twitter.pos(sentence, norm=True, stem=True)
    sentence_words = [lex for lex, pos in pos_result]
    # stem each word
#     sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


def classify(sentence, words, classes, model):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, intents, words, classes, model, userID='123', show_details=False):
    results = classify(sentence, words, classes, model)
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

if __name__ == '__main__':
    # ???�� 말뭉치�? ???�� ?��?���? ?��?��?�� JSON 문서 집합 ?���?
    input_file_name = '../ArkNLU/DialogIntents/intents_home_kr.json'
    intents = read_dialog_intents_jsonfile(input_file_name)
    #  ?��?��?��(tensorflow) 모델 ?��?��?�� ?��?��?�� ?��료구조�?? ?��?��?��?��
    input_training_data_file_name = "../ArkNLU/NLUModel/training_data_home_kr"
    classes, words, train_x, train_y = restore_training_data_structures(input_training_data_file_name)
    #  ?��?��?��(tensorflow)?���? ?��?��?�� ?��?��?�� ?��?�� 모델?�� ?��?��?��?��
    tflearn_logs_dir = "../ArkNLU/home_tflearn_kr_logs"
    model = restore_training_model(train_x, train_y, tflearn_logs_dir)
    # load our saved model
    tflearn_model_file_name = "../ArkNLU/NLUModel/model_home_kr.tflearn"
    model.load(tflearn_model_file_name)

    sentence = '비젼?? 무엇?��?���??'
    print("classify('비젼?? 무엇?��?���??')[%s]" % classify(sentence, words, classes, model))
    print("response('비젼?? 무엇?��?���??') ==> [%s]" % response(sentence, intents, words, classes, model))
    print()
    sentence = '무슨 ?��?��?�� ?��?��?��?'
    print("classify('무슨 ?��?��?�� ?��?��?��?')[%s]" % classify(sentence, words, classes, model))
    print("response('무슨 ?��?��?�� ?��?��?��?') ==> [%s]" % response(sentence, intents, words, classes, model))
    print()
    sentence = '구체?��?�� 기술???'
    print("classify('구체?��?�� 기술???')[%s]" % classify(sentence, words, classes, model))
    print("response('구체?��?�� 기술???') ==> [%s]" % response(sentence, intents, words, classes, model))
    print()
    sentence = '?��?��기술'
    print("classify('?��?��기술')[%s]" % classify(sentence, words, classes, model))
    print("response('?��?��기술') ==> [%s]" % response(sentence, intents, words, classes, model))
    print()
    # clear context
    #response("Hi there!", show_details=True)
    sentence = '?��?��'
    print("response('?��?��?') ==> [%s]" % response(sentence, intents, words, classes, model,show_details=True))
    print("classify('?��?��?')[%s]" % classify(sentence, words, classes, model))
    print()
    sentence = '?��비스기술'
    print("classify('?��비스기술')[%s]" % classify(sentence, words, classes, model))
    print("response('?��비스기술') ==> [%s]" % response(sentence, intents, words, classes, model))
    print()