import pandas as pd
import re
from sklearn.model_selection import train_test_split


class PreProcessing:

	def __init__(self):
		self.val = 0

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

	def tokenizing_data(self, text):
		# tokenized data
		tokenized_data = []

		# text tokenization
		for idx in range(len(text)):
			str_split = text[idx].split()
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
	train_q, train_a, test_q, test_a = data.load_data()
	noise_canceled = data.prepro_noise_canceling(test_a)
	tokenized_data = data.tokenizing_data(noise_canceled)
	print(tokenized_data)

if __name__ == '__main__':
    main()