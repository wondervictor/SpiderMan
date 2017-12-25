# -*- coding: utf-8 -*-

"""

Store data in the Sqlite3 Database

Table1



"""

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
    exec_sql = "create table Answer (id INTEGER primary key, question_id INTEGER, content text, user VARCHAR(20), date VARCHAR(30))"
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


def __test__question():

    pass


def __test__answer():

    pass



