'''
Created on 2018. 2. 14.

@author: phs
'''
"""
1.???�� 말뭉�? ?��?��?�� ?��?��?��?��?��.
2.???�� 말뭉치�?? ?��?��?�� ?��?��?�� 처리 �?  Bag of word ?��?��
3.Bag of word�? ?��?��?�� ?��고리�? ?��?��?�� ?��?�� ?��?��?���? �??��
4.?��?��?��(tensorflow)?�� ?��?�� ?��?��?�� ?��?�� 모델 ?��?��
5.?��?��?�� ?��?�� 모델?�� �?리한?��(???��,?���?)
"""
# things we need for NLP
import json
import pickle
import random

from konlpy.tag import Twitter
import tflearn

import numpy as np
import tensorflow as tf


# import nltk
# from nltk.stem.lancaster import LancasterStemmer
# stemmer = LancasterStemmer()
# from konlpy.tag import Komoran
# komoran = Komoran()
twitter = Twitter()



# things we need for Tensorflow
# import our chat-bot intents file
# save all of our data structures

def read_dialog_intents_jsonfile(input_file_name):
    """
     ???�� 말뭉�? ?��?��?�� ?��?��?��?��?��.
    """
    with open(input_file_name) as json_data:
        intents = json.load(json_data)
        
    return intents
    
def dialog_nlp_processing(intents):
    """
     ???�� 말뭉치�?? ?��?��?�� ?��?��?�� 처리 �?  Bag of word ?��?��
    """
    words = []
    classes = []
    documents = []
    ignore_words = ['?']
    # loop through each sentence in our intents patterns
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # tokenize each word in the sentence
#             w = nltk.word_tokenize(pattern)
            pos_result = twitter.pos(pattern, norm=True, stem=True)
            w = [lex for lex, pos in pos_result]
            # add to our words list
            words.extend(w)
            # add to documents in our corpus
            documents.append((w, intent['tag']))
            # add to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
    
    # stem and lower each word and remove duplicates
#     words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
#     words = sorted(list(set(words)))
    words = [w for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    
    # remove duplicates
    classes = sorted(list(set(classes)))
    
    return classes, documents, words

def prepare_machine_learning(classes, documents, words):
    """
    Bag of word�? ?��?��?�� ?��고리�? ?��?��?�� ?��?�� ?��?��?���? �??��
    """
    
    # create our training data
    training = []
    output_row = []
    # create an empty array for our output
    output_empty = [0] * len(classes)
    
    # training set, bag of words for each sentence
    for doc in documents:
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # stem each word
#         pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        # create our bag of words array
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)
    
        # output is a '0' for each tag and '1' for current tag
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
    
        training.append([bag, output_row])
    
    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)
    
    # create train and test lists
    train_x = list(training[:,0])
    train_y = list(training[:,1])

    return train_x, train_y

def create_tensorflow_learning_model(train_x, train_y, output_model_file_name):
    """
    ?��?��?��(tensorflow)?�� ?��?�� ?��?��?�� ?��?�� 모델 ?��?��
    """
    
    # reset underlying graph data
    tf.reset_default_graph()
    # Build neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)
    
    # Define model and setup tensorboard
    model = tflearn.DNN(net, tensorboard_dir='tflearn_kr_logs')
    # Start training (apply gradient descent algorithm)
    model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
    # save the trained model to directory
    model.save(output_model_file_name)

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

# save all of our data structures
def save_training_data_structures(words, classes, train_x, train_y, output_training_data_file_name):
    """
    ?��?��?�� ?��?�� 모델?�� �?리한?��(???��,?���?)
    """
    # save all of our data structures
    pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( output_training_data_file_name, "wb" ) )


if __name__ == '__main__':
    
    # ???�� 말뭉�? ?��?��?�� ?��?��?��?��?��.
    input_file_name = 'DialogIntents/intents_kr.json'
    intents = read_dialog_intents_jsonfile(input_file_name)
    
    # ???�� 말뭉치�?? ?��?��?�� ?��?��?�� 처리 �?  Bag of word ?��?��
    classes, documents, words = dialog_nlp_processing(intents)
    print (len(documents), "documents")
    print (len(classes), "classes", classes)
    print (len(words), "unique stemmed words", words)
    
    # Bag of word�? ?��?��?�� ?��고리�? ?��?��?�� ?��?�� ?��?��?���? �??��
    train_x, train_y = prepare_machine_learning(classes, documents, words)
    
    # ?��?��?��(tensorflow)?�� ?��?�� ?��?��?�� ?��?�� 모델 ?��?��
    output_model_file_name = 'NLUModel/model_kr.tflearn'
    model = create_tensorflow_learning_model(train_x, train_y, output_model_file_name)

    # ?��?��?�� ?��?�� 모델?�� �?리한?��(???��,?���?)
    output_training_data_file_name = "NLUModel/training_data_kr"
    save_training_data_structures(words, classes, train_x, train_y, output_training_data_file_name)
    
    p = bow("?��?�� �?�?  ?��?��?��?", words)
    print("p is Bag of word for '?��?�� �?�?  ?��?��?��?' :{}".format(p))
    print("classes :{}".format(classes))
    print("model.predict([p]) :{}".format(model.predict([p])))
    