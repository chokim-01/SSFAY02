import re
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from os.path import exists as exists_file
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from collections import deque
from config import DEFINES
from tqdm import tqdm

SPECIAL_CHARACTER = "([~.,!?\"':;)(])"
PAD = "<PADDING>"
STD = "<START>"
END = "<END>"
UNK = "<UNKNOWN>"

PAD_INDEX = 0
STD_INDEX = 1
END_INDEX = 2
UNK_INDEX = 3

MARKER = [UNK, END, STD, PAD]
SPECIAL_CHARACTER = re.compile(SPECIAL_CHARACTER)


def load_data():
    """
    Load chatbot data and split question and answer
    :return: question train, question test, answer train, answer test data
    """

    if not exists_file("./Data/question_and_answer.dat"):
        # Load Chatbot data
        data_frame = pd.read_csv(DEFINES.chatbot_data_path, header=0)

        # Get question and answer data
        question = data_frame["Q"]
        answer = data_frame["A"]

        # question and answer data splited
        question_train, answer_train, question_test, answer_test\
            = train_test_split(question, answer, test_size=0.33, random_state=42)

        with open("./Data/question_and_answer.data", "wb") as file:
            pickle.dump([question_train, question_test, answer_train, answer_test], file)

    else:
        with open("./Data/question_and_answer.data", "r") as file:
            question_and_answer = pickle.load(file)

        question_train = question_and_answer[0]
        question_test = question_and_answer[1]
        answer_train = question_and_answer[2]
        answer_test = question_and_answer[3]

    return question_train, question_test, answer_train, answer_test


def make_vocabulary(vocabulary_list):
    """

    :param vocabulary_list: vocabulary list
    :return: vocabulary to index, index to vocabulary
    """
    voca2idx = {voca: idx for idx, voca in enumerate(vocabulary_list)}
    idx2voca = {idx: voca for idx, voca in enumerate(vocabulary_list)}

    return voca2idx, idx2voca


def remove_special_character(sentence):
    return re.sub(SPECIAL_CHARACTER, "", sentence)


def remove_special_character_and_tokenize_as_space(data_frame):
    """
    Remove special character and tokenize as space
    :param data_frame: data frame
    :return: remove special character and tokenize as space vocabulary data
    """
    global SPECIAL_CHARACTER

    vocabularies = deque()

    for sentence in data_frame:
        # Remove special character
        sentence = remove_special_character(sentence)

        for voca in sentence.split():
            vocabularies.append(voca)

    return deque(voca for voca in vocabularies if voca)


def tokenize_data_as_morpheme(data_frame):
    """
    Each sentence delete space and tokenize as morpheme
    :param data_frame: data frame
    :return: tokenize as morpheme data list
    """

    okt = Okt()
    morphemed_sentence_list = deque()

    # Each sentence delete space and tokenize as morpheme
    for sentence in tqdm(data_frame):
        # Remove space and tokenize as morpheme
        morphlized_sentence = " ".join(okt.morphs(sentence.replace(" ", "")))

        # Append list
        morphemed_sentence_list.append(morphlized_sentence)

    return morphemed_sentence_list


def load_vocabulary():
    """
    If not exists VocabularyData.voc, make vocabulary data
    If exists load vocabulary data
    :return: vocabulary to index, index to vocabulary, vocabulary length
    """

    global MARKER
    vocabulary_list = []

    # If not exists VocabularyData.voc
    if not exists_file(DEFINES.vocabulary_path):

        # If exists ChatBotData.csv
        if exists_file(DEFINES.chatbot_data_path):
            # Load chat bot data
            dataframe = pd.read_csv(DEFINES.chatbot_data_path, encoding="utf-8")
            print("[+] Load chatbot data complete")

            # Get question and answer data
            question = dataframe["Q"]
            answer = dataframe["A"]

            # If tokenize flag is true
            if DEFINES.tokenize_morpheme_flag:
                question = tokenize_data_as_morpheme(question)
                answer = tokenize_data_as_morpheme(answer)
                print("[+] tokenize as morpheme complete")

            data = deque()
            data.extend(question)
            data.extend(answer)

            vocabularies = deque(set(list(remove_special_character_and_tokenize_as_space(data))))
            print("[+] Get vocabularies complete")

            for maker in MARKER:
                vocabularies.appendleft(maker)
            print("[+] Append MAKER complete")

        # Save vocabulary file
        with open(DEFINES.vocabulary_path, "w", encoding="utf-8") as file:
            for voca in vocabularies:
                file.write(voca + "\n")

    # Load vocabulary file
    with open(DEFINES.vocabulary_path, "r", encoding="utf-8") as file:
        for line in file:
            vocabulary_list.append(line.strip())

    voca2idx, idx2voca = make_vocabulary(vocabulary_list)
    print("[+] Make vocabulary complete")

    return voca2idx, idx2voca, len(voca2idx)


def encode_processing(data_frame, voca2idx):
    global UNK, PAD

    message_index_list = deque()
    message_length_list = deque()

    # If using tokenize as morpheme
    if DEFINES.tokenize_morpheme_flag:
        data_frame = tokenize_data_as_morpheme(data_frame)

    for sentence in data_frame:
        # Remove special character
        sentence = remove_special_character(sentence)

        sentence_index_list = deque()

        for voca in sentence.split():

            # If exists voca in voca2idx
            if voca2idx.get(voca) is not None :
                sentence_index_list.extend([voca2idx[voca]])
            else:
                sentence_index_list.extend([voca2idx[UNK]])

        if len(sentence_index_list) > DEFINES.max_sentence_length:
            sentence_index_list = sentence_index_list[:DEFINES.max_sentence_length]

        # Add sentence_list_length
        message_length_list.append(len(sentence_index_list))

        # If sentence_list_length under max_sentence_length
        sentence_index_list += [voca2idx[PAD]] * (DEFINES.max_sentence_length - len(sentence_index_list))
        message_index_list.append(sentence_index_list)

    return np.asarray(message_index_list)


def decode_processing(data_frame, voca2idx):
    global STD

    message_index_list = deque()
    message_length_list = deque()

    # If using tokenize as morpheme
    if DEFINES.tokenize_morpheme_flag:
        data_frame = tokenize_data_as_morpheme(data_frame)

    for sentence in data_frame:
        # Remove special character
        sentence = remove_special_character(sentence)

        sentence_tmp = deque()
        for voca in sentence.split():
            sentence_tmp.append(voca2idx[voca])

        sentence_index_list = deque([voca2idx[STD]]) + sentence_tmp

        if len(sentence_index_list) > DEFINES.max_sentence_length:
            sentence_index_list = deque(list(sentence_index_list)[:DEFINES.max_sentence_length])

        message_length_list.append(len(sentence_index_list))
        sentence_index_list += [voca2idx[PAD]] * (DEFINES.max_sentence_length - len(sentence_index_list))

        message_index_list.append(sentence_index_list)

    return np.asarray(message_index_list)


def decode_target_processing(data_frame, voca2idx):
    global END, PAD

    message_index_list = deque()

    # If using tokenize as morpheme
    if DEFINES.tokenize_morpheme_flag:
        data_frame = tokenize_data_as_morpheme(data_frame)

    for sentence in data_frame:
        sentence = remove_special_character(sentence)

        sentence_index_list = deque(voca2idx[voca] for voca in sentence.split())

        if len(sentence_index_list) > DEFINES.max_sentence_length:
            sentence_index_list = deque(list(sentence_index_list)[:DEFINES.max_sentence_length-1]) + deque([voca2idx[END]])
        else:
            sentence_index_list += deque([voca2idx[END]])

        sentence_index_list += [voca2idx[PAD]] * (DEFINES.max_sentence_length - len(sentence_index_list))
        message_index_list.append(sentence_index_list)

    return np.asarray(message_index_list)


def re_arrange(input_data, output_data, target):
    features = {"input": input_data, "output": output_data}

    return features, target


def train_input_fn(encode_train, decode_train, decode_target_train, batch_size):
    # Make data set, splited each sentence
    dataset = tf.data.Dataset.from_tensor_slices((encode_train, decode_train, decode_target_train))
    dataset = dataset.shuffle(buffer_size=len(encode_train))

    # If batch_size is None
    assert batch_size is not None, "Train batch size is None"

    # Combine as batch size of from_tensor_slices
    dataset = dataset.batch(batch_size)
    dataset = dataset.map(re_arrange)

    # If repeat func does not have parameter, Infinite iterating
    dataset = dataset.repeat()
    one_shot_iterator = dataset.make_one_shot_iterator()

    return one_shot_iterator.get_next()


def eval_input_fn(encode_predict, decode_predict, decode_target_predict, batch_size):
    # Make data set, splited each sentence
    dataset = tf.data.Dataset.from_tensor_slices((encode_predict, decode_predict, decode_target_predict))
    dataset = dataset.shuffle(buffer_size=len(encode_predict))

    # If batch_size is None
    assert batch_size is not None, "Predict batch size is none"

    # Combine as batch size of from_tensor_slices
    dataset = dataset.batch(batch_size)
    dataset = dataset.map(re_arrange)

    # This function is predict test so, repeat 1
    dataset = dataset.repeat(1)

    one_shot_iterator = dataset.make_one_shot_iterator()

    return one_shot_iterator.get_next()


def predict_to_sentence(indexing_data, idx2voca):
    global PAD, END

    vocabularies = deque()

    for indexd in indexing_data:
        vocabularies = deque([idx2voca[index] for index in indexd["indexs"]])

    answer = ""

    for voca in vocabularies:
        # If voca not in PAD and END
        if voca not in [PAD, END]:
            answer += voca
            answer += " "

    return answer


def main(self):
    voca2idx, idx2voca, vocabulary_length = load_vocabulary()


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
