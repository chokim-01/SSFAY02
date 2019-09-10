import numpy as np
import pickle
from scipy.sparse import lil_matrix
from konlpy.tag import Okt
from os.path import isfile

LOGISTIC_PATH = "./Logistic_data"
word_indices = dict()


class LogisticRegressionClassifier(object):
    x_scope = 0
    c_bias = 0

    # Sigmoid: S-shaped graph (return value between 0 and 1)
    # Implement: y = 1 / (1 + e^(-z))
    def sigmoid(self, z):
        """
        :param z: true value
        :return: sigmoid of z
        """

        return 1 / (1 + np.exp(-z))

    # Calculated Prediction probability (class=1)
    def prediction(self, x_scope, c_bias, X):
        """
        :param x_scope: Weight
        :param c_bias: Bias
        :param X: Input data
        :return: Prediction probability
        """

        return self.sigmoid(X.dot(np.array(x_scope).T) + c_bias)

    # Calculate gradient descent to adjust weights
    def gradient_beta(self, X, error, lr):
        """
        :param X: input data
        :param error: difference between the true value(Y) and predicted value
        :param lr: learning rate
        :return: slope, bias's weights
        """

        # delta: learning rate * derivation of Cost
        x_weight_delta = lr * (-1 / X.shape[1]) * lil_matrix.dot(error.reshape(1, -1), X)
        c_weight_delta = lr * (-1 / X.shape[1]) * sum(error)

        return x_weight_delta, c_weight_delta

    def train(self, X, Y):
        """
        :param X: input data X_train
        :param Y: Input data Y_train
        :return: adjusted weights of slope and bias
        """

        # lr: Set learning rate
        # iters: Set iteration
        lr = 0.15
        iters = 10000

        # Initialize x_weight, c_weight
        x_weight = np.array([[0] * X.shape[1]], dtype="float64")
        c_weight = 0

        Y = Y.reshape(len(Y), 1)

        for i in range(iters):
            # error : difference between true value(Y) and predicted value
            error = Y - self.prediction(x_weight, c_weight, X).reshape(-1,1)
            # update delta values with gradient descent
            x_weight_delta, c_weight_delta = self.gradient_beta(X, error, lr)
            x_weight -= x_weight_delta
            c_weight -= c_weight_delta

        self.x_scope = x_weight
        self.c_bias = c_weight

        return self.x_scope, self.c_bias

    def classify(self, X_test):
        """
        :param X_test: Input test data
        :return: predicted data
        """

        result = self.sigmoid(X_test.dot(np.array(self.x_scope).T) + self.c_bias)

        if result >= 0.5:
            return 1
        else:
            return 0

    def predict(self, X_test):
        """
        :param X_test: value to predict
        :return: predicted data with classified value
        """

        predictions = []
        X_test = X_test.toarray()

        if len(X_test) == 1:
            predictions.append(self.classify(X_test))
        else:
            for case in X_test:
                predictions.append(self.classify(case))

        return predictions

    def score(self, X_test, Y_test):
        """
        :param X_test: test data to predict
        :param Y_test: X_test's label
        :return: accuracy score
        """

        loss = Y_test.reshape(-1,1) - np.array(self.predict(X_test)).reshape(-1,1)
        count = 0

        for idx in range(len(loss)):
            if loss[idx] == 0:
                count += 1

        return count / len(Y_test)


def train_model():
    model2 = LogisticRegressionClassifier()

    # Open train_data
    x_train_data_path = LOGISTIC_PATH + "/X_train_model.clf"
    if isfile(x_train_data_path):
        print("[+] open x_train model")
        with open(x_train_data_path, 'rb') as f:
            x_data = pickle.load(f)

        y_train_data_path = LOGISTIC_PATH + "/Y_train_model.clf"
        if isfile(y_train_data_path):
            print("[+] open y_train model")
            with open(y_train_data_path, 'rb') as f:
                y_data = pickle.load(f).reshape(-1, 1)

            # Train
            print("[+] train models")
            model2.train(x_data, y_data)

            pickle.dump(model2, open(LOGISTIC_PATH+"/logistic_model_e15_10000.clf", "wb"))


def test_model():
    model_path = LOGISTIC_PATH + "/logistic_model_e15_10000.clf"
    if isfile(model_path):
        with open(model_path, 'rb') as f:
            res_data = pickle.load(f)

    x_test_data_path = LOGISTIC_PATH + "/X_test_model.clf"
    if isfile(x_test_data_path):
        with open(x_test_data_path, 'rb') as f:
            x_test = pickle.load(f)

        y_test_data_path = LOGISTIC_PATH + "/Y_test_model.clf"
        if isfile(y_test_data_path):
            with open(y_test_data_path, 'rb') as f:
                y_test = pickle.load(f)

            print("Logistic_Regression_Classifier accuracy: {}".format(res_data.score(x_test, y_test)))


# make word_indices
def make_word_indices():
    global word_indices

    word_indices_path = LOGISTIC_PATH + "/word_indices.dat"
    if isfile(word_indices_path):
        with open(word_indices_path, "rb") as model:
            word_indices = pickle.load(model)


def load_mention(mention, model):
    global word_indices

    mention_token_data = tokenize_data(mention)

    X_mention = lil_matrix((1, len(word_indices) + 1), dtype=np.int64)

    for token in mention_token_data:
        word = token.split("/")[0]
        if word in word_indices:
            X_mention[0, word_indices[word]] = 1

    res = model.predict(X_mention)

    return "긍정적 리뷰" if res[0] else "부정적 리뷰"


# Tokenize data
def tokenize_data(data_row):
    okt = Okt()
    return ['/'.join(t) for t in okt.pos(data_row, norm=True, stem=True)]


def use_model():
    model_path = LOGISTIC_PATH + "/logistic_model_e1_10000.clf"
    if isfile(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        make_word_indices()

        print("문장을 입력하세요: ", end='')
        txt = input()
        print(load_mention(txt, model)+"\n")

    else:
        print("[ERROR] Cannot open model")


def main():
    while True:
        print("#####################")
        print("1. 모델 학습")
        print("2. 모델 학습 검증")
        print("3. 사용하기")
        print("4. 종료")
        print("#####################")
        print("기능을 선택하세요.: ", end='')
        num = int(input())

        if num == 1:
            train_model()
        elif num == 2:
            test_model()
        elif num == 3:
            use_model()
        else:
            break


if __name__ == "__main__":
    main()

