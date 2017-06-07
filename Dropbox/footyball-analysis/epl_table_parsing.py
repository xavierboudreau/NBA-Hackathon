

"""
Pld comes at col 35
(Separated by ~~~)
Title of csv file two lines below ~~~
e.g.
### Standings


~~~
                                        - Home -          - Away -            - Total -
                                 Pld   W  D  L   F:A     W  D  L   F:A      F:A   +/-  Pts
 1. Man United                    38  15  2  2  49:12    9  6  4  30:19    79:31  +48   80
 2. Arsenal                       38  15  3  1  45:13    5  7  7  18:25    63:38  +25   70
 3. Liverpool                     38  13  4  2  40:14    7  5  7  31:25    71:39  +32   69
 4. Leeds                         38  11  3  5  36:21    9  5  5  28:22    64:43  +21   68
 5. Ipswich                       38  11  5  3  31:15    9  1  9  26:27    57:42  +15   66
 6. Chelsea                       38  13  3  3  44:20    4  7  8  24:25    68:45  +23   61
 7. Sunderland                    38   9  7  3  24:16    6  5  8  22:25    46:41   +5   57
 8. Aston Villa                   38   8  8  3  27:20    5  7  7  19:23    46:43   +3   54
 9. Charlton                      38  11  5  3  31:19    3  5 11  19:38    50:57   -7   52
10. Southampton                   38  11  2  6  27:22    3  8  8  13:26    40:48   -8   52
11. Newcastle                     38  10  4  5  26:17    4  5 10  18:33    44:50   -6   51
12. Tottenham                     38  11  6  2  31:16    2  4 13  16:38    47:54   -7   49
13. Leicester                     38  10  4  5  28:23    4  2 13  11:28    39:51  -12   48
14. Middlesbrough                 38   4  7  8  18:23    5  8  6  26:21    44:44        42
15. West Ham                      38   6  6  7  24:20    4  6  9  21:30    45:50   -5   42
16. Everton                       38   6  8  5  29:27    5  1 13  16:32    45:59  -14   42
17. Derby                         38   8  7  4  23:24    2  5 12  14:35    37:59  -22   42
18. Man City                      38   4  3 12  20:31    4  7  8  21:34    41:65  -24   34
19. Coventry                      38   4  7  8  14:23    4  3 12  22:40    36:63  -27   34
20. Bradford                      38   4  7  8  20:29    1  4 14  10:41    30:70  -40   26
~~~

(Source: `1-premierleague.csv`)
"""

class Team:
	def __init__(self, name, league, position, wins, draws, losses, goals_for, goals_against, goal_difference, points,
		home_goals_for, home_goals_against, away_goals_for, away_goals_against):
		self.name = name
		self.league = league
		self.position = position
		self.wins = wins
		self.draws = draws
		self.losses = losses
		self.goals_for = goals_for
		self.goals_against = goals_against
		self.goal_difference = goal_difference
		self.points = points
		self.home_goals_for = home_goals_for
		self.home_goals_against = home_goals_against
		self.away_goals_for = away_goals_for
		self.away_goals_against = away_goals_against













