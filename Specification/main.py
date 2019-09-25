import Preprocessing
import os
import sys
import model as ml
import tensorflow as tf

from config import DEFINES

DATA_OUT_PATH = './data_out/'

def main(self):
    data_out_path = os.path.join(os.getcwd(), DATA_OUT_PATH)
    os.makedirs(data_out_path, exist_ok=True)

    # Load voca2idx, idx2voca, vocabulary_length
    voca2idx, idx2voca, vocabulary_length = Preprocessing.load_vocabulary()
    print("[+] Load vocabulary complete")

    # Get train and test data
    question_train, answer_train, question_test, answer_test = Preprocessing.load_data()
    print("[+] Load train and test data complete")

    # Encode and decode train data
    encode_question_train, encode_question_train_length = Preprocessing.encode_processing(question_train, voca2idx)
    decode_answer_train, decode_answer_train_length = Preprocessing.decode_processing(answer_train, voca2idx)
    decode_target_train = Preprocessing.decode_target_processing(answer_train, voca2idx)
    print("[+] Encode and decode train data complete")

    # Encode and decode test data
    encode_question_test, encode_question_test_length = Preprocessing.encode_processing(question_test, voca2idx)
    decode_answer_test, decode_answer_test_length = Preprocessing.decode_processing(answer_test, voca2idx)
    decode_target_test = Preprocessing.decode_target_processing(answer_test, voca2idx)
    print("[+] Encode and decode test data complete")

    # Make check point directory
    check_point_path = os.path.join(os.getcwd(), DEFINES.check_point_path)
    os.makedirs(check_point_path, exist_ok=True)

    # Make Estimator
    classifier = tf.estimator.Estimator(
        model_fn=ml.Model,
        model_dir=DEFINES.check_point_path,
        params={
            'embedding_size': DEFINES.embedding_size,
            "embedding": DEFINES.embedding,
            'model_hidden_size': DEFINES.model_hidden_size,
            'ffn_hidden_size': DEFINES.ffn_hidden_size,
            'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,
            'vocabulary_length': vocabulary_length,
            'layer_size': DEFINES.layer_size,
            'max_sentence_length': DEFINES.max_sentence_length,
            'xavier_initializer': DEFINES.xavier_initializer
        }
    )
    print(encode_question_train.shape, decode_answer_train.shape, decode_target_train.shape)
    print(encode_question_test.shape, decode_answer_test.shape, decode_target_test.shape)
    # Execute training
    classifier.train(input_fn=lambda: Preprocessing.train_input_fn(encode_question_train, decode_answer_train,
                                                                   decode_target_train, DEFINES.batch_size),
                     steps=DEFINES.train_steps)

    # Execute evaluating
    answer_result = classifier.evaluate(input_fn=lambda:Preprocessing.eval_input_fn(
        encode_question_test, decode_answer_test, decode_target_test,  DEFINES.batch_size))



    # Make predict data
    encode_predict_question, encode_predict_question_length = Preprocessing.encode_processing(["가끔 궁금해"], voca2idx)
    decode_predict_answer, decode_predict_answer_length_ = Preprocessing.decode_processing([""], voca2idx)
    decode_predict_target = Preprocessing.decode_target_processing([""], voca2idx)

    # Execute predicting
    predictions = classifier.predict(
        input_fn=lambda: Preprocessing.eval_input_fn(encode_predict_question, decode_predict_answer, decode_predict_target, 1))

    result_sentence = Preprocessing.predict_to_sentence(predictions, idx2voca)

    print(result_sentence)
    print("\n [+] Predict accuracy: {accuracy: 0.6f}\n".format(**answer_result))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)

tf.logging.set_verbosity
