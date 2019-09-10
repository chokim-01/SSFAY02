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
    print(voca_dictionary)




if __name__ == '__main__':
    #tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
    #tf.compat.v1.app.run(main)
    main()
