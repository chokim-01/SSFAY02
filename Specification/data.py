import re
import pandas as pd


class PreProcessing:
	def __init__(self):
		self.train_percent = 0.8

	def pred_next_string(self):
		return ""

	def load_voc(self):
		return ""

	def make_voc(self):
		return ""

	def dec_target_processing(self):
		return ""

	def dec_output_processing(self):
		return ""

	def enc_processing(self):
		return ""

	def tokenizing_data(self):
		return ""

	def prepro_noise_canceling(self, question_train, question_test, answer_train, answer_test):
		"""
		:param question_train: train question data
		:param question_test: test question data
		:param answer_train: train answer data
		:param answer_test: test answer data
		:return: noise canceling each train and test data
		"""

		remove_characters = "[~.,!?\"':;)(]"

		train_len = len(question_train)
		test_len = len(question_test)

		for idx in range(train_len):
			question_train[idx] = re.sub(remove_characters, "", question_train[idx][0])
			answer_train[idx] = re.sub(remove_characters, "", answer_train[idx][0])

		for idx in range(test_len):
			question_test[idx] = re.sub(remove_characters, "", question_test[idx][0])
			answer_test[idx] = re.sub(remove_characters, "", answer_test[idx][0])

		return question_train, question_test, answer_train, answer_test

	def load_data(self):
		"""
		:return: question_train, question_test, answer_train, answer_test
		"""

		# Get chatbot data
		data_frame = pd.read_csv("./data_in/ChatBotData.csv")

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
