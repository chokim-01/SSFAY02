import pandas as pd
import numpy as np
import tensorflow as tf
import re
import os

from tqdm import tqdm
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
from configs import DEFINES


class PreProcessing:

	def __init__(self):
		self.PAD = "<PAD>"
		self.STD = "<SOS>"
		self.END = "<END>"
		self.UNK = "<UNK>"

		self.PAD_INDEX = 0
		self.STD_INDEX = 1
		self.END_INDEX = 2
		self.UNK_INDEX = 3

		self.MARKER = [self.PAD, self.STD, self.END, self.UNK]


	def pred_next_string(self, value, dictionary):
		sentence = []
		for text in  value:
			# change to word in dictionary
			sentence = [ dictionary[index] for index in text['indexs']]

		answer = ""
		# make answer
		for word in sentence:
			if word not in self.END and word not in self.PAD:
				answer += word
				answer += " "

		return answer


	def data_tokenizer(self, data):
		words = []
		for sentence in data:
			sentence = self.prepro_noise_canceling(sentence)
			for word in sentence.split():
				words.append(word)
		return [word for word in words if word]


	def load_voc(self):
		# dictionary data
		voc_list = []

		# create dictionary
		if (not (os.path.exists(DEFINES.vocabulary_path))):
			if (os.path.exists(DEFINES.data_path)):
				# get data
				data_frame = pd.read_csv("./data_in/ChatBotData.csv", encoding='utf-8')
				question = list(data_frame["Q"])
				answer = list(data_frame["A"])

				# if not tokenized
				if DEFINES.xavier_initializer:
					question = self.tokenizing_data(question)
					answer = self.tokenizing_data(answer)

				data = []
				data.extend(question)
				data.extend(answer)

				# tokenization data
				words = self.data_tokenizer(data)

				# removing duplicated
				words = list(set(words))

				# set marker
				words[:0] = self.MARKER

			# create dictionary data
			with open(DEFINES.vocabulary_path, 'w', encoding='utf-8') as voc_file:
				for word in words:
					voc_file.write(word+"\n")

		# read voc file and save voc_list
		with open(DEFINES.vocabulary_path, 'r', encoding='utf-8') as voc_file:
			for line in voc_file:
				voc_list.append(line.rstrip('\n'))

		# create dictionary
		char2idx, idx2char = self.make_voc(voc_list)

		return char2idx, idx2char, len(voc_list)


	def make_voc(self, voc_list):
		char2idx = {word: idx for idx, word in enumerate(voc_list)}
		idx2char = {idx: word for idx, word in enumerate(voc_list)}
		print(char2idx)
		return char2idx, idx2char


	def dec_target_processing(self, value, dictionary):
		seq_input_index = []

		# tokenize
		if DEFINES.xavier_initializer:
			value = self.tokenizing_data(value)

		print(len(value))
		for seq in value:
			# remove length over tokens
			seq_index = [dictionary[word] for word in seq.split()]

			# add end tokens
			if len(seq_index) >= DEFINES.max_sequence_length:
				seq_index = seq_index[:DEFINES.max_sequence_length - 1] + [dictionary[self.END]]
			else:
				seq_index += [dictionary[self.END]]

			# if shorter than max_sequence_length add padding
			seq_index += (DEFINES.max_sequence_length - len(seq_index)) * [dictionary[self.PAD]]

			# append index value
			seq_input_index.append(seq_index)

		return np.asarray(seq_input_index)


	def dec_input_processing(self, value, dictionary):
		"""
			seq_input_index : index data
			seq_len : length of sentence
		"""
		seq_input_index = []
		seq_len = []

		# tokenize
		if DEFINES.xavier_initializer:
			value = self.tokenizing_data(value)

		for seq in value:
			seq_index = [dictionary[self.STD]] + [dictionary[word] for word in seq.split()]

			# remove length over tokens
			if len(seq_index) > DEFINES.max_sequence_length:
				seq_index = seq_index[:DEFINES.max_sequence_length]

			# set seq_length
			seq_len.append(len(seq_index))

			# if shorter than max_sequence_length add padding
			seq_index += (DEFINES.max_sequence_length - len(seq_index)) * [dictionary[self.PAD]]

			# append index value
			seq_input_index.append(seq_index)

		return np.asarray(seq_input_index), seq_len


	def enc_processing(self, value, dictionary):
		"""
		seq_input_index : index data
		seq_len : length of sentence
		"""
		seq_input_index = []
		seq_len = []

		# noise canceling
		if DEFINES.xavier_initializer:
			value = self.tokenizing_data(value)

		for seq in value:
			seq_index = []
			for word in seq:
				if dictionary.get(word) is not None:
					# set word index
					seq_index.append(dictionary[word])
				else:
					# word is none
					seq_index.append(dictionary[self.UNK])

			# remove length over token
			if len(seq_index) > DEFINES.max_sequence_length:
				seq_index = seq_index[:DEFINES.max_sequence_length]

			# set seq_length
			seq_len.append(len(seq_index))

			# if shorter than max_sequence_length add padding
			seq_index += (DEFINES.max_sequence_length - len(seq_index)) * [dictionary[self.PAD]]
			seq_input_index.append(seq_index)

		return np.asarray(seq_input_index), seq_len


	def tokenizing_data(self, data):
		morph_analyzer = Okt()
		result_data = list()
		for seq in tqdm(data):
			seq = self.prepro_noise_canceling(seq)
			morphlized_seq = " ".join(morph_analyzer.morphs(seq.replace(' ', '')))
			result_data.append(morphlized_seq)

		return result_data


	def prepro_noise_canceling(self, text):

		# text normalization
		sentence = re.sub(re.compile("([~.,!?\"':;)(])"),"",str(text))


		return sentence


	def load_data(self):
		# Get data
		data_frame = pd.read_csv("./data_in/ChatBotData.csv", header=0)
		question = list(data_frame['Q'])
		answer = list(data_frame['A'])

		# split data using scikit-learn
		train_q, test_q, train_a, test_a = train_test_split(question, answer, test_size=0.33, random_state=42)

		return train_q, train_a, test_q, test_a


	def in_out_dict(self, input, output, target):
		features = {"input": input, "output": output}
		return features, target


	def eval_input_fn(self, encode_train, decode_output_train, decode_target_train, batch_size):
		# Make dataset splited each sentence
		dataset = tf.data.Dataset.from_tensor_slices((encode_train, decode_output_train, decode_target_train))

		# Shuffled whole dataset
		dataset = dataset.shuffle(buffer_size=len(encode_train))

		# Assert error, batch_size is not None
		assert batch_size is not None, "train batchSize must not be None"

		# Batch
		dataset = dataset.batch(batch_size, drop_remainder=True)

		dataset = dataset.map(self.in_out_dict)
		dataset = dataset.repeat(1)

		iterator = dataset.make_one_shot_iterator()

		return iterator.get_next()


	def train_input_fn(self, encode_train, decode_output_train, decode_target_train, batch_size):
		# Make dataset splited each sentence
		dataset = tf.data.Dataset.from_tensor_slices((encode_train, decode_output_train, decode_target_train))

		# Shuffled whole dataset
		dataset = dataset.shuffle(buffer_size=len(encode_train))

		# Assert error, batch_size is not None
		assert batch_size is not None, "train batchSize must not be None"

		# Batch
		dataset = dataset.batch(batch_size, drop_remainder=True)

		dataset = dataset.map(self.in_out_dict)
		dataset = dataset.repeat()

		iterator = dataset.make_one_shot_iterator()

		return iterator.get_next()


def main(self):
	data = PreProcessing()
	char_to_idx, idx_to_char, voc_len = data.load_voc()



if __name__ == '__main__':
	tf.logging.set_verbosity(tf.logging.INFO)
	tf.app.run(main)