import tensorflow as tf
import os
import pickle
import numpy as np
from flask import Flask
from threading import Thread
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter


import Preprocessing
import model as ml
from config import DEFINES


SLACK_TOKEN = "xoxb-729760465732-772320589472-YYWyfpnROIUb6OwjUyvxhnBh"
SLACK_SIGNING_SECRET = "91945cd65b348a3c92872113c4433b7c"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def predict(question):
    tf.logging.set_verbosity(tf.logging.ERROR)
    arg_length = len(question)

    if (arg_length < 2):
        raise Exception("Don't call us. We'll call you")

    # load dictionary
    char2idx, idx2char, vocabulary_length = Preprocessing.load_vocabulary()

    # make test data
    input = str(question)

    # encoding / decoding
    predic_input_enc, predic_input_enc_length = Preprocessing.encode_processing([input], char2idx)
    predic_output_dec, predic_output_dec_length = Preprocessing.decode_processing([""], char2idx)
    predic_target_dec = Preprocessing.decode_target_processing([""], char2idx)

    # Estimator
    classifier = tf.estimator.Estimator(
        model_fn=ml.Model,
        model_dir=DEFINES.check_point_path,
        params={
            'embedding_size': DEFINES.embedding_size,
            'model_hidden_size': DEFINES.model_hidden_size,
            'ffn_hidden_size': DEFINES.ffn_hidden_size,
            'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,
            'vocabulary_length': vocabulary_length,
            'layer_size': DEFINES.layer_size,
            'max_sentence_length': DEFINES.max_sentence_length,
            'xavier_initializer': DEFINES.xavier_initializer
        })

    predictions = classifier.predict(
        input_fn=lambda: Preprocessing.eval_input_fn(predic_input_enc, predic_output_dec, predic_target_dec, 1))

    answer, finished = Preprocessing.predict_next_sentence(predictions, idx2char)

    return answer


@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    text = text.split()
    message = ''.join(text[1:])
    print(message)
    answer = predict(message)


    slack_web_client.chat_postMessage(
        channel=channel,
        text=answer
    )


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run()
