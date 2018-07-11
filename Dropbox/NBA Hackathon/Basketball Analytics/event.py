from game_time import *

class event:
	#a static variable to find a player's team in a game
	#the team ids are additionally included for each event because it makes for clearer code rather than
	#having to repeatedly call and search event.team_lookup outside the class
	team_lookup = {}

	def __init__(self, event_str, event_table, lineup_table):
		self.parse(event_str, event_table)
		self.person_1_team_id = None
		self.person_2_team_id = None
		
		#for each person involved in this event, find the team to which they belong
		if self.person_1 != None:
			if self.person_1 in event.team_lookup[self.game_id]:
				self.person_1_team_id = event.team_lookup[self.game_id][self.person_1]
		
		#take the chance to update player 2's saved team in the table if this is a substitution
		if self.event_msg_type == 'Substitution':
			event.team_lookup[self.game_id][self.person_2] = event.team_lookup[self.game_id][self.person_1]
		
		if self.person_2 != None:
			if self.person_2 in event.team_lookup[self.game_id]:
				self.person_2_team_id = event.team_lookup[self.game_id][self.person_2]
		
	def __lt__(self, other):
		if self.game_time < other.game_time:
			return self
			
	def __str__(self):
		return "Event: {}, Action: {}".format(self.event_msg_type, self.action_type)
	
	
	def parse(self, event_str, event_table):
		#decide to put this in or out of class
		event_data = event_str.split()
		for i in range(len(event_data)):
			if event_data[i] == '':
				event_data[i] = None
		
		self.game_id = event_data[0]
		event_num = event_data[1]
		#get the event description (e.g. shot, dunk) from the look-up table
		#if the codes are not found in the look-up table, skip the descriptions
		try:
			event_description = event_table[int(event_data[2])][int(event_data[6])]
			self.event_msg_type = event_description['event']
			self.action_type = event_description['action']
		except KeyError:
			self.event_msg_type = None
			self.action_type = None
		
		period = event_data[3]
		wc_time = event_data[4]
		pc_time = event_data[5]
		self.game_time = game_time(period, pc_time, wc_time, event_num)
		
		self.option_1 = event_data[7]
		self.option_2 = event_data[8]
		self.option_3 = event_data[9]
		self.team_id = event_data[10]
		self.person_1 = event_data[11]
		self.person_2 = event_data[12]
		self.team_id_type = event_data[13]