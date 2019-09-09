from data import PreProcessing


def main():
    pre_processing = PreProcessing()
    question_train, question_test, answer_train, answer_test = pre_processing.load_data()


if __name__ == '__main__':
    main()
