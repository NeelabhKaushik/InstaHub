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
import joblib


Window.size = (600, 800)
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
        screen_manager.add_widget(Builder.load_file("reach.kv"))
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
            listToStr = ' '.join([str(elem) for elem in words])
            
            screen_manager.get_screen("home").ids['curency'].text =str(listToStr)
            screen_manager.get_screen("home").ids['happy'].text = "Copy"
            print(words)
        except:
            toast("Please select an image")
            
            
            
    def find_tag(self,word):
        url = "http://best-hashtags.com/hashtag/" + word + "/"
        print(url)

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.get_text()

        hashtags = re.findall(r'\#\w+', text)

        # print the hashtags
        return(hashtags[3:7])
        
    
            
    def coppy(self):
        words
    
        listToStr = ' '.join([str(elem) for elem in words])
    
        text = ""
        Clipboard.copy(listToStr)
        toast("Copied")
        
        
    # Likes = ""
    # Saves = ""
    # Comments = ""
    # Shares = ""
    # Visits = ""
    # Followers = ""
    def predict_instagram_reach(blah):
    # Take input for each feature one by one
        try:
            likes = float(screen_manager.get_screen("reach").ids["Likes"].text)
            saves = float(screen_manager.get_screen("reach").ids["Saves"].text)
            comments = float(screen_manager.get_screen("reach").ids["Comments"].text)
            shares = float(screen_manager.get_screen("reach").ids["Shares"].text)
            profile_visits = float(screen_manager.get_screen("reach").ids["Visits"].text)
            follows = float(screen_manager.get_screen("reach").ids["Followers"].text)

            # Use the model to predict reach
            features = np.array([[likes, saves, comments, shares, profile_visits, follows]])
            model = joblib.load('instagram_reach_model.joblib')
            predicted_reach = model.predict(features)
            if(likes < 0):
                screen_manager.get_screen("reach").ids["happyhappy"].text = "Please enter valid number of likes"
                return
            if(saves < 0):
                screen_manager.get_screen("reach").ids["happyhappy"].text = "Please enter valid number of saves"
                return
            if(comments < 0):
                screen_manager.get_screen("reach").ids["happyhappy"].text = "Please enter valid number of comments"
                return
            if(shares < 0):
                screen_manager.get_screen("reach").ids["happyhappy"].text = "Please enter valid number of shares"
                return
            if(profile_visits < 0):
                screen_manager.get_screen("reach").ids["happyhappy"].text = "Please enter valid number of profile visits"
                return
            if(follows < 0):
                screen_manager.get_screen("reach").ids["happyhappy"].text = "Please enter valid number of followers"
                return 
            screen_manager.get_screen("reach").ids["happyhappy"].text =  ("Predicted Reach: " + str(round(predicted_reach[0]/1000)) + "\n" + "Which will result in nearly " + str(round(predicted_reach[0]/1000) * 41/1000) + " new followers")
            
            print("Predicted Reach:", predicted_reach[0], "\n", "Which will result in nearly", round(predicted_reach[0]/1000)* 41/100, "new followers")
        except:
            toast("Please fill out all feilds")
        
if __name__ == '__main__':
    App().run()



#eturing type of iamge
global preds
def kartik_peddu(img):
    #loading model
    model = tf.keras.applications.InceptionV3(include_top=True, weights='imagenet')

    #resiging image
    img = img.resize((299, 299))
    #preprocessing
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.inception_v3.preprocess_input(x)
    x = np.expand_dims(x, axis=0)
    # Predict the class of the image
    
    preds = model.predict(x)
    #top_pred will give 1 top prediction
    top_preds = tf.keras.applications.inception_v3.decode_predictions(preds, top=1)[0]
    return top_preds

#getiing dominant color
def get_dominant_colors(preds, num_clusters=5):
    img_features = preds.flatten()
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(img_features)
    colors = kmeans.cluster_centers_
    return colors
