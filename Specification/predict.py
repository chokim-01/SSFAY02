import tensorflow as tf
import os
import sys
import model as ml

from data import PreProcessing
from config import DEFINES

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def main(message):
    pre_processing = PreProcessing()

    voca2idx, idx2voca, vocabulary_length = pre_processing.load_voc()

    # Remove special characters
    noise_cancel_message = pre_processing.prepro_noise_canceling([message])

    # Tokenize data
    tokenize_message = pre_processing.tokenize_data(noise_cancel_message)
    tokenize_none_msg = pre_processing.tokenize_data([""])

    print(tokenize_none_msg)

    # Encoding, Decoding for question data
    encode_message_predict, encode_message_predict_length = pre_processing.enc_processing(tokenize_message, voca2idx)
    decode_message_output_predict, decode_message_output_predict_length = pre_processing.dec_output_processing(tokenize_none_msg, voca2idx)
    decode_message_target_predict = pre_processing.dec_target_processing(tokenize_none_msg, voca2idx)

    print("here2", encode_message_predict)
    print("here2", decode_message_output_predict)
    print("here2", decode_message_target_predict)

    classifier = tf.estimator.Estimator(
        model_fn=ml.model,  # 모델 등록한다.
        model_dir=DEFINES.check_point_path,  # 체크포인트 위치 등록한다.
        params={  # 모델 쪽으로 파라메터 전달한다.
            'model_hidden_size': DEFINES.model_hidden_size,
            'layer_size': DEFINES.layer_size,
            'learning_rate': DEFINES.learning_rate,
            'vocabulary_length': vocabulary_length,
            'embedding_size': DEFINES.embedding_size,
            'embedding': DEFINES.embedding,
            'multilayer': DEFINES.multilayer,
        })

    predictions = classifier.predict(input_fn=lambda: pre_processing.eval_input_fn(
        encode_message_predict, decode_message_output_predict, decode_message_target_predict, DEFINES.batch_size))

    print("insert pred_next_string")
    print(list(predictions))
    answer = pre_processing.pred_next_string(predictions, idx2voca)

    print(answer)


if __name__ == '__main__':
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    if len(sys.argv) < 2:
        print("python predict.py sentence")
    else:
        main(sys.argv[1])
