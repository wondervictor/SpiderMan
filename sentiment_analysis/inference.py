# -*- coding: utf-8 -*-
import codecs
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


def inference_answers(filepath, save_path):

    """
    Answer:
    :param filepath:
    :return:
    """

    with open(filepath, 'r') as f:
        raw_content = f.read()

    content = raw_content.split('\n\n')
    title = content[0]
    content = content[1:-2]

    result = list()
    result.append(title)

    for con in content:
        ans = con.split('\n')[2]
        ans = ans.replace('[内容]:','')
        prob = SnowNLP(ans).sentiments
        con += '\n[正面情感概率]: %s\n' % prob
        result.append(con)
    content = '\n'.join(result)

    with codecs.open(save_path, 'a+') as f:
        f.write(content)

