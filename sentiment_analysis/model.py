# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F


class CNNRNNClassifier(nn.Module):
    def __init__(self, vocab_size, label_size):
        super(CNNRNNClassifier, self).__init__()

        self.embedding = nn.Embedding(
            vocab_size, 256, padding_idx=0)
        self.convs = nn.ModuleList([
            nn.Conv2d(1, Nk, Ks)
            for (Ks, Nk) in zip([(5, 256), (5, 256)], [256, 128])
        ])
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=128,
            num_layers=2,
            dropout=0.5,
            bidirectional=False)

        self.dense = nn.Linear(
            in_features=128, out_features=label_size)

    def forward(self, entity_ids, seq_len):
        x = self.embedding(entity_ids)
        x = x.unsqueeze(1)

        x = F.relu(self.convs[0](x)).squeeze(3)
        x = x.transpose(1, 2)
        x = x.unsqueeze(1)
        x = F.relu(self.convs[1](x)).squeeze(3)
        x = x.transpose(1, 2)

        out, _ = self.lstm(x.transpose(0, 1))
        last_output = out[-1, :, :]
        logits = self.dense(last_output)

        return logits

def test():

    import numpy as np
    m = np.random.random_integers(0, 500, size=[4, 50])
    p = CNNRNNClassifier(520, 2)
    m = Variable(torch.LongTensor(m))

    s = p(m,30)
    print(s.size())



