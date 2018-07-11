import queue

def commit_substitutions(players_on_court, substitution_queue):
	while not substitution_queue.empty():
		sub = substitution_queue.get()
		players_on_court[sub.team_id].discard(sub.outgoing_player)
		players_on_court[sub.team_id].add(sub.incoming_player)

class substitution:
	def __init__(self, outgoing_player, incoming_player, team_id):
		self.outgoing_player = outgoing_player
		self.incoming_player = incoming_player
		self.team_id = team_id