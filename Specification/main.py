from data import PreProcessing


def main():

    # Make PreProcessing object
    pre_processing = PreProcessing()

    # Get Train, Test data
    question_train, question_test, answer_train, answer_test = pre_processing.load_data()

    # Remove special character
    remove_noise_question_train, remove_noise_question_test, remove_noise_answer_train, remove_noise_answer_test\
        = pre_processing.prepro_noise_canceling(question_train, question_test, answer_train, answer_test)


if __name__ == '__main__':
    main()
