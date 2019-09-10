import pandas as pd
import re
import os

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


	def pred_next_string(self):
		return ""


	def load_voc(self):

		# dictionary data
		voc_list = []

		# create dictionary
		if (not (os.path.exists(DEFINES.vocabulary_path))):
			# get data
			data_frame = pd.read_csv("./data_in/ChatBotData.csv", sep=',').dropna()[["Q", "A", "label"]].values
			question = data_frame[:, [0]]
			answer = data_frame[:, [1]]

			data = []
			data.extend(question)
			data.extend(answer)

			# normalization data
			data = self.prepro_noise_canceling(data)

			# tokenization data
			words = []
			for idx in data:
				words.extend(self.tokenizing_data(idx))

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
		char_to_idx, idx_to_char = self.make_voc(voc_list)

		return char_to_idx, idx_to_char, len(voc_list)


	def make_voc(self, voc_list):
		
		char_to_idx = {}
		idx_to_char = {}

		for idx in range(len(voc_list)):
			word = voc_list[idx]
			char_to_idx[word] = idx
			idx_to_char[idx] = word

		return char_to_idx, idx_to_char


	def dec_target_processing(self):
		return ""

	def dec_output_processing(self):
		return ""

	def enc_processing(self, value, dictionary):
		"""
		seq_input_index : index data
		seq_len : length of sentence
		"""

		seq_input_index = []
		seq_len = []

		# noise canceling`
		value = self.prepro_noise_canceling(value)

		for seq in value:


			seq_index = []


		return ""

	def tokenizing_data(self, text):
		# tokenized data
		tokenized_data = []

		# text tokenization
		str_split = text.split()
		for word in str_split:
			tokenized_data.append(word)

		return tokenized_data


	def prepro_noise_canceling(self, data):
		# result_data
		noise_canceled_data = []

		# text normalization
		for idx in range(len(data)):
			noise_canceled_data.append(re.sub("[~.,!?\"':;)(]",'',data[idx][0]))

		return noise_canceled_data


	def load_data(self):
		# Get data
		data_frame = pd.read_csv("./data_in/ChatBotData.csv", sep=',').dropna()[["Q", "A", "label"]].values

		question = data_frame[:, [0]]
		answer = data_frame[:, [1]]

		# split data using scikit-learn
		train_q, train_a, test_q, test_a = train_test_split(question, answer, test_size=0.33)

		return train_q, train_a, test_q, test_a


def main():
	data = PreProcessing()
	data.load_voc()


if __name__ == '__main__':
    main()