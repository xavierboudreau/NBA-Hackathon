import pickle
import csv
from parse_text import Data
from epl_table_simulation import SimTeam
from math import sqrt
import numpy as np

with open('sim_data.pkl', 'rb') as simfile:
	Sim_Data = pickle.load(simfile)

def calc_our_metric(sim_league, act_league):
	x = 0
	for i in range(len(sim_league)):
		x += (sim_league[i].points - act_league[i+1]['points'])**2
	return sqrt(x/len(sim_league))

def fill_data():
	Var_Data = {}
	for year in Data:
		Var_Data[year] = year_dict = {}
		for league in Data[year]:
			sim_league = Sim_Data[year][league]
			act_league = Data[year][league]
			league_dict = {}
			league_dict['our metric'] = calc_our_metric(sim_league, act_league)
			league_dict['sim table SD'] = np.std([team.points for team in Sim_Data[year][league]])
			act_table = Data[year][league]
			league_dict['act table SD'] = np.std([act_table[pos]['points'] for pos in act_table if pos not in ['away goals', 'home goals']])
			year_dict[league] = league_dict
	return Var_Data

#export the results to a simple text file for a quick look-over
#need to sort by year for this to be useful
def send_to_text(filename = "simpleTextOutput"):
	f = open(filename,"w")
	Var_Data = fill_data()
	years = sorted(Var_Data.keys())
	for year in years:
		f.write("\n\n\nyear: {}".format(year))
		for league in Var_Data[year]:
			f.write("\n\n\tleague: {}".format(league))
			f.write("\n\t\tOur metric: {}".format(Var_Data[year][league]["our metric"]))
			f.write("\n\t\tSim table SD: {} ".format(Var_Data[year][league]["sim table SD"]))
			f.write("\n\t\tAct table SD: {}".format(Var_Data[year][league]["act table SD"]))

#export the results in a .csv for graph analysis
def send_to_csv():
	Var_Data = fill_data()
	with open("test.csv","excel") as csvfile:
		#go through each year in Var_data
		#go through each league in each year
		#
		print("Done")
		

#send_to_text()
