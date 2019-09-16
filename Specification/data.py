import re
import pickle
import pandas as pd
from config import DEFINES


class PreProcessing:
	def __init__(self):
		self.train_percent = 0.8
		self.question_and_answer = None
		self.PAD = "<PAD>"
		self.STD = "<SOS>"
		self.END = "<END>"
		self.UNK = "<UNK>"
		self.PAD_INDEX = 0
		self.STD_INDEX = 1
		self.END_INDEX = 2
		self.UNK_INDEX = 3

	def pred_next_string(self):
		return ""

	def load_voc(self):
		with open('./Data/voca_dictionary.dat', 'rb') as file:
			return pickle.load(file)

	def make_voc(self):
		"""

		:return: None
		"""

		# Set initialize dict
		voca_dictionary = {self.PAD: self.PAD_INDEX, self.STD: self.STD_INDEX,
							self.END: self.END_INDEX, self.UNK: self.UNK_INDEX}

		# Insert voca and index
		idx = 4
		for sentence in self.question_and_answer:

			# Remove special word
			noise_cancel_sentence_0 = self.prepro_noise_canceling([sentence[0]])
			noise_cancel_sentence_1 = self.prepro_noise_canceling([sentence[1]])

			# Tokenize sentence
			tokenize_sentence_0 = self.tokenize_data(noise_cancel_sentence_0)
			tokenize_sentence_1 = self.tokenize_data(noise_cancel_sentence_1)

			# Insert token and index
			for token in tokenize_sentence_0[0]:
				voca_dictionary[token] = idx
				idx += 1

			for token in tokenize_sentence_1[0]:
				voca_dictionary[token] = idx
				idx += 1

		# Make voca_dictionary file
		pickle.dump(voca_dictionary, open("./Data/voca_dictionary.dat", "wb"))

	def dec_target_processing(self):
		return ""

	def dec_output_processing(self):
		return ""

	def enc_processing(self, message, voca_dictionary):

		# Message index list
		message_index = []

		# Message length list
		message_len = []

		noise_cancel_message = self.prepro_noise_canceling(message)

		for msg in noise_cancel_message:
			# Each message index
			msg_index = []

			split_message = msg.split()

			# Check msg_len
			msg_len = len(split_message)

			for word in split_message:
				word_idx = voca_dictionary.get(word)

				# If word exist in voca_dictionary
				if word_idx is not None:
					# Append voca_dictionary index
					msg_index.append(word_idx)

				# If not exist in voca_dictionary
				else:
					# Append UNK_INDEX
					msg_index.append(self.UNK_INDEX)

			# If message length over max_sequence_length
			if msg_len > DEFINES.max_sequence_length:
				msg_index = msg_index[:DEFINES.max_sequence_length]
				message_len.append(len(msg_index))
			else:
				padding = [self.PAD_INDEX for _ in range(DEFINES.max_sequence_length - len(msg_index))]
				message_len.append(len(msg_index))
				msg_index += padding

			message_index.append(msg_index)

		return message_index, message_len

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
		data_frame = pd.read_csv("./data_in/ChatBotData.csv")
		self.question_and_answer = data_frame[["Q", "A"]].values

		# Get question data
		question = data_frame[["Q"]].values

		# Get answer data
		answer = data_frame[["A"]].values

		# Calculate percent
		data_len = len(data_frame)
		train_index = round(data_len * self.train_percent)

		# Divide question, answer for train ans test
		question_train = question[:train_index]
		question_test = question[train_index:]

		answer_train = answer[:train_index]
		answer_test = answer[train_index:]

		return question_train, question_test, answer_train, answer_test
