# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import sys
import uproot
import ROOT  # apt install -y libgl1-mesa-glx
import numba as nb

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import tensorflow as tf
import xgboost as xgb
import tensorflow_probability as tfp

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from kerastuner.tuners import RandomSearch
from functools import partial

# -----------------------------------------------------------------------------
# Basic Setup
# -----------------------------------------------------------------------------
print("Python version:", sys.version)
print("GPU Available:", tf.config.list_physical_devices('GPU'))

device = '/device:GPU:0' if tf.config.list_physical_devices('GPU') else '/device:CPU:0'
print(f"Using device: {device}")

# -----------------------------------------------------------------------------
# Test Pandas
# -----------------------------------------------------------------------------
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 28],
    'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)
print("DataFrame:")
print(df)

# -----------------------------------------------------------------------------
# Test Matplotlib
# -----------------------------------------------------------------------------
plt.figure()
plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
plt.title("Matplotlib Test")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()

# -----------------------------------------------------------------------------
# Test scikit-learn
# -----------------------------------------------------------------------------
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Random Forest
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)
rf_accuracy = accuracy_score(y_test, rf_classifier.predict(X_test))
print(f"Random Forest Accuracy: {rf_accuracy}")

# -----------------------------------------------------------------------------
# Test XGBoost
# -----------------------------------------------------------------------------
xgb_classifier = xgb.XGBClassifier(objective="multi:softmax", num_class=3)
xgb_classifier.fit(X_train, y_train)
xgb_accuracy = accuracy_score(y_test, xgb_classifier.predict(X_test))
print(f"XGBoost Accuracy: {xgb_accuracy}")

# -----------------------------------------------------------------------------
# Test TensorFlow Keras
# -----------------------------------------------------------------------------
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    Dense(10, activation='relu', input_shape=(4,)),
    Dense(3, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=5, verbose=0)
tf_predictions = np.argmax(model.predict(X_test), axis=1)
tf_accuracy = accuracy_score(y_test, tf_predictions)
print(f"TensorFlow Accuracy: {tf_accuracy}")

# -----------------------------------------------------------------------------
# Test Keras Tuner
# -----------------------------------------------------------------------------
def build_model(hp):
    mdl = Sequential([
        Dense(
            units=hp.Int('units', min_value=32, max_value=512, step=32),
            activation='relu',
            input_shape=(4,)
        ),
        Dense(3, activation='softmax')
    ])
    mdl.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return mdl

tuner = RandomSearch(
    build_model,
    objective='val_accuracy',
    max_trials=3,
    directory='keras_tuner',
    project_name='test_tuning'
)
tuner.search(X_train, y_train, epochs=5, validation_data=(X_test, y_test))

# -----------------------------------------------------------------------------
# Test mplhep
# -----------------------------------------------------------------------------
df = pd.DataFrame({'A': np.random.randn(1000), 'B': np.random.randn(1000)})
plt.figure()
plt.hist(df, bins=30, alpha=0.5, label=df.columns)
plt.legend(loc='upper right')
plt.title("mplhep Test")
plt.show()

# -----------------------------------------------------------------------------
# Test TensorFlow Probability
# -----------------------------------------------------------------------------
import tf_keras as tfk
tfd = tfp.distributions

print(f"TensorFlow version: {tf.__version__}")
print(f"TensorFlow Probability version: {tfp.__version__}")

def neg_log_lik(y, rv_y):
    return -rv_y.log_prob(y)

# Sample dataset
w0, b0 = 0.125, 5.0
n_samples = 150
x_range = [-20, 60]
x_domain = np.linspace(*x_range, n_samples)

def load_dataset(n=150, n_tst=n_samples):
    np.random.seed(27)
    def s(x):
        g = (x - x_range[0]) / (x_range[1] - x_range[0])
        return 3 * (0.25 + g**2.)
    x = (x_range[1] - x_range[0]) * np.random.rand(n) + x_range[0]
    eps = np.random.randn(n) * s(x)
    y = (w0 * x * (1. + np.sin(x)) + b0) + eps
    x = x[..., np.newaxis]
    x_tst = np.linspace(*x_range, num=n_tst).astype(np.float32)
    x_tst = x_tst[..., np.newaxis]
    return y, x, x_tst

ys, xs, xs_test = load_dataset()

def plot_training_data():
    plt.figure(figsize=(12, 7))
    plt.scatter(xs, ys, c="#619CFF", label="training data")
    plt.xlabel("x")
    plt.ylabel("y")

def plt_left_title(title):
    plt.title(title, loc="left", fontsize=18)

def plt_right_title(title):
    plt.title(title, loc='right', fontsize=13, color='grey')
    
plot_training_data()
plt_left_title("Training Data")

model_case_1 = tfk.Sequential([
    tfk.layers.Dense(1),
    tfp.layers.DistributionLambda(
        lambda t: tfd.Normal(loc=t, scale=1.0)
    )
])
model_case_1.compile(optimizer=tfk.optimizers.Adam(learning_rate=0.01), loss=neg_log_lik)
model_case_1.fit(xs, ys, epochs=500, verbose=False)

print(f"predicted w : {model_case_1.layers[-2].kernel.numpy()}")
print(f"predicted b : {model_case_1.layers[-2].bias.numpy()}")

yhat = model_case_1(xs_test)

plot_training_data()
plt_left_title("No Uncertainty")
plt_right_title("$Y \sim N(w_0 x + b_0, 1)$")
plt.plot(x_domain, yhat.mean(), "#F8766D", linewidth=5, label="mean")
plt.legend()
plt.show()

print("Finish!")
