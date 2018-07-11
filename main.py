import queue
from game_time import *
from substitution import *
from event import *

def load_event_table(event_codes_filepath, event_table):
	'''
	Constructs event code look-up table in following form:
	{event_code: {action_code: {'event_string': 'made shot', 'action_string': 'dunk'}, ...}, ...}
	
	Parameters:
	event_codes_filepath: filepath to text file that stores event and action code descriptions
	event_table: dictionary to serve as look-up table
	'''
	event_codes_file = open(event_codes_filepath, 'r')
	end_of_file = False
	first_line = True
	while not end_of_file:
		line = event_codes_file.readline()
		if line == '':
			end_of_file = True
			continue
		if first_line:
			first_line = False
			continue
		
		line_data = line.split('\"')
		codes = line_data[0].split()
		event_code = int(codes[0])
		action_code = int(codes[1])
		
		event_description = line_data[1].strip()
		try:
			action_description = line_data[3].strip()
		except IndexError:
			action_description = ''
		
		if event_code not in event_table:
			event_table[event_code] = {}

		event_table[event_code][action_code] = {'event': event_description, 'action': action_description}

def load_lineup_table(game_lineup_filepath, lineup_table):
	lineup_file = open(game_lineup_filepath, 'r')
	end_of_file = False
	first_line = True
	while not end_of_file:
		line = lineup_file.readline()
		if line == '':
			end_of_file = True
			continue
		if first_line:
			first_line = False
			continue
		line_data = line.split()
		game_id = line_data[0]
		period = int(line_data[1])
		person_id = line_data[2]
		team_id = line_data[3]
		status = line_data[4]
		
		if game_id not in lineup_table:
			lineup_table[game_id] = {}
		if period not in lineup_table[game_id]:
			lineup_table[game_id][period] = {}
		
		lineup_table[game_id][period][person_id] = {'team_id': team_id, 'status': status}

def load_game_events(play_by_play_filepath, event_table, lineup_table, game_events):
	'''
	Returns:
	{game_id: [event1, event2, ...], ...}
	where the arrays of events are sorted by occurence (earliest first)
	'''
	play_file = open(play_by_play_filepath, 'r')
	end_of_file = False
	first_line = True
	while not end_of_file:
		line = play_file.readline()
		if line == '':
			end_of_file = True
			continue
		if first_line:
			first_line = False
			continue
		this_event = event(line, event_table, lineup_table)
		game_id = this_event.game_id
		if game_id not in game_events:
			game_events[game_id] = []
		game_events[game_id].append(this_event)
	
	for game_id in game_events.keys():
		game_events[game_id].sort()
		
def start_team_lookup(lineup_table):
	team_lookup = {}
	for game_id in lineup_table:
		for period in lineup_table[game_id]:
			for person_id in lineup_table[game_id][period]:
				if game_id not in team_lookup:
					team_lookup[game_id] = {}
				team_lookup[game_id][person_id] = lineup_table[game_id][period][person_id]['team_id']
	return team_lookup


def adjust_score_differentials(players_on_court, scoring_team, player_differentials, score_value):
	for team in players_on_court:
		for player in players_on_court[team]:
			if player not in player_differentials:
				player_differentials[player] = 0
				print('UHHHHH OHHHHHH')
			if team == scoring_team:
				player_differentials[player] += score_value
			else:
				player_differentials[player] -= score_value

def get_period_starters(game_id, period, lineup_table):
	'''
	Returns
	{team_id_1: {player1, player2, ..., player5}, team_id_2: {...}}
	'''
	starting_players = lineup_table[game_id][period].keys()
	starting_lineups = {}
	for player in starting_players:
		players_team = lineup_table[game_id][period][player]['team_id']
		if players_team not in starting_lineups:
			starting_lineups[players_team] = set()
		starting_lineups[players_team].add(player)
	return starting_lineups
	
if __name__ == '__main__':
	event_codes_path = 'NBA Hackathon - Event Codes.txt'
	game_lineup_path = 'NBA Hackathon - Game Lineup Data Sample (50 Games).txt'
	play_by_play_path = 'NBA Hackathon - Play by Play Data Sample (50 Games).txt'
	
	event_table = {}
	load_event_table(event_codes_path, event_table)
	
	lineup_table = {}
	load_lineup_table(game_lineup_path, lineup_table)
	
	#load the starting lineups into a table that contains player's team_id
	event.team_lookup = start_team_lookup(lineup_table)
	
	game_events = {}
	load_game_events(play_by_play_path, event_table, lineup_table, game_events)
	
	with open('results.csv', 'w+') as out_file:
				out_file.write('Game ID,Player ID,+/-\n')
				out_file.close()
	
	for game in game_events:
		#keep track of the players on the court to correctly edit plus/minus 
		players_on_court = {}
		
		substitution_queue = queue.Queue()
		# {player1: +/-, player2: +/-, ...}
		player_differentials = {}
		period = 0
		
		for event in game_events[game]:
			if event.event_msg_type == 'Start Period':
				period += 1
				players_on_court = get_period_starters(game, period, lineup_table)
				
				for team in players_on_court:
					for player in players_on_court[team]:
						if player not in player_differentials:
							player_differentials[player] = 0
				
			if event.event_msg_type == 'Substitution':
				#person 1 in event leaves the game while person 2 comes on
				event.person_2_team_id = event.person_1_team_id
				sub = substitution(event.person_1, event.person_2, event.person_1_team_id)
				if sub.incoming_player not in player_differentials:
					player_differentials[sub.incoming_player] = 0
				substitution_queue.put(sub)
				
			if event.event_msg_type == 'Foul':
				commit_substitutions(players_on_court, substitution_queue)
				
			if event.event_msg_type == 'Free Throw':
				#the free throw was made if and only if option_1 is 1
				if event.option_1 == '1':
					adjust_score_differentials(players_on_court, event.person_1_team_id, player_differentials, 1)	
				
			if event.event_msg_type == 'Made Shot':
				#commit the substitutions before evaluating the new score differentials
				commit_substitutions(players_on_court, substitution_queue)
				
				#option_1 is the point value of the shot
				adjust_score_differentials(players_on_court, event.person_1_team_id, player_differentials, int(event.option_1))
		
		for player in player_differentials:
			with open('results.csv', 'a') as out_file:
				out_file.write('{},{},{}\n'.format(game, player, player_differentials[player]))
				out_file.close()