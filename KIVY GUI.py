
# importing the dependencies
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button 
import time
import os
import glob
import pandas as pd
import numpy as np
from libdw import pyrebase 

url = "https://temperature-981f5.firebaseio.com/"
apikey = "-"

config = {
    "apiKey": apikey,
    "databaseURL": url,
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class Temp_Predict(App):
    
    
    ##########################################################################
    # count = 0                      # we are not using this method of displaying time, instead we will be obtaining
                                     # real time values from firebase to get the more accurate time
    # start = time.time()

    # def Callback_Clock(self, dt):

    #   self.count = self.count+1
    #   self.label2.text = str(self.count)
    ##########################################################################
    def build(self):
        Window.size = (600, 200)
        layout = GridLayout(cols=4)
        # Clock.schedule_interval(self.Callback_Clock, 1)
        
        self.label1 = Label(text = 'Current Time: ', font_size = 24, halign='left', valign='middle')
        self.label2 = Label(text = "", font_size = 24, halign='left', valign='middle')
        self.label3 = Label(text = 'Prediction\nTime: ', font_size = 24, halign='left', valign='middle')
        self.label4 = Label(text = '', font_size = 24, halign='left', valign='middle')
        self.label5 = Label(text = 'Temperature\nReading: ', font_size = 24, halign='left', valign='middle')
        self.label6 = Label(text = '', font_size = 24, halign='left', valign='middle')
        self.label7 = Label(text = 'Predicted\nTemperature: ', font_size = 24, halign='left', valign='middle')
        self.label8 = Label(text = 'Predicting...', font_size = 24, halign='left', valign='middle')

        btn = Button(text="predict", on_press=self.calculate, font_size=24)
        
        # stream_handler to continuously obtain the data of temperature and time after the kivy app is opened without lag
        
        # this is the stream_handler to handle temperature data
        def stream_handler(message):
            actual_temp = message["data"]
            print(actual_temp)
            self.label6.text = str(actual_temp) # obtains the temperature data from firebase in real time
        
        my_stream = db.child("temp_actual").stream(stream_handler)

        self.stream = my_stream
        
        # this is the stream_handler to handle the time data 
        def stream_handler2(message):
            actual_time = message["data"]
            print(actual_time)
            self.label2.text = str(actual_time)
        
        my_stream2 = db.child("time_actual").stream(stream_handler2)

        self.stream2 = my_stream2
        
        # adding of widgets(labels and buttons)
        layout.add_widget(self.label1)
        layout.add_widget(self.label2)
        layout.add_widget(self.label3)
        layout.add_widget(self.label4)
        layout.add_widget(self.label5)
        layout.add_widget(self.label6)
        layout.add_widget(self.label7)
        layout.add_widget(self.label8)
        layout.add_widget(btn)
        return layout
        
    # callback function when the button is pressed to get the prediction
    def calculate(self, instance):
        # this is to get the prediction of the temperature of water from firebase
        self.label8.text = str(db.child("temp").get().val())
        self.label4.text =  str(db.child("time").get().val())
                
    def on_stop(self):
        # this is to stop the streamer on close, to fully close the app.
        self.stream.close()
        self.stream2.close()

# this is to initiate our kivy app which checks if this is the main window and is not imported.
if __name__ == '__main__':
    Temp_Predict().run()