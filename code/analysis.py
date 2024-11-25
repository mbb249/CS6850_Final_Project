import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load the CSV data
file_path = "../modified_data/feature_vectors.csv"
data = pd.read_csv(file_path)

# Separate features and labels
X = data.iloc[:, :-1].values  # All columns except the last one
y = data.iloc[:, -1].values  # The last column

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Data loaded and split successfully.")
print(f"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

# Define a simple neural network using TensorFlow
model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(
            128, activation="relu", input_shape=(X_train.shape[1],), name="Input_Layer"
        ),
        tf.keras.layers.Dense(64, activation="relu", name="Hidden_Layer_1"),
        tf.keras.layers.Dense(32, activation="relu", name="Hidden_Layer_2"),
        tf.keras.layers.Dense(
            1, activation="sigmoid", name="Output_Layer"
        ),  # Binary classification
    ]
)

# Compile the model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

print("Model defined and compiled successfully.")
model.summary()  # Print the model architecture


# Define a custom callback for logging
class TrainingLogger(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"\nEpoch {epoch + 1}:")
        print(
            f"  Training Loss: {logs['loss']:.4f}, Training Accuracy: {logs['accuracy']:.4f}"
        )
        print(
            f"  Validation Loss: {logs['val_loss']:.4f}, Validation Accuracy: {logs['val_accuracy']:.4f}"
        )


# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    callbacks=[TrainingLogger()],
    verbose=0,  # Suppress default verbose to use custom logging
)

# Evaluate the model on the test set
print("\nEvaluating model on test set...")
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")

# Predictions
print("\nGenerating predictions on the test set...")
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype("int32")

# Classification report
print("\nClassification Report:")
report = classification_report(y_test, y_pred, target_names=["Class 0", "Class 1"])
print(report)

# Final Accuracy
final_accuracy = accuracy_score(y_test, y_pred)
print(f"Final Test Accuracy: {final_accuracy:.4f}")
