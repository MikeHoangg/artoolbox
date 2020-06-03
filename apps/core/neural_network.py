from __future__ import absolute_import, division, print_function, unicode_literals
import struct
import json
import os

import tensorflow as tf
import numpy as np


def hex_to_float(hex_value):
    """
    Function for parsing hex colours to rgb
    :param hex_value:
    :return: tuple
    """
    hex_value = hex_value.lstrip('#')
    return struct.unpack('!f', bytes.fromhex(f'{hex_value}ff'))[0]


def load_data(raw_data):
    """
    Function for parsing json data
    :param raw_data: dict, json data
    :return: tuple, train colours and toolsets
    """

    train_colours = np.asarray(
        [np.asarray(sorted([hex_to_float(j) for j in json.loads(i['fields']['colours'])])) for i in raw_data])
    train_toolsets = np.asarray([i['fields']['toolset'] for i in raw_data])

    return train_colours, train_toolsets


def train_model(m_obj, train_data):
    """
    Function for training neural network model
    :param m_obj: obj, model obj
    :param train_data: list, list of dicts
    :return:
    """

    train_colours, train_toolsets = train_data

    m_obj.fit(train_colours, train_toolsets, epochs=10)


def export_model(m_obj, m_path, m_version):
    """
    Function for exporting trained model
    :param m_obj: obj, model obj
    :param m_path: str, path to save model
    :param m_version: int, version of model
    :return:
    """
    export_path = os.path.join(m_path, str(m_version))
    tf.compat.v1.keras.experimental.export_saved_model(m_obj, export_path)


if __name__ == '__main__':
    model_version = 1
    model_path = '/var/tmp/apps/models/artoolbox'
    model_training_file = '/var/tmp/dumps/db.json'

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    with open(model_training_file) as db_file:
        data = json.load(db_file)
    data = list(filter(lambda x: x['model'] == 'core.image', data))

    training_data = load_data(data)
    train_model(model, training_data)
    export_model(model, model_path, model_version)
