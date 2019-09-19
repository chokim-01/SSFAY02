import Preprocessing
import os

import model as ml
import tensorflow as tf

from config import DEFINES


def main(self):

    # Load voca2idx, idx2voca, vocabulary_length
    voca2idx, idx2voca, vocabulary_length = Preprocessing.load_vocabulary()
    print("[+] Load vocabulary complete")

    # Get train and test data
    question_train, question_test, answer_train, answer_test = Preprocessing.load_data()
    print("[+] Load train and test data complete")

    # Encode and decode train data
    encode_question_train = Preprocessing.encode_processing(question_train, voca2idx)
    decode_question_test = Preprocessing.decode_processing(question_test, voca2idx)
    decode_target_question_test = Preprocessing.decode_target_processing(question_test, voca2idx)
    print("[+] Encode and decode train data complete")


    # Encode and decode test data
    encode_answer_train = Preprocessing.encode_processing(answer_train, voca2idx)
    decode_answer_test = Preprocessing.decode_processing(answer_test, voca2idx)
    decode_target_answer_test = Preprocessing.decode_target_processing(answer_test, voca2idx)
    print("[+] Encode and decode test data complete")

    # Make check point directory
    check_point_path = os.path.join(os.getcwd(), DEFINES.check_point_path)
    os.makedirs(check_point_path, exist_ok=True)

    # Make Estimator
    classifier = tf.estimator.Estimator(
        model_fn=ml.model,
        model_dir=DEFINES.check_point_path,
        params={
            "hidden_size": DEFINES.hidden_size,
            "layer_size": DEFINES.layer_size,
            "learning_rate": DEFINES.learning_rate,
            "vocabulary_length": vocabulary_length,
            "embedding_size": DEFINES.embedding_size,
            "embedding": DEFINES.embedding,
            "multilayer": DEFINES.multilayer
        }
    )

    # Execute training
    classifier.train(input_fn=lambda: Preprocessing.train_input_fn(encode_question_train, decode_question_test,
                                                                   decode_target_question_test, DEFINES.batch_size),
                     steps=DEFINES.train_steps)

    # Execute evaluating
    answer_result = classifier.evaluate(input_fn=lambda:Preprocessing.eval_input_fn(
        encode_answer_train, decode_answer_test, decode_target_answer_test,  DEFINES.batch_size))

    print("\n [+] Predict accuracy: {accuracy: 0.3f}\n".format(**answer_result))

    # Make predict data
    encode_predict_train = Preprocessing.encode_processing(["가끔 궁금해"], voca2idx)
    decode_predict_test = Preprocessing.decode_processing([""], voca2idx)
    decode_target_predict_test = Preprocessing.decode_target_processing([""], voca2idx)

    # Execute predicting
    predictions = classifier.predict(
        input_fn=lambda: Preprocessing.eval_input_fn(encode_predict_train, decode_predict_test,
                                                     decode_target_predict_test, DEFINES.batch_size))

    result_sentence = Preprocessing.predict_to_sentence(predictions, idx2voca)

    print(result_sentence)


if __name__ == '__main__':
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    tf.compat.v1.app.run(main)
