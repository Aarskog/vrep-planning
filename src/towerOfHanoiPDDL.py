class Tower_of_hanoi:
	def __init__(self,number_of_plates):


	def make_pddl_problem(self):


		#Lines contains the lines which are written to the pddl file
		lines = []

		lines.append('(define (problem hanoi)')
		lines.append('(:domain hanoi)')

		#------------------objects--------------------------------
		lines.append('(:objects')
		lines.append('')

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

		self.make_pddl_file(lines,path)

	def make_pddl_file(self,lines,path):
		with open(path, 'w') as the_file:
			for line in lines:
				the_file.write(line+'\n')
