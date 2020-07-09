import tensorflow as tf
import tf.keras as keras
from layers import BilinearUpSampling2D
from keras import backend as K

class UWPDmodel():
    def __init__(self):
        self.lr = 0.001
        self.model_path = ""
        self.epochs = 20

    def get_generator(self):
        pass

    def depth_loss_function(self, y_true, y_pred, theta=0.1, maxDepthVal=1000.0/10.0):
    
        # Point-wise depth
        l_depth = K.mean(K.abs(y_pred - y_true), axis=-1)

        # Edges
        dy_true, dx_true = tf.image.image_gradients(y_true)
        dy_pred, dx_pred = tf.image.image_gradients(y_pred)
        l_edges = K.mean(K.abs(dy_pred - dy_true) + K.abs(dx_pred - dx_true), axis=-1)

        # Structural similarity (SSIM) index
        l_ssim = K.clip((1 - tf.image.ssim(y_true, y_pred, maxDepthVal)) * 0.5, 0, 1)

        # Weights
        w1 = 1.0
        w2 = 1.0
        w3 = theta

        return (w1 * l_ssim) + (w2 * K.mean(l_edges)) + (w3 * K.mean(l_depth))
    
    def get_loss(self):
        pass

    def get_metrics(self):
        pass

    def get_callbacks(self):
        pass
    
    def get_model(self, model_path):
        custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': self.depth_loss_function}
        model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)

        return model

    
    def train(self):
        optimizer = keras.optimizer.Adam(self.lr, amsgrad=True)
        model = self.get_model(self.model_path)
        model.compile(loss=self.depth_loss_function, optimizer=optimizer)

        model.fit(
                    x = "" TODO,
                    callbacks= self.get_callbacks(), 
                    validation_data= TODO, 
                    epochs = self.epochs, 
                    shuffle=True)

if __name__ == "__main__":


    uwpd_model = UWPDmodel()
    uwpd_model.train()