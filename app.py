"""
==========================================================================================================================
==========================================================================================================================
==========================================================================================================================
Author: Dawoud Husain
File Name: app.py
Date Created: 2021-06-11
Description: Utalizing SQLAlchemy and Flask, this script handels the chat database and the website routes
==========================================================================================================================
==========================================================================================================================
==========================================================================================================================
"""
from flask.signals import message_flashed
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import pusher

from datetime import datetime
app = Flask(__name__)

# Message database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)


# Message class
class Message(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(50))
  message = db.Column(db.String(500))

# Pusher API
pusher_client = pusher.Pusher(
  app_id='1214203',
  key='afd053e07705f743ec57',
  secret='57f51f9f7f6d3a435b63',
  cluster='us2',
  ssl=True
)


# Defult route
@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages = messages)

# Message route
@app.route('/message', methods=['POST'])
def message():
  try:
      # Get username and message
      username = request.form.get('username')
      message = request.form.get('message')

      # Add message to the database
      new_message = Message(username=username, message=message)
      db.session.add(new_message)
      db.session.commit()

      # Send message
      pusher_client.trigger('chat-channel', 'new-message', {'username': username, 'message': message})
      return jsonify({'result':'sucess'})

  except:
    return jsonify({'result':'failure'}) 


#delete route  
@app.route('/delete')
def delete():
  db.session.query(Message).delete()
  db.session.commit()
  
  messages = Message.query.all()
  return render_template('index.html', messages = messages)


  # element_to_delete = Message.query.get_or_404(id)
  # try:
  #   db.session.delete(element_to_delete)
  #   db.session.commit() 
  #   return jsonify({'delete':'sucess'})

  # except:
  #   return jsonify({'delete':'failure'}) 

# Run applicatoin
if __name__ == '__main__': 
  app.run(debug=True)
