# -*- coding: utf-8 -*-

from snownlp import SnowNLP


def inference(sentence):

    sentence = SnowNLP(sentence)
    prob = sentence.sentiments
    if prob > 0.5:
        return True, prob
    elif prob < 0.5:
        return False, 1-prob
    else:
        return False, 0


def inference_answers(filepath):
    
    pass