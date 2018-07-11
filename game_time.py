class game_time:
	def __init__(self, period, pc_time, wc_time, event_num):
		self.period = int(period)
		self.pc_time = int(pc_time)
		self. wc_time = int(wc_time)
		self.event_num = int(event_num)
	def __lt__(self, other):
		'''
		Compares self to other using the following sequence of sorted columns: 
		
		Period (ascending), PC_Time (descending), WC_Time (ascending), Event_Number (ascending)
		'''
		if self.period < other.period:
			return True
			
		elif self.period == other.period:
			if self.pc_time > other.pc_time:
				return True
				
			elif self.pc_time == other.pc_time:
			
				if self.wc_time < other.pc_time:
					return True
					
				elif self.wc_time == other.pc_time:
					if self.event_num < other.event_num:
						return True
					else:
						return False
					
				else:
					return False
			else:
				return False
		else:
			return False