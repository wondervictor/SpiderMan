# -*- coding: utf-8 -*-

"""

Store data in the Sqlite3 Database

Table1



"""
import os
import sys
import sqlite3

from common import log
from model import Question, Answer

DB_PATH = 'spiderman.db'

logger = log.Logger(name='store')

def init_all_dbs():
    """
    call it when creating database
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    exec_sql = "create table Question (id INTEGER primary key, content text, user VARCHAR(20), date VARCHAR(30))"
    cursor.execute(exec_sql)
    exec_sql = "create table People (id INTEGER primary key, question_id INTEGER, content text, user VARCHAR(20), date VARCHAR(30))"
    cursor.execute(exec_sql)
    conn.commit()
    conn.close()


def store_to_file(filename, question, answers):

    f = open(filename, 'w+')
    f.write(question)
    for ans in answers:
        f.write(ans)
    f.close()
    logger.info("Saved to file %s" % filename)


def store_new_question(question):

    assert isinstance(question, Question), "param `question` should be model.Question's instance"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "INSERT into Question (id, content, user, date) VALUES (%s, %s, %s, %s)" % question()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def store_answers(ques_id, answers):
    """
    :param ques_id: 问题ID
    :param answers: 回答
    :type answers: [Answer] list object
    :return:
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    def part(answer):
        assert isinstance(answer, Answer), "param `answer` should be model.Answer's instance"
        sql = "INSERT into Answer (id, question_id, content, user, date) VALUES (%s, %s, %s, %s, %s)" % answer()
        cursor.execute(sql)

    for answer in answers:

        part(answer)

    conn.commit()
    conn.close()

""""
f.write(u'人物昵称:\t'+information[0]+'\n')
            f.write(u'人物签名:\t'+information[1]+'\n')
            f.write(u'人物标签:\t'+information[2]+'\n')
            f.write(u'回答数:\t\t'+information[3]+'\n')
            f.write(u'提问数:\t\t'+information[4]+'\n')
            f.write(u'文章数:\t\t'+information[5]+'\n')
            f.write(u'专栏数:\t\t'+information[6]+'\n')
            f.write(u'想法数:\t\t'+information[7]+'\n')
            f.write('\n'+u'个人成就:'+'\n')
            f.write(u'总赞同数:\t'+achieve[0]+'\n')
            f.write(u'总感谢数:\t'+achieve[1]+'\n')
            f.write(u'总收藏数:\t'+achieve[2]+'\n')
            f.write(u'总编辑数:\t'+achieve[3]+'\n')
            f.write(u'总关注数:\t'+achieve[4]+'\n')
            f.write(u'被关注数:\t'+achieve[5]+'\n')
            f.write('\n'+u'关注的信息:'+'\n')
            f.write(u'话题:\t\t'+care[0]+'\n')
            f.write(u'专栏:\t\t'+care[1]+'\n')
            f.write(u'问题:\t\t'+care[2]+'\n')
            f.write(u'收藏夹:\t\t'+care[3]+'\n')
            f.write('\n'+u'动态:'+'\n')
            for i in range(len(activity[0])):
                f.write(activity[0][i]+u':\t'+activity[1][i]+'\n')
"""


def init_people_file(directory):

    if directory[-1] != '/':
        directory += '/'
    path = directory + 'people.csv'

    if not os.path.exists(path):

        columns = [u'人物昵称', u'人物签名', u'人物标签', u'回答数', u'提问数', u'文章数', u'专栏数', u'想法数',
                   u'总赞同数', u'总收藏数', u'总编辑数', u'总关注数', u'被关注数', u'关注话题', u'关注专栏', u'关注问题',
                   u'收藏夹', u'动态']
        with open(path, 'w+') as f:
            line = ','.join(columns)
            line += '\n'
            f.write(line)

        logger.info("Created people information file: %s" % path)

def init_question_file(directory):

    if directory[-1] != '/':
        directory += '/'
    path = directory + 'question.csv'

    if not os.path.exists(path):

        columns = [u'问题ID', u'问题标题', u'问题描述', u'问题关注数', u'问题浏览数', u'问题评论数', u'URL', u'回答文件']

        with open(path, 'w+') as f:
            line = ','.join(columns)
            line += '\n'
            f.write(line)

        logger.info("Created question information file: %s" % path)


def save_file(path, content_type, content, filetype='csv'):

    if content_type == 'people':
        # 存储用户信息
        pass








