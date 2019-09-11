from data import PreProcessing
import tensorflow as tf


def main(self):

    # Make PreProcessing object
    pre_processing = PreProcessing()

    # Get Train, Test data
    question_train, answer_train, question_test, answer_test = pre_processing.load_data()

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

    # Get vocabulary dictionary
    voca2idx, idx2voca, voca_len = pre_processing.load_voc()

    # Encoding data
    encode_question_train, encode_question_train_len = pre_processing.enc_processing(tokenize_question_train, voca2idx)
    encode_question_test, encode_question_test_len = pre_processing.enc_processing(tokenize_question_test, voca2idx)
    encode_answer_train, encode_answer_train_len = pre_processing.enc_processing(tokenize_answer_train, voca2idx)
    encode_answer_test, encode_answer_test_len = pre_processing.enc_processing(tokenize_answer_test, voca2idx)



if __name__ == '__main__':
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
    tf.compat.v1.app.run(main)
