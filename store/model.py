# -*- coding: utf-8 -*-

from collections import namedtuple


class Question(object):

    def __init__(self, ques_id, url, title, description, follower, views, comments, answer_file):

        self.questionid = ques_id
        self.title = title
        self.description = description
        self.follower = follower
        self.views = views
        self.comments = comments
        self.answers = answer_file
        self.url = url

    def to_csv_line(self):
        line = ['%s'] * 8
        line = ','.join(line)
        line = line % (self.questionid, self.title, self.description, self.follower, self.views, self.comments,
                       self.url, self.answers)

        return line


class Answer(object):

    def __init__(self, question, name, user_tag, content, ups, comments):

        self.question = question
        self.name = name
        self.user_tag = user_tag
        self.content = content
        self.ups = ups
        self.comments = comments

    def __str__(self):

        s = "[回答者]:%s\n[回答者标签]:%s\n[内容]:%s\n[赞同数]:%s\n[评论数]:%s\n" % \
            (self.name, self.user_tag, self.content, self.ups, self.comments)
        return s

    def question(self):
        return self.question


class Topic(object):

    def __init__(self, topic_id, title, topic_type, questions, question_user, question_answer, question_comments):

        self.topic_id = topic_id
        self.title = title
        self.topic_type = topic_type
        self.questions = zip(questions, question_user, question_answer, question_comments)


class Person(object):

    def __init__(self, name, signature, tag, counters, achievements, cares, activities):
        self.name = name
        self.signature = signature
        self.tag = tag
        self.answer_num = counters[0]
        self.question_num = counters[1]
        self.article_num = counters[2]
        self.zhuanlan_num = counters[3]
        self.thoughts_num = counters[4]

        self.ups = achievements[0]
        self.thanks = achievements[1]
        self.collected = achievements[2]
        self.edits = achievements[3]
        self.following = achievements[4]
        self.followers = achievements[5]

        self.follow_topics = cares[0]
        self.follow_zhuanlan = cares[1]
        self.follow_questions = cares[2]
        self.collection = cares[3]

        self.activities = activities

    def to_csv_line(self):
        """
        提供写入csv
        :return:
        """
        activity = ''
        for i in xrange(len(self.activities[0])):
            activity += self.activities[0][i] + ':' + self.activities[1][i] + '\n'

        line = ['%s'] * 19
        line = ','.join(line)
        line = line % (self.name, self.signature, self.tag, self.answer_num, self.question_num,
                       self.article_num, self.zhuanlan_num, self.thoughts_num, self.ups,
                       self.thanks, self.collected, self.edits, self.following, self.followers,
                       self.follow_topics, self.follow_zhuanlan, self.follow_questions, self.collection,activity)

        return line

