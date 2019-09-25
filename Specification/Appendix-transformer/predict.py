import tensorflow as tf
import Preprocessing
import os
import sys
import model as ml

from config import DEFINES

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.ERROR)
    arg_length = len(sys.argv)

    if (arg_length < 2):
        raise Exception("Don't call us. We'll call you")

    # make dictionary
    char2idx, idx2char, vocabulary_length = Preprocessing.load_vocabulary()

    input = ""
    for i in sys.argv[1:]:
        input += i
        input += " "

    print(input)

    predic_input_enc, predic_input_enc_length = Preprocessing.encode_processing([input], char2idx)
    predic_output_dec, predic_output_dec_length = Preprocessing.decode_processing([""], char2idx)
    predic_target_dec = Preprocessing.decode_target_processing([""], char2idx)

    print("[+] Encoding Decoding complete")

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


    predictions = classifier.predict(input_fn=lambda: Preprocessing.eval_input_fn(predic_input_enc, predic_output_dec, predic_target_dec, 1))

    answer, finished = Preprocessing.predict_next_sentence(predictions, idx2char)

    print("answer: ", answer)
