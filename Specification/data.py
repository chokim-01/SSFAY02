import re
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split
from os.path import exists
from config import DEFINES


class PreProcessing:
	def __init__(self):
		self.PAD = "<PAD>"
		self.STD = "<STD>"
		self.END = "<END>"
		self.UNK = "<UNK>"
		self.PAD_INDEX = 0
		self.STD_INDEX = 1
		self.END_INDEX = 2
		self.UNK_INDEX = 3

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

		print(dataset)

		dataset = dataset.repeat(1)

		iterator = dataset.make_one_shot_iterator()

		print("vvv", iterator.get_next())

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

	def pred_next_string(self, message, idx2voca_dictionary):
		message_string = []

		indexs = list(message)[0]
		print(indexs)
		#message_string = [idx2voca_dictionary[index] for index in list(message)[0]["indexs"]]

		answer = ""

		for msg in message_string:
			if msg not in self.PAD and msg not in self.END:
				answer += msg
				answer += " "

		return answer

	def load_voc(self):
		"""
		Load voc file If exist VocabularyData.voc
		:return: voca to idx, idx to voca, length of voca
		"""
		vocabulary = []
		exist_check = False

		# If exist vocabularyData.voc
		if exists(DEFINES.vocabulary_path):
			exist_check = True
			# Read vocabulary file
			with open(DEFINES.vocabulary_path, "r", encoding="utf-8") as file:
				# Remove space each line
				for line in file:
					vocabulary.append(line.strip())
		else:
			# If exists data
			if exists(DEFINES.data_path):
				# Get chatbot data
				data_frame = pd.read_csv(DEFINES.data_path)

				# Get question and answer data
				question_and_answer = data_frame[["Q", "A"]].values

				for sentence in question_and_answer:

					# Remove special characters
					noise_cancel_sentence_0 = self.prepro_noise_canceling([sentence[0]])
					noise_cancel_sentence_1 = self.prepro_noise_canceling([sentence[1]])

					# Tokenize sentence
					tokenize_sentence_0 = self.tokenize_data(noise_cancel_sentence_0)
					tokenize_sentence_1 = self.tokenize_data(noise_cancel_sentence_1)

					# Make vocabulary dictionary
					vocabulary += tokenize_sentence_0[0]
					vocabulary += tokenize_sentence_1[0]

				# Remove duplicate
				vocabulary = list(set(vocabulary))
				vocabulary[:0] = [self.PAD, self.STD, self.END, self.UNK]

				# Save vocabulary
				with open(DEFINES.vocabulary_path, "w", encoding="utf-8") as file:
					for voca in vocabulary:
						file.write(voca + "\n")
			else:
				print("Check data or path")

		voca2idx, idx2voca = self.make_voc(vocabulary)

		return voca2idx, idx2voca, len(voca2idx)

	def make_voc(self, vocabulary):
		"""

		:param vocabulary: sentence splited by space
		:return: voca to index, index to voca
		"""
		voca2idx = {word: idx for idx, word in enumerate(vocabulary)}
		idx2voca = {idx: word for idx, word in enumerate(vocabulary)}

		return voca2idx, idx2voca

	def dec_target_processing(self, message, voca_dictionary):
		message_target_index = []

		for msg in message:
			msg_index = [voca_dictionary[voca] for voca in msg]

			if len(msg_index) >= DEFINES.max_sequence_length:
				msg_index = msg_index[:DEFINES.max_sequence_length+1] + [voca_dictionary[self.END]]
			else:
				msg_index += [voca_dictionary[self.END]]

			msg_index += (DEFINES.max_sequence_length - len(msg_index)) * [voca_dictionary[self.PAD]]
			message_target_index.append(msg_index)

		return np.asarray(message_target_index)

	def dec_output_processing(self, message, voca2idx_dictionary):
		message_output_index = []
		message_output_length = []

		for msg in message:
			msg_index = [voca2idx_dictionary[self.STD]] + [voca2idx_dictionary[voca] for voca in msg]

			if len(msg_index) > DEFINES.max_sequence_length:
				msg_index = msg_index[:DEFINES.max_sequence_length]

			message_output_length.append(len(msg_index))
			msg_index += (DEFINES.max_sequence_length - len(msg_index)) * [voca2idx_dictionary[self.PAD]]
			message_output_index.append(msg_index)

		print("dec", message_output_index)
		return np.asarray(message_output_index), message_output_length

	def enc_processing(self, message, voca2idx_dictionary):
		"""

		:param message: noise_canceled and tokenized message
		:param voca2idx_dictionary: tokenize word and index
		:return: message index as np.array and message length
		"""

		# Message index list
		message_index = []

		# Message length list
		message_length = []

		for msg in message:
			# Each message index
			msg_index = []

			for word in msg:
				word_idx = voca2idx_dictionary.get(word)

				# If word exist in voca_dictionary
				if word_idx is not None:
					# Append voca_dictionary index
					msg_index.append(word_idx)

				# If not exist in voca_dictionary
				else:
					# Append UNK_INDEX
					msg_index.append(voca2idx_dictionary[self.UNK])

			# If message length over max_sequence_length
			if len(msg_index) > DEFINES.max_sequence_length:
				msg_index = msg_index[:DEFINES.max_sequence_length]

			message_length.append(len(msg_index))

			msg_index += (DEFINES.max_sequence_length - len(msg_index)) * [voca2idx_dictionary[self.PAD]]
			message_index.append(msg_index)

		return np.array(message_index), message_length

	def tokenize_data(self, message):
		"""
		:param message: sentence, 2D array
		:return: tokenize data
		"""
		message_len = len(message)

		tokenize_data = [0 for _ in range(message_len)]

		if message_len == 1:
			tokenize_data[0] = message[0].split()
		elif message_len == 0:
			print("Check message")
		else:
			for idx in range(message_len):
				tokenize_data[idx] = message[idx][0].split()

		return tokenize_data

	def prepro_noise_canceling(self, message):
		"""
		:param message: sentence, 2D array
		:return: noise canceling message
		"""

		remove_characters = "[~.,!?\"':;)(]"

		message_len = len(message)

		if message_len == 1:
			message[0] = re.sub(remove_characters, "", message[0])
		elif message_len == 0:
			print("Check message")
		else:
			for idx in range(message_len):
				message[idx] = re.sub(remove_characters, "", message[idx][0])

		return message

	def load_data(self):
		"""
		:return: question_train, question_test, answer_train, answer_test
		"""

		# Get chatbot data
		data_frame = pd.read_csv(DEFINES.data_path)
		self.question_and_answer = data_frame[["Q", "A"]].values

		# Get question data
		question = data_frame[["Q"]].values

		# Get answer data
		answer = data_frame[["A"]].values

		question_train, answer_train, question_test, answer_test = \
			train_test_split(question, answer, test_size=0.33, random_state=42)

		return question_train, question_test, answer_train, answer_test

if __name__ == '__main__':
	tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
	pre_processing = PreProcessing()
	tf.compat.v1.app.run(pre_processing)
