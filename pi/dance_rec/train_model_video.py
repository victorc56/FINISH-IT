import os
import numpy as np
import cv2
import tensorflow as tf
from keras.models import Sequential
from keras.layers import TimeDistributed, Conv2D, MaxPooling2D, Flatten, LSTM, Dense

num_classes = 3  # Update this based on the number of classes you have

model = Sequential([
    TimeDistributed(Conv2D(32, (3, 3), activation='relu'), input_shape=(None, 224, 224, 3)),
    TimeDistributed(MaxPooling2D(2, 2)),
    TimeDistributed(Conv2D(64, (3, 3), activation='relu')),
    TimeDistributed(MaxPooling2D(2, 2)),
    TimeDistributed(Flatten()),
    LSTM(50),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

class VideoFrameGenerator(tf.keras.utils.Sequence):
    def __init__(self, directory, classes, batch_size=16, frames_per_sequence=10, shuffle=True, resize=(224, 224)):
        self.directory = directory
        self.classes = classes
        self.batch_size = batch_size
        self.frames_per_sequence = frames_per_sequence
        self.shuffle = shuffle
        self.resize = resize
        self.class_indices = dict(zip(classes, range(len(classes))))
        self.samples = self._load_samples()
        self.indexes = np.arange(len(self.samples))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def _load_samples(self):
        samples = []
        for label in self.classes:
            class_dir = os.path.join(self.directory, label)
            for video_name in os.listdir(class_dir):
                video_path = os.path.join(class_dir, video_name)
                frames = [os.path.join(video_path, frame) for frame in sorted(os.listdir(video_path))]
                if len(frames) >= self.frames_per_sequence:
                    samples.append((frames, self.class_indices[label]))
        return samples

    def __len__(self):
        return int(np.floor(len(self.samples) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        batch_samples = [self.samples[k] for k in indexes]
        X, y = self._data_generation(batch_samples)
        return X, y

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def _data_generation(self, batch_samples):
        X = np.empty((self.batch_size, self.frames_per_sequence, *self.resize, 3), dtype=np.float32)
        y = np.empty((self.batch_size), dtype=np.int)
        for i, (frames, label) in enumerate(batch_samples):
            for j in range(self.frames_per_sequence):
                frame = cv2.imread(frames[j])
                frame = cv2.resize(frame, self.resize)
                frame = frame / 255.0  # Normalize pixel values
                X[i, j] = frame
            y[i] = label
        return X, tf.keras.utils.to_categorical(y, num_classes=len(self.classes))

# Example usage
train_gen = VideoFrameGenerator(
    directory='training_data_pi/',
    classes=['griddy', 'naenae', 'whip'],
    batch_size=2,  # Adjust based on your system's capability
    frames_per_sequence=5,  # Number of frames to include in each sequence
    shuffle=True,
    resize=(224, 224)  # Resize frames to fit the model input
)

# Then, use it with model.fit
model.fit(train_gen, epochs=10)
