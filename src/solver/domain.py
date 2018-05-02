import copy

class Action:
	def __init__(self,action):
		self.action_name = ''
		self.preconditions=[]
		self.effects = []
		self.delete_effects=[]#Delete litst effects e.g. not on location A
		self.parameters = []
		self.num_parameters = 0

		elements = get_elements(action)

		for element in elements:
			element =  "".join(element)

			if element[0]!=':':
				self.set_name_and_parameters(element)
			elif element[0:13] == ':precondition':
				#print "".join(element)
				self.set_preconditions(element)

			elif element[0:7]==':effect':
				self.sef_effects(element)
			else:
					raise ValueError('Error in: ',element,"Did not recognize action property")

	def set_name_and_parameters(self,name_and_params):
		#print name_and_params
		letters = []
		for letter in name_and_params:

			if letter ==':':
				self.name="".join(letters)
				letters = []
			if letter=='?':
				if letters[0]=='?':
					self.parameters.append(join(letters[1:]))
				letters=[]

			letters.append(letter)
		self.parameters.append(join(letters[1:-1]))
		self.num_parameters = len(self.parameters)




		letters = "".join(letters)
		if letters[0:11] ==':parameters':
			#remove ':parameters' and parantheses
			letters = letters[12:-1]
			temp_list = [] #Best name
			for letter in letters:
				if letter=='?':
					a=1

	def set_preconditions(self,preconditions):
		element = preconditions[14:-1]
		#print element

		#ignore 'and' statement since strips only allows conjunctions
		if element[0:3]=='and':
			element=element[3:]

		#print element

		if element[0]=='(':
			preconditions = get_elements(element)
			#print preconditions
			for precondition in preconditions:
				precondition =  "".join(precondition)[1:-1]
				if precondition[0:3]=='not':
					raise ValueError('Error in action: ',self.name,precondition,"No negative preconditions")
				self.preconditions.append(Predicate(precondition))
		else:
			self.preconditions.append(Predicate(element))

	def sef_effects(self,effects):
		#Example input: :effect(and(pointing?s?d_new)(not(pointing?s?d_prev)))

		#Remove ':effect()'
		effects = effects[7:]

		#If there is an 'and', remove it. Because STRIPS

		if effects[0:4]=='(and':
			effects=effects[4:-1]

		effects = get_elements(effects)

		for effect in effects:
			effect = join(effect[1:-1])
			if effect[0:4]=='not(':
				effect=effect[4:-1]
				self.delete_effects.append(Predicate(effect))
			else:
				self.effects.append(Predicate(effect))

	def get_addlist(self,parameters):
		list_of_effects = []

		for effect in self.effects:

			if effect.parameters:
				list_of_effects.append(effect.name+" "+" ".join(self.select_parameters(effect,parameters)))
			else:
				#If the effect has no parameters e.g. (hand-empty)
				list_of_effects.append(effect.name)
		return list_of_effects

	def get_deletelist(self,parameters):
		list_of_delete_effects = []
		#parameters_mapped = dict(zip(self.parameters,parameters))
		for delete_effect in self.delete_effects:
			# print effect.name+" "+" ".join(parameters)
			if delete_effect.parameters:
				list_of_delete_effects.append(delete_effect.name+" "+" ".join(self.select_parameters(delete_effect,parameters)))
			else:
				list_of_delete_effects.append(delete_effect.name)
		return list_of_delete_effects

	def select_parameters(self,precondition,parameters):

		if self.parameters == precondition.parameters:
			return parameters
		elif not parameters:
			return parameters
		else:
			parameters_mapped = dict(zip(self.parameters,parameters))
			lst = []

			for param in precondition.parameters:
				lst.append(parameters_mapped[param])
			return lst

	def return_possible(self,states):
		'''
		Returns the possible combinatoins of input objects that satisfy the
		state and this actions preconditions
		'''

		precondition_matches = dict()
		for precondition in self.preconditions:
			for state in states:
				state = state.split()
				if precondition.name == state[0]:
					if precondition.name+ " " + " ".join(precondition.parameters) in precondition_matches:
						if state not in precondition_matches[precondition.name+ " " + " ".join(precondition.parameters)]:
							precondition_matches[precondition.name + " " + " ".join(precondition.parameters)].append(state)
					else:
							precondition_matches[precondition.name+ " " + " ".join(precondition.parameters)] = [state]


		combinations = []
		if len(precondition_matches)==len(self.preconditions):
			self.recursive_get_combo(combinations,precondition_matches,{})

		possible_parameters = []
		for combination in combinations:
			temp = []
			for parameter in self.parameters:
				temp.append(combination[parameter])
			possible_parameters.append(temp)
		return possible_parameters

	def recursive_get_combo(self,combinations,precondition_matches,temp_combinations):
		'''
		get possible combinations of objects based on predonditions and states
		'''

		if precondition_matches:# and len(temp_combinations) < self.num_parameters:
			first_key = precondition_matches.keys()[0]
			first_key_split = first_key.split()

			if len(first_key_split)>1:

				for state in precondition_matches[first_key]:
					go = False
					i = 1
					temp_combinations_copy = temp_combinations.copy()
					for obj in state[1:]:
						# go = False
						if not first_key_split[i] in temp_combinations_copy:
							temp_combinations_copy[first_key_split[i]] = obj
							go = True
						elif obj == temp_combinations_copy[first_key_split[i]]:
							go = True
						else:
							go = False
							break

						i = i + 1
					#print temp_combinations_copy not in combinations
					# if temp_combinations_copy in combinations:
					# 	return
					if go:
						self.recursive_get_combo(combinations,removekey(precondition_matches,first_key),temp_combinations_copy)

			else:
				temp_combinations_copy = copy.copy(temp_combinations)
				self.recursive_get_combo(combinations,removekey(precondition_matches,first_key),temp_combinations_copy)


		else:
			if len(temp_combinations) == self.num_parameters and temp_combinations not in combinations:
				combinations.append(temp_combinations)

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

class Predicate:
	def __init__(self,predicate):
		# print "".join(predicate)
		self.parameters=[]
		self.name=''

		letters = []
		named = False
		have_parameters = False

		for letter in predicate:

			if letter=='?':
				have_parameters = True
				if not named:
					self.name = (join(letters)).upper()
					named = True

				else:
					self.parameters.append(join(letters[1:]))
				letters=[]

			letters.append(letter)

		if have_parameters:
			self.parameters.append(join(letters[1:]))

		if not named:
			self.name = join(predicate).upper()

class Domain:
	domain_name = ''
	requirements = []
	predicates = []
	actions = []
	def __init__(self,domain_file):
		self.parse(domain_file)
		domain_file.close()

	def parse(self,file):
		current_element = ''
		i = 0
		#Number of parantheses pointing left or right
		num_par_left = 0
		num_par_right = 0

		#nprl is one because the first parenthese shall be accounted for
		num_par_right_last = 1
		num_par_left_last = 0

		#Number of elements in the domain file. Actions, predicates, requirecements
		num_elements = 0

		lines = []
		element = []
		for line in file:
			lines.append(line)

			i = i + 1
			#Remove whitespace
			line = line.replace(' ','')
			line = line.replace('	','')
			line = line.strip()


			if line:
				#if comment line
				if line[0]==";":
					continue

				for symbol in line:
					element.append(symbol)
					if symbol=='(':
						num_par_right += 1

					elif symbol ==')':
						num_par_left +=1


					#If the number of parantheses has changed
					if not (num_par_right_last == num_par_right) or not (num_par_left_last== num_par_left):

						if num_par_right-num_par_left==1:
							num_elements+=1
							self.set_element(element)
							element = []
							#print 'new',i,line

					num_par_left_last = num_par_left
					num_par_right_last = num_par_right



		#If the sum of left and right parantheses is not zero raise exepction
		if (num_par_right-num_par_left):
			raise ValueError('Error. Inconsistent number of left and right parantheses in domain file')

	def set_element(self,element):
		element = "".join(element)
		element = element.lower()

		if element[1:7]=='define':
			self.domain_name = element[14:-1]

		elif element[1:14]==':requirements':
			self.requirements = element[15:21]
			if self.requirements!='strips':
				raise ValueError('Error in: ',element,"Wrong requirements, must be strips")

		elif element[1:12]==':predicates':
			self.set_predicates(element[12:-1])

		elif element[1:8]==':action':
			self.actions.append(Action(element[8:-1]))
		else:
			raise ValueError('Error in: ',element,'Can not recognice this property.')

	def set_predicates(self,element):
		predicates = get_elements(element)
		for predicate in predicates:
			self.predicates.append(Predicate(predicate[1:-1]))

def get_elements(line):

	num_par_left = 0
	num_par_right = 0

	#nprl is one because the first parenthese shall be accounted for
	num_par_right_last = 0
	num_par_left_last = 0
	element=[]
	elements = []
	num_elements = 0
	for symbol in line:
		element.append(symbol)
		if symbol=='(':
			num_par_right += 1

		elif symbol ==')':
			num_par_left +=1


		#If the number of parantheses has changed
		if not (num_par_right_last == num_par_right) or not (num_par_left_last== num_par_left):

			if num_par_right-num_par_left==0:
				num_elements+=0
				elements.append(element)
				element = []
				#print 'new',i,line

		num_par_left_last = num_par_left
		num_par_right_last = num_par_right
	return elements

def join(arr):
	#sets an array of chars to string
	if arr:
		return "".join(arr)
	return ''
