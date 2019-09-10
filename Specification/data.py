import re
import pickle
import pandas as pd


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
		return ""

	def make_voc(self):
		voca_dictionary = {"<PAD>": 0, "<SOS>": 1, "<END>": 2, "<UNK>": 3}

		idx = 4
		for sentence in self.question_and_answer:

			noise_cancel_sentence_0 = self.prepro_noise_canceling([sentence[0]])
			noise_cancel_sentence_1 = self.prepro_noise_canceling([sentence[1]])

			tokenize_sentence_0 = self.tokenize_data(noise_cancel_sentence_0)
			tokenize_sentence_1 = self.tokenize_data(noise_cancel_sentence_1)

			for token in tokenize_sentence_0[0]:
				voca_dictionary[token] = idx
				idx += 1

			for token in tokenize_sentence_1[0]:
				voca_dictionary[token] = idx
				idx += 1

		pickle.dump(voca_dictionary, open("./Data/voca_dictionary.dat", "wb"))

	def dec_target_processing(self):
		return ""

	def dec_output_processing(self):
		return ""

	def enc_processing(self, message, voca_dictionary):

		return ""

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
