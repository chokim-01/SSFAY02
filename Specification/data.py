import pandas as pd
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

	def tokenizing_data(self):
		return ""

	def prepro_noise_canceling(self):
		return ""

	def load_data(self):
		# Get data
		data_frame = pd.read_csv("./data_in/ChatBotData.csv", sep=',').dropna()[["Q", "A", "label"]].values

		question = data_frame[:, [0]]
		answer = data_frame[:, [1]]

		# split data
		train_q, train_a, test_q, test_a = train_test_split(question, answer, test_size=0.33)

		return train_q, train_a, test_q, test_a


def main():
	data = PreProcessing()
	data.load_data()

if __name__ == '__main__':
    main()