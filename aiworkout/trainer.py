
#local functions
from get_data import get_img

#libraries
import numpy as np
import joblib

import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras import Sequential, layers

from sklearn.model_selection import train_test_split

class Trainer():

    def __init__(self,X,y):
        self.X = X
        self.y = y


    def build_model(self):

        model = VGG16(weights="imagenet", include_top=False, input_shape=(256,256,3))
        model.trainable = False

        flatten_layer = layers.Flatten()
        dense_layer = layers.Dense(500, activation='relu')
        dropout_layer = layers.Dropout(rate=0.2)
        prediction_layer = layers.Dense(3, activation='softmax')

        self.model = Sequential([
                    model,
                    flatten_layer,
                    dense_layer,
                    dropout_layer,
                    prediction_layer
            ])

        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adam',
                           metrics=['accuracy'])

        return self.model

    def run(self):

        self.build_model()
        self.model.fit(self.X,self.y)


    def evaluate(self,X_test,y_test):

        res = self.model.evaluate(X_test,y_test)
        accuracy = round(res[-1],2)

        return accuracy

    def save_model(self):
        joblib.dump(self.model,'vggmodel.joblib')
        print('vggmodel saved locally')


if __name__ == "__main__":

    X , y = get_img()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    trainer = Trainer(X=X_train,y=y_train)

    print('Training Model')
    trainer.run()

    print('Evaluate Model')
    acc = trainer.evaluate(X_test,y_test)
    print(acc)

    print('Save Model')
    trainer.save_model()