'''
Created on 2018. 2. 9.

@author: phs

1. ???™” ë§ë­‰ì¹? ?ŒŒ?¼?„ ?½?–´?“¤?¸?‹¤.
2. ?”¥?Ÿ¬?‹(tensorflow) ëª¨ë¸ ?ƒ?„±?— ?‚¬?š©?•œ ?žë£Œêµ¬ì¡°ë?? ?½?–´ ?“¤?—¬?„œ ë°˜í™˜?•œ?‹¤.
3. ?”¥?Ÿ¬?‹(tensorflow)?œ¼ë¡? ?ƒ?„±?•œ ?ž?—°?–´ ?´?•´ ëª¨ë¸?„ ?½?–´?“¤?—¬?„œ ë°˜í™˜?•œ?‹¤.
4. ?ž…? ¥ë°›ì? ë¬¸ìž¥?„ ?ž?—°?–´ ì²˜ë¦¬?•œ?‹¤(?† ?¬?‚˜?´??, ?Š¤?ƒœë°?).
5. ?ž?—°?–´ ì²˜ë¦¬?•œ ë¬¸ìž¥?„ Bag of word ?ƒ?„±?•˜?—¬ ë°˜í™˜?•œ?‹¤.
6. ?ž…? ¥ë°›ì? ë¬¸ìž¥?„ ?•™?Šµ ëª¨ë¸(?ž?—°?–´ ?´?•´ ëª¨ë¸)?„ ?´?š© ë¶„ë¥˜?•˜?—¬  ê²°ê³¼ë¥? ë°˜í™˜?•œ?‹¤.
7. ë¶„ë¥˜?œ ë§ë­‰ì¹? ???™”?—?„œ ?ž„?˜ë¡? ?•œ ë¬¸ìž¥?„ ?„ ?ƒ?•˜?—¬ ?ž…? ¥ë°›ì? ë¬¸ìž¥?˜ ???‹µ?œ¼ë¡? ë°˜í˜¼?•œ?‹¤.

'''
# things we need for NLP
import json
import os
import pickle
import random
import sys

import nltk
from nltk.stem.lancaster import LancasterStemmer
import tflearn

import numpy as np


stemmer = LancasterStemmer()

os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"


for i in range(3):    # Add this for loop.
    sys.stdout.write('\033[F') # Back to previous line.
    sys.stdout.write('\033[K') # Clear line.

# things we need for Tensorflow

# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.25


# import our chat-bot intents file
def read_dialog_intents_jsonfile(input_file_name):
    """
     ???™” ë§ë­‰ì¹? ?ŒŒ?¼?„ ?½?–´?“¤?¸?‹¤.
    """
    with open(input_file_name) as json_data:
        intents = json.load(json_data)
        
    return intents


# restore all of our data structures
def restore_training_data_structures(input_training_data_file_name):
    """
     ?”¥?Ÿ¬?‹(tensorflow) ëª¨ë¸ ?ƒ?„±?— ?‚¬?š©?•œ ?žë£Œêµ¬ì¡°ë?? ?½?–´ ?“¤?—¬?„œ ë°˜í™˜?•œ?‹¤.
    """
    # restore all of our data structures
    data = pickle.load( open( input_training_data_file_name, "rb" ) )
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']
    
    return classes, words, train_x, train_y

# restore all of trained tflearn model file
def restore_training_model(train_x, train_y, tflearn_logs_dir, tflearn_model_file_name):
    """
     ?”¥?Ÿ¬?‹(tensorflow)?œ¼ë¡? ?ƒ?„±?•œ ?ž?—°?–´ ?´?•´ ëª¨ë¸?„ ?½?–´?“¤?—¬?„œ ë°˜í™˜?•œ?‹¤.
    """
    # Build neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)
    
    # Define model and setup tensorboard
    model = tflearn.DNN(net, tensorboard_dir=tflearn_logs_dir)

    # load our saved model
    model.load(tflearn_model_file_name)

    return model


def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
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

    # ???™” ë§ë­‰ì¹˜ì? ???™” ?˜?„ê°? ? •?˜?œ JSON ë¬¸ì„œ ì§‘í•© ?½ê¸?
    input_file_name = '../ArkNLU/DialogIntents/intents.json'
    intents = read_dialog_intents_jsonfile(input_file_name)

    #  ?”¥?Ÿ¬?‹(tensorflow) ëª¨ë¸ ?ƒ?„±?— ?‚¬?š©?•œ ?žë£Œêµ¬ì¡°ë?? ?½?–´?“¤?ž„
    input_training_data_file_name = "../ArkNLU/NLUModel/training_data"
    classes, words, train_x, train_y = restore_training_data_structures(input_training_data_file_name)

    #  ?”¥?Ÿ¬?‹(tensorflow)?œ¼ë¡? ?ƒ?„±?•œ ?ž?—°?–´ ?´?•´ ëª¨ë¸?„ ?½?–´?“¤?ž„
    tflearn_logs_dir = '../ArkNLU/tflearn_logs'
    tflearn_model_file_name = '../ArkNLU/NLUModel/model.tflearn'
    model = restore_training_model(train_x, train_y, tflearn_logs_dir, tflearn_model_file_name)

    sentence = 'is your shop open today?'
    print("classify('is your shop open today?')[{}]".format(classify(sentence, words, classes, model)))
    print("response('is your shop open today?') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()
    
    sentence = 'do you take cash?'
    print("response('do you take cash?') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()
    
    sentence = 'what kind of mopeds do you rent?'
    print("response('what kind of mopeds do you rent?') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()
    
    sentence = 'Goodbye, see you later'
    print("response('Goodbye, see you later') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()

    print("context1")
    for key, value in context.items():
        print("context[{}:{}]".format(key, value))
        print()

    sentence = 'we want to rent a moped'
    print("response('we want to rent a moped') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()

    # show context
    print("context2")
    for key, value in context.items():
        print("context[{}:{}]".format(key, value))
        print()

    sentence = 'is your shop open today?'
    print("classify('today')[{}]".format(classify(sentence, words, classes, model)))
    print()
    print("response('today') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()

    # clear context
    print()
    sentence = 'Hi there!'
    print("response(Hi there!, show_details=True) ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()

    sentence = 'today'
    print("response('today') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    print()
    print("classify('today')[{}]".format(classify(sentence, words, classes, model)))
    print()
   
    sentence = 'thanks, your great'
    print("response('thanks, your great') ==> [{}]".format(response(sentence, intents, words, classes, model)))
    