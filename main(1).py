import os
import telebot
import random
import joblib
import requests
import matplotlib.pyplot as plt
import cv2
import numpy as np
from transform_image import transform_single_image


API_KEY = "1907978377:AAGmOeo7-uGjTGU2AEx9A59QHptTNNrD2Ts"
bot = telebot.TeleBot(API_KEY)

loaded_model = joblib.load('enhanced_model.sav')

dic = {0:'scissors', 1:'rock', 2:'paper'}


possible_actions = ["rock", "paper", "scissors"]
computer_action = random.choice(possible_actions)

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, ''' Select from the following
  - rock
  - paper
  - scissors ''')

@bot.message_handler(content_types=['photo','document'])
def image_sent(message):
  #bot.send_message(message.chat.id, bot.get_file_url(message.document.file_id))
  #print(message.photo)
  file_id = message.photo[-1].file_id
  file_info = bot.get_file(file_id)
  file_downloaded = bot.download_file(file_info.file_path)

  # response = requests.get(bot.get_file_url(message.document.file_id))
  file = open("sample_image.jpeg", "wb")
  file.write(file_downloaded)
  file.close()
  image_path = "sample_image.jpeg"
  image = transform_single_image(image_path)
  #print(image)
  cv2.imwrite('Test_gray.jpg', image)
 
  img = cv2.imread('Test_gray.jpg')
  img_resized = np.array(img,dtype = 'int')
  img_resized = img_resized.flatten()
  img_resized = img_resized.reshape(1, -1)
  user_action = dic[loaded_model.predict(img_resized)[0]]

  computer_action = random.choice(possible_actions)
  if user_action == computer_action:
    bot.send_message(message.chat.id, "The bot also playeded " + user_action + "\n It's a tie!")
    computer_action = random.choice(possible_actions)
  elif user_action == "rock":
      if computer_action == "scissors":
        bot.send_message(message.chat.id, "The bot playeded " + computer_action + "\n you played "+ user_action + "\n Rock smashes scissors! \n You win!")
        computer_action = random.choice(possible_actions)
      else:
         bot.send_message(message.chat.id,"The bot played " + computer_action + "\n you played "+ user_action + "\n Paper covers rock! \n You lose.")
         computer_action = random.choice(possible_actions)
  elif user_action == "paper":
      if computer_action == "rock":
        bot.send_message(message.chat.id,"The bot played " + computer_action + "\n you played "+ user_action +  " \n Paper covers rock! \n You win!")
        computer_action = random.choice(possible_actions)
      else:
        bot.send_message(message.chat.id, "The bot played " + computer_action + "\n you played "+ user_action + "\n Scissors cuts paper! \n You lose.")
        computer_action = random.choice(possible_actions)
  elif user_action == "scissors":
      if computer_action == "paper":
        bot.send_message(message.chat.id,"The bot played " + computer_action + "\n you played "+ user_action + "\n Scissors cuts paper! \n You win!")
        computer_action = random.choice(possible_actions)
      else:
        bot.send_message(message.chat.id,"The bot played " + computer_action + "\n you played "+ user_action + "\n Rock smashes scissors! \n You lose.")
        computer_action = random.choice(possible_actions)

bot.polling()
