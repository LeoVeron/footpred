import glob
import os
from os import path
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

from footpred.data_prep import create_Y, create_X
from footpred.model import get_model_classifier
from footpred.plot import plot_confusion_matrix




class Trainer():

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", 'unnamed')
        self.data_folder = kwargs.get("data_folder", path.join('data', 'csv') )
        self.epochs = kwargs.get("epochs", 10)

    def open_csv(self):
        all_files = glob.glob(path.join(self.data_folder, "*.csv"))
        li = []
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)
        print(f'{len(li)} csv founds')
        self.df = pd.concat(li, axis=0, ignore_index=True)
        print(f'{len(self.df)} matchs founds')


    def data_prep(self):
        self.X_train, self.X_test, self.y_train, self.y_test = \
           train_test_split(create_X(self.df), create_Y(self.df), test_size=0.2)


    def create_model(self):
        in_dim = self.X_train.shape[1]
        out_shape = len(self.y_train.columns)
        self.model = get_model_classifier(in_dim,out_shape)
                
    def evaluate_model(self):

        # Use history to fetch validation score on last epoch
        self.score_name =list(self.history.history.keys())[1]
        self.val_score_name =list(self.history.history.keys())[-1]
        self.score = round(self.history.history[self.val_score_name][-1]*100,2)
        
        print(f'{self.score_name} = {self.score}')

    def create_result_folder(self):
        
        self.resdir = path.join("data", "results", self.name + str(int(time.time())))
        if not path.exists(self.resdir):
            os.mkdir(self.resdir)
    
    def save_fig(self):
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        ax1.plot(self.history.history['loss'], label='train')
        ax1.plot(self.history.history['val_loss'], label='val')
        # ax1.set_ylim(0., 2.2)
        ax1.set_title('loss')
        ax1.legend()

        ax2.plot(self.history.history[self.score_name], label=f'train {self.score_name}' )
        ax2.plot(self.history.history[self.val_score_name], label=f'val {self.score_name}' )
        # ax2.set_ylim(0.25, 1.)
        ax2.set_title(self.score_name)
        ax2.legend()

        fig_path = path.join(self.resdir, self.name + '_loss_score_plot.png')
        print(f'Saving loss/acc curves at {fig_path}')
        f.savefig(fig_path)

    
    def save_confusion_matrix(self):
        y_pred = self.model.predict(self.X_test)

        argmax_pred = np.argmax(y_pred, axis=1)
        argmax_test = np.array(self.y_test.apply(lambda x : np.argmax(x), axis = 1))
        classe = list(self.y_test.columns)
        
        f = plot_confusion_matrix(argmax_test, argmax_pred, classes=classe)
        
        fig_path = path.join(self.resdir, self.name + '_confusion.png')
        print(f'Saving confusion at {fig_path}')
        f.savefig(fig_path)

    def fit_model(self):
        
        es = EarlyStopping(patience=5, restore_best_weights=True)
        
        self.history = self.model.fit(self.X_train, self.y_train,
                                validation_data=(self.X_test, self.y_test),
                                epochs=self.epochs,
                                batch_size=16, 
                                verbose=1,
                                callbacks=[es])

    def savemodel(self):
        
        model_path = path.join(self.resdir, f'model_{self.name}.h5')
        self.model.save(model_path)
        print(f'model saved at {model_path}')

            
    def train(self):
        # step 1 : get data
        self.open_csv()
        self.data_prep()
        
        # step 2 : create model
        self.create_model()

        # step 3 : train
        self.fit_model()

        # step 4 : evaluate perf
        self.evaluate_model()
        
        # step 5 : save training loss score
        self.create_result_folder()
        self.save_fig()
        self.save_confusion_matrix()
        
        # step 6 : save the trained model
        self.savemodel()


if __name__ == '__main__':
    params = {"name" : "first_model",
              "data_folder" : path.join('data', 'csv'),
              "epochs" : 30,}
    
    trainer = Trainer(**params)
    trainer.train()
    print('Finito cappuccino!')