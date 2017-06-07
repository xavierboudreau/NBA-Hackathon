import numpy as np
import pprint
from operator import attrgetter
import parse_text
import datetime
import pickle


## Poisson home and away simulation
# given: total home and total away goals
# how many games are played in a season? 20*19 = 380

def poisson_simulation(home_goals, away_goals, num_teams):
	if num_teams == 0:
		return "No Teams"
	games_played = num_teams*(num_teams-1)
	home_goals_pg = float(home_goals)/games_played
	away_goals_pg = float(away_goals)/games_played
	teams = []
	for i in range(num_teams):
		teams.append(SimTeam(0,0,0))

	for i in range(num_teams):
		for j in range(num_teams):
			if i != j:
				home_score = np.random.poisson(home_goals_pg)
				away_score = np.random.poisson(away_goals_pg)
				teams[i].goals_for += home_score
				teams[j].goals_for += away_score
				teams[i].goals_against += away_score
				teams[j].goals_against += home_score
				if home_score > away_score:
					teams[i].points += 3
				elif home_score < away_score:
					teams[j].points += 3
				else:
					teams[i].points += 1
					teams[j].points += 1
	teams = sorted(teams, key = attrgetter('goals_for'))
	teams = sorted(teams, key = lambda team: team.goals_for - team.goals_against)
	teams = sorted(teams, key = attrgetter('points'))
	teams.reverse()
	legend = "Pts\tGF\tGA"
	#print(legend)
	#pp = pprint.PrettyPrinter(indent = 4)
	#pp.pprint(teams)
	return teams

def batch_run(year, league, num_sim, print_data = False):
	start = datetime.datetime.now()
	leagueDict = parse_text.Data[year][league]
	leagueSize = len(leagueDict.keys())-2 # 2 for home goals key and away goals key
	teams = [SimTeam(0,0,0) for i in range(leagueSize)]
	for i in range(num_sim):
		sim = poisson_simulation(leagueDict["home goals"], leagueDict["away goals"], leagueSize)
		if sim == "No Teams":
			return sim
		teams = [teams[j]+sim[j] for j in range(leagueSize)]
	teams = [team.divide(num_sim) for team in teams]
	if print_data:
		pp = pprint.PrettyPrinter(indent = 4)
		print("\nSimulation for year {0}, league #{1}, num_sim = {2}".format(year, league, num_sim))
		legend = "    Pts\t\tGF\tGA"
		print(legend)
		pp.pprint(teams)
		time = datetime.datetime.now().microsecond - start.microsecond
		time /= 1000000.
		print("\ntime to complete: {0} seconds".format(time))
	return teams

def sim_all(num_sim):
	start = datetime.datetime.now()
	print("Simulating...")
	SimData = {}
	Data = parse_text.Data
	for year in Data:
		#print("YEAR : ", end = "")
		#print(year)
		SimData[year] = {}
		for league in Data[year]:
			#print("\tLEAGUE : ", end = "")
			#print(league)
			simmed = batch_run(year, league, num_sim)
			if simmed == "No Teams":
				continue
			SimData[year][league] = batch_run(year, league, num_sim)
	print("Done Simulating.")
	time = datetime.datetime.now().second - start.second
	print("Total time: {0}".format(time))
	with open("sim_data.pkl", 'wb') as picklefile:
		pickle.dump(SimData, picklefile)
	return SimData

def try_pickle():
	with open("sim_data.pkl", 'rb') as picklefile:
		SimData = pickle.load(picklefile)
	print(SimData.keys())
	print(SimData["2010-11"][2][1])
	return


class SimTeam:
	def __init__(self, points, goals_for, goals_against):
		self.points = points
		self.goals_for = goals_for
		self.goals_against = goals_against

	def __str__(self):
		return "{0}\t{1}\t{2}".format(self.points, self.goals_for, self.goals_against)

	def __repr__(self):
		return self.__str__()

	def __add__(self, other):
		return SimTeam(self.points+other.points, self.goals_for+other.goals_for, self.goals_against+other.goals_against)

	def divide(self, f):
		f = float(f)
		return SimTeam(self.points/f, self.goals_for/f, self.goals_against/f)



#poisson_simulation(800,600,20)
#batch_run("2010-11", 2, 1000)
#sim_all(1000)
#try_pickle()

# decide: do we use the home and away goal tallies for each year, or use the averages for the league overall? The game changes over time, y'know?
# Does it really though? Would be good to see a graph of home, away, and total goals per game. for the prem










