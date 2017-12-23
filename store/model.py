# -*- coding: utf-8 -*-


class Question(object):

    def __init__(self, ques_id, content, user, date):
        """

        :param ques_id: 问题ID
        :param content: 问题内容
        :param user: 提问者
        :param date: 日期
        """

        self._id = ques_id
        self._content = content
        self._user = user
        self._date = date

    def __call__(self, *args, **kwargs):
        s = (self._id, self._content, self._user, self._date)
        return s

    def __str__(self):

        s = "[ID] %s\n[问题] %s\n[提问者] %s\n[日期] %s\n" % (self._id, self._content, self._user, self._date)
        return s


class Answer(object):

    def __init__(self, ques_id, answer_id, content, user, date):
        """

        :param ques_id: 问题ID
        :param answer_id: 回答ID
        :param content: 回答内容
        :param user: 回答用户
        :param date: 日期
        """
        self._ques_id = ques_id
        self._content = content
        self._user = user
        self._date = date
        self._id = answer_id

    def __call__(self, *args, **kwargs):
        s = (self._id, self._ques_id, self._content, self._user, self._date)
        return s

    def __str__(self):

        s = "[回答者]%s\n[日期]%s\n[内容]%s\n" % (self._user, self._date,self._content)
        return s


class Topic(object):

    def __init__(self, topic_id, content, url, questionids):

        """

        :param topic_id:  Topic ID
        :param url: Topic URL
        :param content: topic content
        :param questions: question ids in Topic
        """

        self._id = topic_id
        self._questions = questionids
        self._url = url
        self._content = content

    def __call__(self, *args, **kwargs):
        s = (self._id, self._content, self._url, self._questions)
        return s
