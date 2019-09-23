import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_frame = pd.read_csv("./Data/result_train_val.txt", header=0).dropna()

train_step = data_frame["train_step"].values
accuracy = data_frame["accuracy"].values * 100

plt.plot(train_step, accuracy, "rs--")
plt.xlabel('train step')
plt.ylabel('accuracy')
plt.axis([train_step[0], train_step[-1], accuracy[0], 84])

plt.show()

