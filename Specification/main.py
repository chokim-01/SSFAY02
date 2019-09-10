from data import PreProcessing
#import tensorflow as tf

def main():

    # Make PreProcessing object
    pre_processing = PreProcessing()

    # Get Train, Test data
    question_train, question_test, answer_train, answer_test = pre_processing.load_data()

    # Make voca_dictionary
    pre_processing.make_voc()

    # Load voca_dictionary
    voca_dictionary = pre_processing.load_voc()


    # Encoding
    index, lens = pre_processing.enc_processing([["안녕하세요. 반갑습니다!"], ["좋은하루 입니다!"]], voca_dictionary)
    print(index, lens)


if __name__ == '__main__':
    #tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
    #tf.compat.v1.app.run(main)
    main()
