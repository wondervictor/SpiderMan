# -*- coding: utf-8 -*-

from collections import namedtuple


class Question(object):

    def __init__(self, ques_id, url, title, description, follower, views, comments, answer_file):
        """
        :param ques_id: 问题ID
        :param url:问题URL
        :param title: 问题标题
        :param description: 问题内容
        :param follower: 问题关注者数量
        :param views: 问题浏览量
        :param comments: 问题评论数
        :param answer_file: 问题回答文件名
        """
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
        """
        :param question: 问题内容
        :param name: 回答者昵称
        :param user_tag: 回答者标签
        :param content: 回答内容
        :param ups: 点赞数
        :param comments: 评论数
        """
        self.question = question
        self.name = name
        self.user_tag = user_tag
        self.content = content
        self.ups = ups
        self.comments = comments

    def __str__(self):

        s = u"[回答者]:%s\n[回答者标签]:%s\n[内容]:%s\n[赞同数]:%s\n[评论数]:%s\n" % \
            (self.name, self.user_tag, self.content, self.ups, self.comments)
        return s

    def question(self):
        return self.question


class Topic(object):

    def __init__(self, topic_id, title, topic_type, questions, question_user, question_answer, question_comments):
        """
        :param topic_id: 话题 ID
        :param title: 话题标题
        :param topic_type: 话题类型
        :param questions: 问题
        :param question_user: 问题答者
        :param question_answer: 问题回答
        :param question_comments: 问题评论
        """
        self.topic_id = topic_id
        self.title = title
        self.topic_type = topic_type
        self.questions = zip(questions, question_user, question_answer, question_comments)


class Person(object):

    def __init__(self, name, signature, tag, counters, achievements, cares, activities):
        """
        :param name: 用户名
        :param signature: 用户签名
        :param tag: 用户标签
        :param counters: 统计量
        :param achievements: 成就
        :param cares: 关注内容
        :param activities: 活动
        """
        self.name = name
        self.signature = signature
        self.tag = tag
        # 回答数
        self.answer_num = counters[0]
        # 提问数
        self.question_num = counters[1]
        # 文章数
        self.article_num = counters[2]
        # 专栏数
        self.zhuanlan_num = counters[3]
        # 想法数
        self.thoughts_num = counters[4]
        # 收到赞
        self.ups = achievements[0]
        # 感谢数
        self.thanks = achievements[1]
        # 收藏数
        self.collected = achievements[2]
        self.edits = achievements[3]
        # 关注人的数量
        self.following = achievements[4]
        # 被关注的数量
        self.followers = achievements[5]
        # 关注的话题
        self.follow_topics = cares[0]
        # 关注的专栏
        self.follow_zhuanlan = cares[1]
        # 关注的问题
        self.follow_questions = cares[2]
        self.collection = cares[3]
        # 活动
        self.activities = activities

    def to_line(self):
        """
        提供写入csv
        :return:
        """
        activity = ''
        for i in xrange(min(len(self.activities[0]), len(self.activities[1]))):
            activity += self.activities[0][i] + ':' + self.activities[1][i] + '\n'

        return (self.name, self.signature, self.tag, self.answer_num, self.question_num, self.article_num,
                self.thanks, self.collected, self.edits, self.following, self.followers,self.follow_topics,
                self.follow_zhuanlan, self.follow_questions, self.collection, activity)


