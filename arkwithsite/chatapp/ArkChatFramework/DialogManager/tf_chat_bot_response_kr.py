'''
Created on 2018. 2. 14.

@author: phs


'''
# things we need for NLP
import json
import os
import pickle
import random

import jpype
from konlpy.tag import Twitter
import tflearn

import numpy as np


# import nltk
# from nltk.stem.lancaster import LancasterStemmer
# stemmer = LancasterStemmer()
# from konlpy.tag import Komoran
# konlpy Django?? ?���??? ?�� ?�� python.exe ?��?��?��방을 ?��?��
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.25

# import our chat-bot intents file
def read_dialog_intents_jsonfile(input_file_name):
    """
    """
    with open(input_file_name) as json_data:
        intents = json.load(json_data)
        
    return intents


# restore all of our data structures
def restore_training_data_structures(input_training_data_file_name):
    """
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
#     print ("tf_chat_bot_response_kr clean_up_sentence start....")
    # komoran = Komoran()
    # konlpy Django?? ?���??? ?�� ?�� python.exe ?��?��?��방을 ?��?��
    if jpype.isJVMStarted():
        jpype.attachThreadToJVM()

    try:
        twitter = Twitter()
    except Exception as e:
        print ("tf_chat_bot_response_kr clean_up_sentence Twitter() error [%s]" % e)
    # tokenize the pattern
#     sentence_words = nltk.word_tokenize(sentence)
    try:
        pos_result = twitter.pos(sentence, norm=True, stem=True)
    except Exception as e:
        print ("tf_chat_bot_response_kr clean_up_sentence twitter error [%s]" % e)
        
#     print ("tf_chat_bot_response_kr clean_up_sentence pos_result[%s]" % pos_result)
    sentence_words = [lex for lex, pos in pos_result]
    # stem each word
#     sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    print ("tf_chat_bot_response_kr clean_up_sentence [%s]" % sentence_words)
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
#     print ("tf_chat_bot_response_kr bow start....")
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
#     print ("tf_chat_bot_response_kr classify start....")
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
#     print ("tf_chat_bot_response_kr classify model.predict [%s]" % results)
    # filter out predictions below a threshold 0.25
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, intents, results, userID='123', show_details=False):
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



if __name__ == '__main__':

    
    input_file_name = '../ArkNLU/DialogIntents/intents_kr.json'
    intents = read_dialog_intents_jsonfile(input_file_name)

    input_training_data_file_name = "../ArkNLU/NLUModel/training_data_kr"
    classes, words, train_x, train_y = restore_training_data_structures(input_training_data_file_name)

    tflearn_logs_dir = '../ArkNLU/tflearn_logs'
    model = restore_training_model(train_x, train_y, tflearn_logs_dir)

    # load our saved model
    tflearn_model_file_name = '../ArkNLU/NLUModel/model_kr.tflearn'
    model.load(tflearn_model_file_name)


    