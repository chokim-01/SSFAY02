import tensorflow as tf
import model as ml
import data
import numpy as np
import os
import sys

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from rouge import Rouge

from configs import DEFINES

DATA_OUT_PATH = './data_out/'

# Req. 1-5-1. bleu score 계산 함수
def bleu_compute():
    
    return None

# Req. 1-5-2. rouge score 계산 함수
def rouge_compute():
    
    return None

# Req. 1-5-3. main 함수 구성
def main(self):
    processing_data = data.PreProcessing()

    data_out_path = os.path.join(os.getcwd(), DATA_OUT_PATH)
    os.makedirs(data_out_path, exist_ok=True)

    # char_to_idx, idx_to_char dictionary and length of voc_list
    char2idx, idx2char, vocabulary_length = processing_data.load_voc()

    # load train, test data
    train_q, train_a, test_q, test_a = processing_data.load_data()

    # train encoding / decoding
    train_input_enc, train_input_enc_length = processing_data.enc_processing(train_q, char2idx)
    train_input_dec, train_input_dec_length = processing_data.dec_input_processing(train_a, char2idx)

    # train decoding output
    train_target_dec = processing_data.dec_target_processing(train_a, char2idx)

    # test encoding / decoding
    eval_input_enc, eval_input_enc_length = processing_data.enc_processing(test_q, char2idx)
    eval_input_dec = processing_data.dec_input_processing(test_a, char2idx)

    # test decoding output
    eval_target_dec = processing_data.dec_target_processing(test_a, char2idx)

    check_point_path = os.path.join(os.getcwd(), DEFINES.check_point_path)
    os.makedirs(check_point_path, exist_ok=True)

    # estimator
    classifier = tf.estimator.Estimator(
        model_fn=ml.Model,
        model_dir=DEFINES.check_point_path,
        params={
            'model_hidden_size': DEFINES.model_hidden_size,
            'ffn_hidden_size': DEFINES.ffn_hidden_size,
            'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,
            'vocabulary_length': vocabulary_length,
            'embedding_size': DEFINES.embedding_size,
            'layer_size': DEFINES.layer_size,
            'max_sequence_length': DEFINES.max_sequence_length,
            'xavier_initializer': DEFINES.xavier_initializer
        })

    # 학습 실행
    classifier.train(input_fn=lambda: data.train_input_fn(
        train_input_enc, train_input_dec, train_target_dec, DEFINES.batch_size), steps=DEFINES.train_steps)

    eval_result = classifier.evaluate(input_fn=lambda: data.eval_input_fn(
        eval_input_enc, eval_input_dec, eval_target_dec, DEFINES.batch_size))

    print('\nEVAL set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # 테스트용 데이터 만드는 부분이다.
    # 인코딩 부분 만든다. 테스트용으로 ["가끔 궁금해"] 값을 넣어 형성된 대답과 비교를 한다.
    predic_input_enc, predic_input_enc_length = processing_data.enc_processing(["가끔 궁금해"], char2idx)
    predic_input_dec, predic_input_dec_length = processing_data.dec_input_processing([""], char2idx)
    predic_target_dec = processing_data.dec_target_processing([""], char2idx)

    predictions = classifier.predict(
        input_fn=lambda: data.eval_input_fn(predic_input_enc, predic_input_dec, predic_target_dec, 1))

    answer, finished = data.pred_next_string(predictions, idx2char)

    # 예측한 값을 인지 할 수 있도록
    # 텍스트로 변경하는 부분이다.
    print("answer: ", answer)
    print("Bleu score: ", bleu_compute("그 사람도 그럴 거예요.", answer))
    print("Rouge score: ", rouge_compute("그 사람도 그럴 거예요.", answer))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)

tf.logging.set_verbosity
