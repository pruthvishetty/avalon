import streamlit as st 
import pandas as pd
import random
import time
from twilio.rest import Client
import csv
## User input

st.title("Avalon")
c1, c2 = st.beta_columns([1, 4])
with c1:
	player_names = [st.text_input("Name")]
	for n in range(9):
	    player_names.append(st.text_input(label='Name', key=f'player_names {n}'))
with c2:
	player_contacts = [st.text_input("Phone Number")]
	for n in range(9):
	    player_contacts.append(st.text_input(label='Phone Number', key=f'player_contacts {n}'))

player_names = list(filter(None, player_names))
player_contacts = list(filter(None, player_contacts))
prefix_ph_code = '+1'
player_contacts = [prefix_ph_code + x for x in player_contacts if not str(x) == "nan"]
contacts = dict(zip(player_names, player_contacts))
options = player_names
num_players = len(options)

##

def send_msg(num, msg):
	account_sid = 'ACf884c0e9acf95f10f5a51c79f32fe0e6' 
	auth_token = '0f731632d3bf2b0214d0bf98f6942152' 
	client = Client(account_sid, auth_token) 
	message = client.messages.create(  
							  messaging_service_sid='MG347b801342b448b3d10159442201127f', 
							  body=msg,      
							  to=num)
	return()

def search(myDict, search1):
    team_mates=[]
    for key, value in myDict.items():
        if search1 in value:
            team_mates.append(key)
    return (team_mates)

account_sid = 'ACf884c0e9acf95f10f5a51c79f32fe0e6' 
auth_token = '0f731632d3bf2b0214d0bf98f6942152' 
client = Client(account_sid, auth_token) 

# contact = {'Bhuvin':'+16127566014', 'Nischitha':'+12184091256', 'Samarth':'+16127565977', 'Shriya':'+13413140047','Kirana':'+16128061852', 'Sindhu':'+14806920787', 'Pruthvi':'+16503502683','Vaishnavi':'+16692685700','Nandan':'+14082040425','Madhuri':'+17202458855', 'Aditya':'+17276857200','Anirudh':'+18126069499','Karthik':'+18123608299', 'Shilpa':'+14803291123','Suhas':'+14803291995'}
# contacts = {'Bhuvin':'+16503502683', 'Nischitha':'+16503502683', 'Samarth':'+16503502683', 'Shriya':'+16503502683','Kirana':'+16503502683', 'Sindhu':'+16503502683', 'Pruthvi':'+16503502683','Vaishnavi':'+16692685700','Nandan':'+16503502683','Madhuri':'+16503502683', 'Aditya':'+16503502683','Anirudh':'+18126069499','Karthik':'+16503502683', 'Shilpa':'+16503502683','Suhas':'+16503502683'}

main_good_char = ['Merlin (Team Good)','Percival (Team Good)']
dummy_good_char =['Loyal Servant of Arthur(Team Good)', 'Lady of the Lake (Team Good)','Dummy Good 1 (Team Good)','Dummy Good 2 (Team Good)']

main_evil_char = ['Assassin (Team Evil)','Morgana (Team Evil)','Mordred (Team Evil)']
dummy_evil_char = ['Oberon (Team Evil)','Minion of Mordred (Team Evil)']

playing_char = main_good_char+main_evil_char

players = []
all_chars = []
ph_nos = []
msgs = []
num_good = 0
num_evil = 0
mordred_flag = 0
morgana_flag = 0

# for key in contacts.keys():
# 	players.append(key)

# options = st.multiselect('Who are all playing?',players,[])
num_players = len(options)

def play_game(options, num_players, playing_char, dummy_good_char, dummy_evil_char):
	if (num_players == 5):
		num_good = 3
		num_evil = 2
		all_chars = playing_char+random.sample(dummy_good_char, 1)
		all_chars.remove('Morgana (Team Evil)')

	elif (num_players == 6):
		num_good = 4
		num_evil = 2
		all_chars = playing_char+random.sample(dummy_good_char, 2)
		all_chars.remove('Morgana (Team Evil)')

	elif (num_players == 7):
		num_good = 4
		num_evil = 3
		all_chars = playing_char+random.sample(dummy_good_char, 2)

	elif (num_players == 8):
		num_good = 5
		num_evil = 3
		all_chars =  playing_char+random.sample(dummy_good_char, 3)

	elif (num_players == 9):
		num_good = 6
		num_evil = 3
		all_chars =  playing_char+random.sample(dummy_good_char, 4)

	elif (num_players == 10):
		num_good = 6
		num_evil = 4
		all_chars =  playing_char+random.sample(dummy_good_char, 4)+random.sample(dummy_evil_char, 1)

	random.shuffle(options)
	random.shuffle(all_chars)
	player_assingments = dict(zip(options, all_chars))

	# st.write('Options:', options)
	st.write('Team Good:', num_good)
	st.write('Team Evil:', num_evil)
	# st.write('all_chars:', all_chars)
	st.write('player_assingments:', player_assingments)
	return options, num_good, num_evil, all_chars, player_assingments


if not (num_players < 7):
	mordred_button = st.radio("Mordred", ('Yes','No')) 
	if mordred_button == 'Yes':
		mordred_flag = 1
	else: 
		mordred_flag = 0

	morgana_button = st.radio("Morgana", ('Yes','No')) 

	if morgana_button == 'Yes':
		morgana_flag = 1
	else: 
		morgana_flag = 0

if not (num_players < 5):
	if st.button('Play Avalon!'):
		options, num_good, num_evil, all_chars, player_assingments = play_game(options, num_players, playing_char, dummy_good_char, dummy_evil_char)
		
		# w = csv.writer(open("latest_player_assignment.csv", "w"))
		# for key, val in player_assingments.items():
		# 	w.writerow([key, val])
		
		for i in range(len(options)):
			ph_nos.append(contacts[options[i]])
			msgs.append("Hi, {}, you are {}!".format(options[i], player_assingments[options[i]]))
			# st.write(ph_nos)
			# st.write(msgs)

		if (mordred_flag == 0):
			msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Merlin')[0] in s][0]] = msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Merlin')[0] in s][0]]+' '+'The Evil players are '+str(search(player_assingments, 'Evil'))

		elif (mordred_flag == 1):
			evil_players = search(player_assingments, 'Evil')
			evil_players.remove(search(player_assingments, 'Assassin')[0])
			msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Merlin')[0] in s][0]] = msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Merlin')[0] in s][0]]+' '+'The Evil players are '+str(evil_players)+'. Assassin is unknown!'

		if (morgana_flag == 0):
			msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Percival')[0] in s][0]] = msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Percival')[0] in s][0]]+' '+'Merlin is '+str(search(player_assingments, 'Merlin')[0])+'!'
		elif (morgana_flag == 1):
			percival_list = [search(player_assingments, 'Merlin')[0], search(player_assingments, 'Morgana')[0]]
			random.shuffle(percival_list)
			msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Percival')[0] in s][0]] = msgs[[i for i, s in enumerate(msgs) if search(player_assingments, 'Percival')[0] in s][0]]+' '+'Merlin could be '+str(percival_list[0])+' or '+str(percival_list[1])+'!'
		
		evil_players = search(player_assingments, 'Evil')

		evil_indices = [i for i, x in enumerate(msgs) if 'Team Evil' in x]
		for i in evil_indices:
		    msgs[i] = msgs[i] + ' Evils: '+str(evil_players)

		st.write(msgs)
		# st.write(ph_nos)
		# for i in range(len(ph_nos)):
		# 	send_msg(ph_nos[i], msgs[i])