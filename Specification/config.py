import tensorflow as tf

# Chatbot data path
tf.app.flags.DEFINE_string("chatbot_data_path", "./Data/ChatBotData.csv", "data path")

# Vocabulary data path
tf.app.flags.DEFINE_string("vocabulary_path", "./Data/VocabularyData.voc", "vocabulary path")

# Checkpoint path
tf.app.flags.DEFINE_string("check_point_path", "./Data_Output/check_point", "check point path")

# Using tokenize morpheme
tf.app.flags.DEFINE_boolean("tokenize_morpheme_flag", True, "Set morpheme tokenize")

# Max sentence length
tf.app.flags.DEFINE_integer("max_sentence_length", 25, "max sentence length")

# Weight size
tf.app.flags.DEFINE_integer("hidden_size", 128, "weights size")

# Layer size
tf.app.flags.DEFINE_integer("layer_size", 3, "layer size")

# Learning rate
tf.app.flags.DEFINE_float("learning_rate", 1e-3, "learning rate")

# Embedding size
tf.app.flags.DEFINE_integer("embedding_size", 128, "embedding size")

# Using embedding
tf.app.flags.DEFINE_boolean("embedding", True, "Use Embedding flag")

# Using multilayer
tf.app.flags.DEFINE_boolean("multilayer", True, "Use Multi RNN Cell")

# Train step
tf.app.flags.DEFINE_integer("train_steps", 20000, "train steps")

# Batch size
tf.app.flags.DEFINE_integer('batch_size', 64, 'batch size')

# Dropout width
tf.app.flags.DEFINE_float('dropout_width', 0.5, 'dropout width')

# Define FLAGS
DEFINES = tf.app.flags.FLAGS