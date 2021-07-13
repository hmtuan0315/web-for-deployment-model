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
    text = request.get_json()
    input = text['text']
    text_input = []
    text_input.append(input)

    input_size = 93270
    output_size = 1
    num_layer = 2
    embedding_dim = 400
    hidden_layer = 256
    PATH = "./nlp models/lstm_state_dict_model.pt"

    word2index = pickle.load(open("./nlp models/pickle_word2index", 'rb'))

    if (torch.cuda.is_available()):
        lstm_model = LSTM(input_size, output_size, num_layer, embedding_dim, hidden_layer).cuda()
    else:
        lstm_model = LSTM(input_size, output_size, num_layer, embedding_dim, hidden_layer)

    lstm_model.load_state_dict(torch.load(PATH))
    lstm_model.eval()

    def pad_features(reviews_int, seq_length):
        features = np.zeros((len(reviews_int), seq_length), dtype=int)

        for i, review in enumerate(reviews_int):
            review_len = len(review)
            if review_len <= seq_length:
                zeroes = list(np.zeros(seq_length - review_len))
                new = zeroes + review
            elif review_len > seq_length:
                new = review[0:seq_length]
            features[i, :] = np.array(new)

        return features

    def encode_sent(sent):
        sent = [word2index.token2id[word] for word in sent if word in word2index.token2id.keys()]
        return sent

    def preprocessing_input(sents):
        sents = list(map(remove_html_tag, sents))
        sents = list(map(remove_accent_char, sents))
        sents = list(map(expand_contractions, sents))
        sents = list(map(remove_special_characters, sents))
        sents = tokenizer_and_lemmatizer(sents)
        sents = list(map(tokenizer, sents))
        sents = list(map(remove_stopwords_sentiment, sents))
        # sents = list(map(remove_stopword, sents))
        sents = list(map(encode_sent, sents))
        sents = pad_features(sents, 300)
        return sents

    def input_prepare(sents):
        input = preprocessing_input(sents)
        input = np.array(input)
        input = torch.from_numpy(input)
        if torch.cuda.is_available():
            input = input.cuda()
        h = lstm_model.init_hidden(input.size(0))
        return input, h

    def make_predict(input, h):
        output, h = lstm_model(input, h)
        pred = torch.round(output)
        for ind, prediction in enumerate(pred):
            if (prediction == 1):
                return "Positive review detected!"
            else:
                return "Negative review detected."

    input, h = input_prepare(text_input)
    res = make_predict(input, h)
    return res


if __name__ == '__main__':
    app.run(debug=True)
