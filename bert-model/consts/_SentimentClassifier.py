import torch.nn as nn
from transformers import BertModel
from consts import MODEL


class SentimentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(MODEL)
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        d = self.bert(input_ids=input_ids, attention_mask=attention_mask)

        output = self.drop(d.pooler_output)
        output = self.out(output)
        return self.softmax(output)
