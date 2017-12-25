# -*- coding: utf-8 -*-

import collections

import numpy as np
import torch
from torch import nn
import torch.optim as optimizer
from torch.autograd import Variable

from model import SentimentNetwork

Config = collections.namedtuple('Config', 'train, gpu, dict_size, lr')


class SentimentClassifier(object):

    def __init__(self, config):

        self.is_train = config.train
        self.use_gpu = config.gpu
        self.dict_size = config.dict_size

        self.classifier = SentimentNetwork(self.dict_size)
        if self.is_train:
            self.criterion = nn.CrossEntropyLoss()
            self.optimizer = optimizer.Adam(lr=config.lr, params=self.classifier.parameters())
        if self.use_gpu:
            self.classifier = self.classifier.cuda()

        if self.is_train and self.use_gpu:
            self.criterion = self.criterion.cuda()

    def train(self, x, labels):

        x = Variable(torch.LongTensor(x))
        labels = Variable(torch.LongTensor(labels))

        if self.use_gpu:
            x = x.cuda()
            labels = labels.cuda()

        prob = self.classifier(x, 30)

        loss = self.criterion(prob, labels)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.cpu().data[0]

    def save(self, path, index):

        if self.use_gpu:
            torch.save(self.classifier.state_dict(), path+'epoch_%s_gpu_params.pth' % index)
            torch.save(self.classifier.cpu().state_dict(), path+'epoch_%s_cpu_params.pth' % index)
        else:
            torch.save(self.classifier.state_dict(), path+'epoch_%s_cpu_params.pth' % index)

    def load_params(self, path):
        self.classifier.load_state_dict(torch.load(path))

    def inference(self, x):

        x = Variable(torch.LongTensor(x))
        x = x.unsqueeze(0)
        prob = self.classifier(x).squeeze(0)

        return prob.data.numpy()


def train():

    opt = Config(
        train=True,
        gpu=False,
        dict_size=1111,
        lr=0.0001
    )

    classifier = SentimentClassifier(opt)

