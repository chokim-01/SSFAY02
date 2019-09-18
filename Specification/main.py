import tensorflow as tf
import model as ml

from config import DEFINES
from data import PreProcessing


def main(self):
    pre_processing = PreProcessing()

    # Get vocabulary and length
    voca2idx, idx2voca, vocabulary_length = pre_processing.load_voc()

    # Get data
    question_train, question_test, answer_train, answer_test = pre_processing.load_data()

    # Remove special characters
    noise_cancel_question_train = pre_processing.prepro_noise_canceling(question_train)
    noise_cancel_question_test = pre_processing.prepro_noise_canceling(question_test)
    noise_cancel_answer_train = pre_processing.prepro_noise_canceling(answer_train)
    noise_cancel_answer_test = pre_processing.prepro_noise_canceling(answer_test)

    # Tokenize data
    tokenize_question_train = pre_processing.tokenize_data(noise_cancel_question_train)
    tokenize_question_test = pre_processing.tokenize_data(noise_cancel_question_test)
    tokenize_answer_train = pre_processing.tokenize_data(noise_cancel_answer_train)
    tokenize_answer_test = pre_processing.tokenize_data(noise_cancel_answer_test)

    # Encoding, Decoding for question data
    encode_question_train, encode_question_train_length = pre_processing.enc_processing(tokenize_question_train, voca2idx)
    decode_question_output_train, decode_question_output_train_length = pre_processing.dec_output_processing(tokenize_question_train, voca2idx)
    decode_question_target_train = pre_processing.dec_target_processing(tokenize_question_train, voca2idx)

    # Encoding, Decoding for answer data
    encode_answer_train, encode_answer_train_length = pre_processing.enc_processing(tokenize_answer_train, voca2idx)
    decode_answer_output_train, decode_answer_output_train_length = pre_processing.dec_output_processing(tokenize_answer_train, voca2idx)
    decode_answer_target_train = pre_processing.dec_target_processing(tokenize_answer_train, voca2idx)

    # Make estimator
    classifier = tf.estimator.Estimator(
        model_fn=ml.model,  # 모델 등록한다.
        model_dir=DEFINES.check_point_path,  # 체크포인트 위치 등록한다.
        params={  # 모델 쪽으로 파라메터 전달한다.
            'embedding_size': DEFINES.embedding_size,
            'model_hidden_size': DEFINES.model_hidden_size,  # 가중치 크기 설정한다.
            'ffn_hidden_size': DEFINES.ffn_hidden_size,
            'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,  # 학습율 설정한다.
            'vocabulary_length': vocabulary_length,  # 딕셔너리 크기를 설정한다.
            'embedding': DEFINES.embedding,  # 임베딩 크기를 설정한다.
            'layer_size': DEFINES.layer_size,
            'max_sequence_length': DEFINES.max_sequence_length,
            'xavier_initializer': DEFINES.xavier_initializer,
            'multilayer': DEFINES.multilayer
        })


    # Training
    classifier.train(input_fn=lambda: pre_processing.train_input_fn(
        encode_question_train, decode_question_output_train, decode_question_target_train, DEFINES.batch_size), steps=DEFINES.train_steps)

    # res
    answer_result = classifier.evaluate(input_fn=lambda: pre_processing.eval_input_fn(
        encode_answer_train, decode_answer_output_train, decode_answer_target_train, DEFINES.batch_size))

    print('\nEVAL set accuracy: {accuracy:0.3f}\n'.format(**answer_result))


if __name__ == '__main__':
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
    tf.compat.v1.app.run(main)

"""
EVAL set accuracy: 0.894
"""
