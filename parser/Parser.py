# -*- coding:utf-8 -*-
import codecs
from bs4 import BeautifulSoup as BS
import re
# 需要爬取问题本体，问题的提出者，浏览次数，点赞次数，答案，答案的作者，答案的评论，答案获得的点赞数

# re.compile(r'(http|https)://www.zhihu.com/search?.*?').match(url):


class Search:
    text = None

    def __init__(self, text):
        self.text = BS(text, 'lxml')

    def clean(self, text):
        return text.replace(' ', '').replace('\n', '').replace('\t', '')

    def getquestion(self):
        data = self.text
        # get contents in 'title'
        questions = data.find('title').text

        # 分割得到的结果
        question = re.compile(u'(.*?)- 搜索结果.*?').match(questions)
        if question:
            judge = re.compile('(.*?),Victor Chan.*?').match(question.group(1))
            if judge:
                return judge.group(1)
            else:
                return question.group(1)
        else:
            return questions

    def getlive(self):
        data = self.text

        # 得到live的标题和网页
        lives = data(href=re.compile('lives'))
        if lives:
            for live in lives:
                # get the correct label
                if live.span:
                    title = self.clean(live.text)
                    url = live['href']
            return [url, title]
        else:
            return []

    def gettopic(self):
        data = self.text

        # 得到话题的标题和网页
        topics = data(class_=re.compile('TopicLink'))
        if topics:
            for topic in topics:
                if topic.span:
                    title = self.clean(topic.text)
                    url = 'https://www.zhihu.com'+topic['href']
            return [url, title]
        else:
            return []

    def getzhuanlan(self):
        data = self.text

        # 得到专栏的标题和网页
        columns = data(class_=re.compile('ColumnLink'))
        if columns:
            for column in columns:
                if column.span:
                    title = self.clean(column.text)
                    url = 'https:'+column['href']
            return [url, title]
        else:
            return []

    def getcontent(self):
        # 得到主体内容的标题，作者，简述，赞同数,评论数和网页
        data = self.text
        title = []
        writers = []
        simpletext = []
        url = []
        agree = []
        comment = []

        for tag in data(itemprop=['name', 'article']):
            if tag['itemprop'] == 'name':
                title.append(tag['content'].replace('<em>', '').replace('</em>', ''))
            elif tag['itemprop'] == 'article':
                title.append(self.clean(tag.span.text))

        for tag in data(itemprop=['text', 'articleBody']):
            content = self.clean(tag.text)
            writers.append(content.split(u'：')[0])
            simpletext.append(content.split(u'：')[1])

        for tag in data(itemprop=['url', 'article']):
            if tag['itemprop'] == 'url':
                url.append(tag['content'])
            elif tag['itemprop'] == 'article':
                url.append('https:'+tag.a['href'])

        for tag in data('button', class_=['VoteButton--up', 'LikeButton']):
            agree.append(tag.text)

        for tag in data('button', class_='Button--withLabel'):
            comment.append(tag.text.split(' ')[0])

        return [url, title, writers, simpletext, agree, comment]

    def geturl(self):
        url1 = self.getlive()
        if url1:
            url1 = [url1[0]]

        url2 = self.gettopic()
        if url2:
            url2 = [url2[0]]

        url3 = self.getzhuanlan()
        if url3:
            url3 = [url3[0]]

        url4 = self.getcontent()[0]
        url = url1 + url2 + url3 + url4
        return url

    def total(self):
        question = self.getquestion()
        live = self.getlive()
        topic = self.gettopic()
        zhuanlan = self.getzhuanlan()
        content = self.getcontent()
        url = self.geturl()
        with codecs.open('Search:'+question+'.txt', 'w', 'utf-8')as f:
            f.write(u'搜索的问题：\t'+question+'\n')
            if live:
                f.write(u'知乎live:\t'+live[1]+'\n')
            if topic:
                f.write(u'知乎话题:\t'+topic[1]+'\n')
            if zhuanlan:
                f.write(u'知乎专栏:\t'+zhuanlan[1]+'\n')
            for i in range(len(content[1])):
                f.write('\n'+u'回答标题:\t'+content[1][i]+'\n')
                f.write(u'作者:\t\t'+content[2][i]+'\n')
                f.write(u'回答简述:\t'+content[3][i]+'\n')
                f.write(u'赞同数:\t'+content[4][i]+'\n')
                f.write(u'评论数:\t'+content[5][i]+'\n')

        return url


# re.compile(r'(http|https)://www.zhihu.com/question.*?').match(url):

class Question:
    text = None

    def __init__(self, text):
        self.text = BS(text, 'lxml')

    def clean(self, text):
        return text.replace(' ', '').replace('\n', '').replace('\t', '')

    # 返回问题的标题，主体，关注数，浏览数，评论数，回答数
    def getquestion(self):
        data = self.text

        # 得到问题的标题
        questions = self.clean(data.find('title').text)
        ismatch = re.compile(u'(.*?)-知乎.*?').match(questions)
        if ismatch:
            question = ismatch.group(1)
        else:
            question = questions

        # 得到问题的主体
        text = data(class_='QuestionRichText')
        for tag in text:
            if tag.span:
                content = self.clean(tag.span.text)

        # 得到问题的关注数和浏览数
        information = self.clean(data.find(class_='QuestionFollowStatus-counts').text)
        info = re.compile(u'.*?关注者([0-9]*)被浏览([0-9]*)').match(information)
        if info:
            follows = info.group(1)
            views = info.group(2)
        else:
            follows = 0
            views = 0

        # 得到问题的评论数
        comment = self.clean(data.find(class_='QuestionHeader-Comment').text.split(u'条')[0])
        if re.compile(u'.*?添加评论.*?').match(comment):
            comment = 0

        # 得到问题的答案数
        # answer = self.clean(data.find(class_='List-headerText').text.split(u'个')[0])

        return [question, content, follows, views, comment]

    def getanswer(self):
        data = self.text

        writer = []
        sign = []
        # 得到答案的作者和签名
        for tag in data(class_='AuthorInfo-content'):
            for name in tag(class_='UserLink-link'):
                writer.append(self.clean(name.text))
            for signs in tag(class_='AuthorInfo-badgeText'):
                sign.append(self.clean(signs.text))

        agree = []
        # 得到答案的赞同数
        for tag in data(class_='AnswerItem-extraInfo'):
            agree.append(self.clean(tag.text.split(u'人')[0]))

        content = []
        # 得到答案内容
        for tag in data(class_='CopyrightRichText-richText', itemprop='text'):
            content.append(self.clean(tag.text))

        comment = []
        # 得到答案评论数
        for tag in data('meta', itemprop='commentCount'):
            comment.append(tag['content'])
        comment = comment[1:]

        return [writer, sign, content, agree, comment]

    def geturl(self):
        data = self.text

        url = []
        # 得到网页包含的知乎内部的其他网页
        for tag in data(itemprop='url'):
            url.append(tag['content'])

        return url

    def total(self):
        data = self.text

        # 得到问题，回答，和网页信息
        question = self.getquestion()
        answer = self.getanswer()
        url = self.geturl()
        with codecs.open('Question:'+question[0]+'.txt', 'w', 'utf-8')as f:
            f.write(u'问题标题:\t'+question[0]+'\n')
            f.write(u'问题描述:\t'+question[1]+'\n')
            f.write(u'问题关注数:\t'+question[2]+'\n')
            f.write(u'问题浏览数:\t'+question[3]+'\n')
            f.write(u'问题评论数:\t'+question[4]+'\n')
            for i in range(len(answer[0])):
                f.write('\n'+u'答者昵称:\t'+answer[0][i]+'\n')
                f.write(u'答者标签:\t'+answer[1][i]+'\n')
                f.write(u'答案内容:\t'+answer[2][i]+'\n')
                f.write(u'赞同数:\t'+answer[3][i]+'\n')
                f.write(u'评论数:\t'+answer[4][i]+'\n')

        return url


# re.compile(r'(https|http)://www.zhihu.com/people.*?').match(url)

class People:
    text = None

    def __init__(self, text):
        self.text = BS(text, 'lxml')

    def clean(self, text):
        return text.replace(' ', '').replace('\n', '').replace('\t', '')

    # 得到个人的信息
    def getinformation(self):
        data = self.text

        # 得到名称和签名
        for tag in data(class_='ProfileHeader-title'):
            for names in tag(class_='ProfileHeader-name'):
                name = self.clean(names.text)
            for intros in tag(class_='ProfileHeader-headline'):
                intro = self.clean(intros.text)

        # 得到标签
        tag = self.clean(data.find(class_='ProfileHeader-contentBody').text)

        # 得到各种活动信息
        infor = self.clean(data.find(class_='ProfileMain-tabs').text)
        ismatch = re.compile(u'.*?回答([0-9]*)提问([0-9]*)文章([0-9]*)专栏([0-9]*)想法([0-9]*).*?').match(infor)
        if ismatch:
            replynumber = ismatch.group(1)
            asknumber = ismatch.group(2)
            articlenumber = ismatch.group(3)
            columnnumber = ismatch.group(4)
            thinknumber = ismatch.group(5)
        else:
            replynumber = 0
            asknumber = 0
            articlenumber = 0
            columnnumber = 0
            thinknumber = 0

        return [name, intro, tag, replynumber, asknumber, articlenumber, columnnumber, thinknumber]

    # 得到动态
    def getactivity(self):
        data = self.text

        act = []
        for tag in data(class_='CopyrightRichText-richText'):
            act.append(self.clean(tag.text))

        return act

    # 得到成就信息
    def getachieve(self):
        data = self.text

        # 赞同数，感谢数，收藏数，编辑数
        information = self.clean(data.find(class_='Profile-sideColumnItems').text)
        ismatch = re.compile(u'.*?获得([0-9]*)次赞同获得([0-9]*)次感谢，([0-9]*)次收藏参与([0-9]*)次公共编辑.*?').match(information)
        if ismatch:
            agree = ismatch.group(1)
            thanks = ismatch.group(2)
            collec = ismatch.group(3)
            edit = ismatch.group(4)
        else:
            agree = 0
            thanks = 0
            collec = 0
            edit = 0

        # 关注数和被关注数
        attention = self.clean(data.find(class_='FollowshipCard-counts').text)
        match = re.compile(u'.*?关注了([0-9]*)关注者([0-9]*).*?').match(attention)
        if match:
            care = match.group(1)
            cared = match.group(2)
        else:
            care = 0
            cared = 0

        return [agree, thanks, collec, edit, care, cared]

    # 得到关注的各种信息
    def getcare(self):
        data = self.text

        # 关注的话题，专栏，问题，收藏夹
        information = self.clean(data.find(class_='Profile-lightList').text)
        ismatch = re.compile(u'.*?关注的话题([0-9]*)关注的专栏([0-9]*)关注的问题([0-9]*)关注的收藏夹([0-9]*).*?').match(information)
        if ismatch:
            topic = ismatch.group(1)
            column = ismatch.group(2)
            question = ismatch.group(3)
            collec = ismatch.group(4)
        else:
            topic = 0
            column = 0
            question = 0
            collec = 0

        return [topic, column, question, collec]

    # 得到url
    def geturl(self):
        data = self.text

        url = []
        for tag in data(itemprop='url'):
            url.append(tag['content'])
        return url


    # 汇总各种信息
    def total(self):
        # 个人信息
        information = self.getinformation()
        # 成就信息
        achieve = self.getachieve()
        # 关注信息
        care = self.getcare()
        # 动态信息
        activity = self.getactivity()
        # 网页信息
        url = self.geturl()

        with codecs.open('People:'+information[0]+'.txt', 'w', 'utf-8')as f:
            f.write(u'人物昵称:\t'+information[0]+'\n')
            f.write(u'人物签名:\t'+information[1]+'\n')
            f.write(u'人物标签:\t'+information[2]+'\n')
            f.write(u'回答数:\t'+information[3]+'\n')
            f.write(u'提问数:\t'+information[4]+'\n')
            f.write(u'文章数:\t'+information[5]+'\n')
            f.write(u'专栏数:\t'+information[6]+'\n')
            f.write(u'想法数:\t'+information[7]+'\n')
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
            for i in range(len(activity)):
                f.write('\n'+u'动态:\t\t'+activity[i]+'\n')

        return url


# re.compile(r'(https|http)://www.zhihu.com/topic.*?').match(url)

class Topic:
    text = None

    def __init__(self, text):
        self.text = BS(text, 'lxml')

    def clean(self, text):
        return text.replace(' ', '').replace('\n', '').replace('\t', '')

    # 得到话题的标题
    def gettitle(self):
        data = self.text
        titles = self.clean(data.find('title').text)
        ismatch = re.compile(u'(.*?)-.*?-知乎').match(titles)
        if ismatch:
            title = ismatch.group(1)
        else:
            title = titles
        return title

    # 热门回答
    # 得到信话题信息
    def getinformation(self):
        data = self.text

        url = []
        kata = u'类型'
        questions = []
        names = []
        simpletext = []
        comments = []
        # 得到精华和等待回答页面
        for tag in data(class_='zm-topic-topbar'):
            for jinghuahotanswers in tag(href=re.compile('top-answers')):
                if jinghua:
                    url.append('https://www.zhihu.com'+jinghua['href'])
                    kata = u'热门问题'
            for active in tag(href=re.compile('hot')):
                if active:
                    url.append('https://www.zhihu.com'+active['href'])
                    kata = u'精华问题'

        # 得到问题
        for ques in data(class_='question_link'):
            if ques.text:
                questions.append(self.clean(ques.text))
                url.append('https://www.zhihu.com'+ques['href'])

        # 得到回答者姓名
        for tag in data(class_='zm-item-rich-text expandable js-collapse-body'):
            names.append(tag['data-author-name'])

        # 得到回答者页面
        for tag in data(class_='author-link'):
            url.append('https://www.zhihu.com'+tag['href'])

        # 得到回答简述及答案页面
        for tag in data(class_='zh-summary summary clearfix'):
            if tag.a:
                url.append('https://www.zhihu.com'+tag.a['href'])
            text = self.clean(tag.text)
            ismatch = re.compile(u'(.*?)显示全部').match(text)
            if ismatch:
                simpletext.append(ismatch.group(1))
            else:
                simpletext.append(text)

        # 得到评论数
        for tag in data(class_='toggle-comment'):
            comment = self.clean(tag.text)
            ismatch = re.compile(u'.*?([0-9]*)条评论.*?').match(comment)
            if ismatch:
                comments.append(ismatch.group(1))
            else:
                comments.append(0)
        comments = [str(i) for i in comments]

        title = self.gettitle()
        with codecs.open('Topic:'+title+'.txt', 'w', 'utf-8')as f:
            f.write(u'话题:\t\t'+title+'\n')
            f.write(u'类型:\t\t'+kata+'\n')
            for i in range(len(names)):
                f.write('\n'+u'问题题目:\t'+questions[i]+'\n')
                f.write(u'回答作者:\t'+names[i]+'\n')
                f.write(u'回答简述:\t'+simpletext[i]+'\n')
                f.write(u'评论数:\t\t'+comments[i]+'\n')

        return url



































with open('/home/fan/people.txt', 'r')as f:
    datas = f.read()

# Data = BS(datas, 'lxml').prettify()
# with codecs.open('/home/fan/people0.txt', 'w', 'utf-8')as f:
#     f.write(Data)
hallo = People(datas).total()
print hallo

