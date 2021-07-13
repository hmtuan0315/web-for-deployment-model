from flask import Flask
import torch
import torch.nn as nn
import pickle
import numpy as np
from flask_cors import CORS, cross_origin
from flask import request, jsonify
from Utils import remove_html_tag, remove_accent_char, remove_stopwords_sentiment, \
    remove_special_characters, tokenizer_and_lemmatizer, tokenizer, expand_contractions

app = Flask(__name__)
cors = CORS(app, headers=['Content-Type'], expose_headers=['Access-Control-Allow-Origin'], supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'


class LSTM(nn.Module):
    def __init__(self, input_size, output_size, num_layers, embedding_dim, hidden_dim, p_drop=0.5):
        super(LSTM, self).__init__()
        self.n_layers = num_layers
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_dim = hidden_dim

        self.embedding = nn.Embedding(input_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, dropout=p_drop, batch_first=True)

        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(hidden_dim, 64)
        self.fc2 = nn.Linear(64, output_size)
        self.sigmoid = nn.Sigmoid()

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        if (torch.cuda.is_available()):
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda(),
                      weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().cuda())
        else:
            hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_(),
                      weight.new(self.n_layers, batch_size, self.hidden_dim).zero_())

        return hidden

    def forward(self, x, hidden):
        # x size: [batch_size, seq_len]
        batch_size = x.size()
        out = self.embedding(x)
        # out: [batch_size, seq_len, embedding_dim]
        out, hidden = self.lstm(out, hidden)
        # out: [batch_size, seq_len, hidden_dim]
        out = self.dropout(out)
        out = self.fc1(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.dropout(out)
        sig_out = self.sigmoid(out)

        sig_out = sig_out.view(batch_size, -1)
        sig_out = sig_out[:, -1]
        return sig_out, hidden


# text_input = ["it's a bad movie out of the time", "you're a murder, but you still have morality"]

@app.route('api/cls_lstm/', methods=['POST'], strict_slashes=False)
def classification():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
