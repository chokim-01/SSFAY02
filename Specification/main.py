from data import PreProcessing
#import tensorflow as tf

def main():

    # Make PreProcessing object
    pre_processing = PreProcessing()

    # Get Train, Test data
    question_train, question_test, answer_train, answer_test = pre_processing.load_data()

    # Remove special character
    noise_cancel_question_train = pre_processing.prepro_noise_canceling(question_train)
    noise_cancel_question_test = pre_processing.prepro_noise_canceling(question_test)
    noise_cancel_answer_train = pre_processing.prepro_noise_canceling(answer_train)
    noise_cancel_answer_test = pre_processing.prepro_noise_canceling(answer_test)

    # Tokenize data
    tokenize_question_train = pre_processing.tokenize_data(noise_cancel_question_train)
    tokenize_question_test = pre_processing.tokenize_data(noise_cancel_question_test)
    tokenize_answer_train = pre_processing.tokenize_data(noise_cancel_answer_train)
    tokenize_answer_test = pre_processing.tokenize_data(noise_cancel_answer_test)





if __name__ == '__main__':
    #tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
    #tf.compat.v1.app.run(main)
    main()
