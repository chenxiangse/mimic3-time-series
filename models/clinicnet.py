from __future__ import absolute_import
from __future__ import print_function

from keras.models import Model
from keras.layers import Input, Dense, LSTM, Masking, Dropout, GRU
from keras.layers.wrappers import Bidirectional, TimeDistributed
from utils.keras_utils import LastTimestep
from utils.keras_utils import ExtendMask
from keras_self_attention import SeqSelfAttention
import keras


class Network(Model):

    def __init__(self, dim, batch_norm, dropout, rec_dropout, task,
                 target_repl=False, deep_supervision=False, num_classes=1,
                 depth=1, input_dim=76, **kwargs):

        print("==> not used params in network class:", kwargs.keys())

        self.dim = dim
        self.batch_norm = batch_norm
        self.dropout = dropout
        self.rec_dropout = rec_dropout
        self.depth = depth

        if task in ['decomp', 'ihm', 'ph']:
            final_activation = 'sigmoid'
        elif task in ['los']:
            if num_classes == 1:
                final_activation = 'relu'
            else:
                final_activation = 'softmax'
        else:
            raise ValueError("Wrong value for task")

        # Input layers and masking
        X = Input(shape=(None, input_dim), name='X')

        print("X-> " , X)

        inputs = [X]
        print("input->", inputs)
        mX = Masking()(X)

        if deep_supervision:
            M = Input(shape=(None,), name='M')
            inputs.append(M)

        # Configurations
        is_bidirectional = False
        if deep_supervision:
            is_bidirectional = False

        # Main part of the network
        '''
        for i in range(depth - 1):
            num_units = dim
            if is_bidirectional:
                num_units = num_units // 2

            lstm = LSTM(units=num_units,
                        activation='tanh',
                        return_sequences=True,
                        recurrent_dropout=rec_dropout,
                        dropout=dropout)

            if is_bidirectional:
                mX = Bidirectional(lstm)(mX)
            else:
                mX = lstm(mX)
        '''

        # Output module of the network
        return_sequences = (target_repl or deep_supervision)
        '''
        L = LSTM(units=dim,
                 activation='tanh',
                 return_sequences=return_sequences,
                 dropout=dropout,
                 recurrent_dropout=rec_dropout)(mX)
        '''

        L = SeqSelfAttention(
                attention_width=48,
                attention_type=SeqSelfAttention.ATTENTION_TYPE_MUL,
                attention_activation='sigmoid',
                kernel_regularizer=keras.regularizers.l2(1e-6),
                use_attention_bias=False,
                name='Attention',
            )(mX)

        
        L = GRU(units=dim,
                 activation='tanh',
                 return_sequences=return_sequences,
                 dropout=dropout,
                 recurrent_dropout=rec_dropout)(L)
        

        if dropout > 0:
            L = Dropout(dropout)(L)

        if target_repl:
            y = TimeDistributed(Dense(num_classes, activation=final_activation),
                                name='seq')(L)
            y_last = LastTimestep(name='single')(y)
            outputs = [y_last, y]
        elif deep_supervision:
            y = TimeDistributed(Dense(num_classes, activation=final_activation))(L)
            y = ExtendMask()([y, M])  # this way we extend mask of y to M
            outputs = [y]
        else:
            y = Dense(num_classes, activation=final_activation)(L)
            outputs = [y]

        super(Network, self).__init__(inputs=inputs, outputs=outputs)

    def say_name(self):
        return "{}.n{}{}{}{}.dep{}".format('k_clinicnet',
                                           self.dim,
                                           ".bn" if self.batch_norm else "",
                                           ".d{}".format(self.dropout) if self.dropout > 0 else "",
                                           ".rd{}".format(self.rec_dropout) if self.rec_dropout > 0 else "",
                                           self.depth)
