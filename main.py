from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from plyer import filechooser
from kivymd.toast import toast
from kivy.uix.scrollview import ScrollView
from bs4 import BeautifulSoup
from keras.models import load_model
import re
import requests
import tensorflow as tf
import os
from PIL import Image, ImageOps  
import numpy as np


Window.size = (400, 800)
class DribbleUI(MDScreen):
    animation_constant = NumericProperty(40)

    def __init__(self, **kw):
        super().__init__(**kw)
        anim = Animation(animation_constant=10, duration=.6, t='in_out_quad') + Animation(animation_constant=40,
                                                                                          duration=.6, t='in_out_quad')
        anim.repeat = True
        anim.start(self)


class App(MDApp):

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("home.kv"))
        return screen_manager

    def file_chooser(self):
        try:
            filechooser.open_file(on_selection = self.selected)
        except(TypeError):
            toast("Please select a file")
        
    def selected(self, selection):
        global filename
        filename = os.path.basename(selection[0])
        global file_loc
        file_loc = selection[0]
        
    def change_image(self):
        image = file_loc
        screen_manager.get_screen("home").ids['riya'].image = file_loc
        
    def find_tag(self,word):
        url = "http://best-hashtags.com/hashtag/" + word + "/"
        print(url)

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.get_text()

        hashtags = re.findall(r'\#\w+', text)

        # print the hashtags
        return(hashtags[3:7])
        
        
    def find_class(self):
        try:
            model = tf.keras.applications.InceptionV3(include_top=True, weights='imagenet')

            # Load and preprocess the image
            img = Image.open(file_loc)
            img = img.resize((299, 299))
            x = tf.keras.preprocessing.image.img_to_array(img)
            x = tf.keras.applications.inception_v3.preprocess_input(x)
            x = np.expand_dims(x, axis=0)

            # Predict the class of the image
            preds = model.predict(x)
            top_preds = tf.keras.applications.inception_v3.decode_predictions(preds, top=5)[0]

            # Print the top predictions
            tag = []
            for pred in top_preds:
                word = pred[1]
                new_wrd = word.replace("_", "")
                print(new_wrd)
                print(self.find_tag(new_wrd))
                tag.append(self.find_tag(new_wrd))
            print(tag)
            global words
            words = []
            for sublist in tag:
                words.append(' '.join(sublist))
                
            screen_manager.get_screen("home").ids['curency'].text =str(words)
            screen_manager.get_screen("home").ids['happy'].text = "Copy"
            print(words)
        except:
            toast("Please select an image")
            
    def coppy(self):
        words
    
        listToStr = ' '.join([str(elem) for elem in words])
    
        text = ""
        Clipboard.copy(listToStr)
        toast("Copied")
        
        
if __name__ == '__main__':
    App().run()



