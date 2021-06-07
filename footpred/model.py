from tensorflow.keras import layers
from tensorflow.keras import models
import tensorflow_addons as tfa

def get_model_classifier(in_dim,out_shape):
        
    #Create Sequential model
    model = load_sequential_model(in_dim)
    
    #Add last layer
    model.add(layers.Dense(out_shape, activation='softmax'))

    #Compile Model
    model = compile_model_classif(model,out_shape)

    return model

def load_sequential_model(in_dim):
    model = models.Sequential()
    # First and Hiden layer
    model.add(layers.Dense(128, activation='relu', input_dim=in_dim))
    model.add(layers.Dense(75, activation='relu'))
    model.add(layers.Dense(30, activation='relu'))
    return model

def compile_model_classif(model, out_shape):
    kappa=tfa.metrics.CohenKappa(num_classes=out_shape)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=[kappa])
    
    return model