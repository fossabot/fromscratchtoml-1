#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Mohit Rathore <mrmohitrathoremr@gmail.com>
# Licensed under the GNU General Public License v3.0 - https://www.gnu.org/licenses/gpl-3.0.en.html

import numpy as np
from functools import partial

from .. import Activations

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Dense(object):
    def __init__(self, units, input_dim=None):
        self.units = units
        self.biases = None
        self.weights = None

        if input_dim:
            self.biases = np.random.randn(self.units, 1)
            self.weights = np.random.randn(input_dim, self.units)

    def initialize_params(self, input_dim):
        self.biases = np.random.randn(input_dim, 1)
        self.weights = np.random.randn(input_dim, self.units)

    def forward(self, X, return_deriv=False):
        if len(X.shape) == 1:
            X = np.expand_dims(X, axis=1)
        print("layer has ", self.units)
        if self.weights is None:
            self.biases = np.random.randn(self.units, 1)
            self.weights = np.random.randn(X.shape[0], self.units)

        self.input = X
        self.output = np.dot(self.weights.T, X) + self.biases
        if return_deriv:
            return self.output, 0

        return self.output

    def back_propogate(self, delta):
        # print("popo")
        # print(delta.shape)
        # print(self.weights.shape)
        delta = np.dot(self.weights, delta)
        return delta

    def optimize(self, optimizer, der_cost_bias, der_cost_weight):
        self.weights = optimizer.update_weights(self.weights, der_cost_weight)
        self.biases = optimizer.update_weights(self.biases, der_cost_bias)


class Activation(object):
    def __init__(self, activation=None):
        self.activation = partial(getattr(Activations, activation))

    def forward(self, X, return_deriv=False):
        self.input = X
        self.output, self.output_deriv = self.activation(X, return_deriv=True)

        if return_deriv:
            return self.output, self.output_deriv

        return self.output

    def back_propogate(self, delta):
        delta = delta * self.output_deriv

        return delta

    def optimize(self, optimizer, der_cost_bias, der_cost_weight):
