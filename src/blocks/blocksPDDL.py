
class blocks:
	def __init__(self,path,number_of_stacks=3,height=3):
		#lines = self.make_pddl_problem(number_of_stacks,height)
		#self.make_pddl_file(lines,path)
		a= 1


	def make_pddl_problem(self,number_of_stacks,height):


		#Lines contains the lines which are written to the pddl file
		lines = []

		lines.append('(define (problem blocks)')
		lines.append('(:domain BLOCKS)')

		#------------------objects--------------------------------
		lines.append('(:objects')


		lines.append(')')
		#------------------------------------------------------------


		#-------------------Initial state ----------------------
		lines.append('(:init')

		lines.append(')')




		#--------------------------------------------------------


		#-----------------------Goal----------------------------------
		lines.append('(:goal (and')

		lines.append(')))')
		#-------------------------------------------------------------------
		return lines

	def make_pddl_file(self,lines,path):
		with open(path, 'w') as the_file:
			for line in lines:
				the_file.write(line+'\n')
