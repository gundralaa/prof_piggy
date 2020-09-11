'''
Model outline for monologue generation
algorithm. A simply char embedded rnn used initially
plans to extend to word embeddings
'''
import tensorflow as tf
import numpy as np
import os
import time

# Generator Model
class GeneratorModel():
    # model params
    def __init__(self, vocab_len, char_indx, indx_char, checkpoint_dir):
        self.vocab_len = vocab_len
        self.embedding_dim = 256
        self.rnn_units = 1024
        self.batch_size = 1
        # training
        self.optimizer = tf.keras.optimizers.Adam()
        self.model = None
        self.seq_len = 200
        # loading
        self.loaded = False
        self.checkpoint_dir = checkpoint_dir
        # index transformation
        self.char_indx = char_indx
        self.indx_char = indx_char
    # build model
    def build(self, training=False):
        if training:
            self.batch_size = 64
        else:
            self.batch_size = 1
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(self.vocab_len, 
                self.embedding_dim,
                batch_input_shape=[self.batch_size, None]),
            tf.keras.layers.LSTM(self.rnn_units,
                return_sequences=True,
                recurrent_initializer='glorot_uniform',
                recurrent_activation='sigmoid',
                stateful=True),
            tf.keras.layers.Dense(self.vocab_len)
        ])
        self.model = model
        return model
    # gradient calc and apply to weights
    @tf.function
    def loss_calc_apply(self, input, target):
        with tf.GradientTape() as tape:
            predictions = self.model(input)
            loss = tf.keras.losses.sparse_categorical_crossentropy(
                    target, predictions, from_logits=True)
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        return loss
    # training loop
    # input vector must be shape (R,)
    def train(self, text_vector, iterations):
        text_vector = np.array(text_vector)
        self.loaded = False
        self.build(training=True)
        # checkpoint location
        checkpoint_prefix = os.path.join(self.checkpoint_dir, "my_ckpt")
        for count in range(iterations):
            # extract sample batch
            input_batch, target_batch = self.get_batch(text_vector)
            # calculate loss
            loss = self.loss_calc_apply(input_batch, target_batch)
            print(count, loss.numpy().mean())
            # save updated weights
            if count % 100 == 0:
                self.model.save_weights(checkpoint_prefix)
    # batching
    def get_batch(self, text_vector):
        text_len = text_vector.shape[0] - 1
        rand_indx = np.random.choice(text_len - self.seq_len, self.batch_size)
        # in batch
        in_batch = [text_vector[i:i+self.seq_len] for i in rand_indx]
        # out batch
        out_batch = [text_vector[i+1:i+self.seq_len+1] for i in rand_indx]
        x_batch = np.reshape(in_batch, [self.batch_size, self.seq_len])
        y_batch = np.reshape(out_batch, [self.batch_size, self.seq_len])
        return x_batch, y_batch
    # prediction
    def generate_line(self, init_string, temp):
        max_gen_length = 100
        if not self.loaded:
            self.build()
            self.model.load_weights(
                tf.train.latest_checkpoint(
                    self.checkpoint_dir))
            self.model.build(tf.TensorShape([1, None]))
            self.loaded = True
        # change init string to char vector using cipher
        init_vec = [self.char_indx[c] for c in init_string]
        init_vec = tf.expand_dims(init_vec, 0)
        # generated text
        text_out = []
        self.model.reset_states()
        for i in range(50):
            predictions = self.model(init_vec)
            predictions = tf.squeeze(predictions, 0) / temp
            predicted_id = tf.random.categorical(
                predictions, num_samples=1)[-1,0].numpy()
            # feed prediction back as input
            init_vec = tf.expand_dims([predicted_id], 0)
            predicted_char = self.indx_char[predicted_id]
            text_out.append(predicted_char)
            if predicted_char == '.':
              break
        return ''.join(text_out)

            