
class Tower_of_hanoi:
	def __init__(self,number_of_plates,path):
		lines = self.make_pddl_problem(number_of_plates)
		self.make_pddl_file(lines,path)


	def make_pddl_problem(self,number_of_plates):


		#Lines contains the lines which are written to the pddl file
		lines = []

		lines.append('(define (problem hanoi)')
		lines.append('(:domain hanoi)')

		#------------------objects--------------------------------
		lines.append('(:objects')
		lines.append('table1')
		lines.append('table2')
		lines.append('table3')

		for i in range(1,number_of_plates+1):
			lines.append('disk'+str(i))

		lines.append(')')
		#------------------------------------------------------------


		#-------------------Initial state ----------------------
		lines.append('(:init')
		lines.append('(clear disk1)')
		lines.append('(clear table2)')
		lines.append('(clear table3)')
		lines.append('(on disk'+ str(number_of_plates) +' table1)')

		for i in range(1,number_of_plates):
			lines.append('(on disk'+str(i)+" disk"+str(i+1)+')')

		for i in range(1,number_of_plates+1):
			lines.append('(smaller disk'+str(i)+' table1'+')')
			lines.append('(smaller disk'+str(i)+' table2'+')')
			lines.append('(smaller disk'+str(i)+' table3'+')')

		number_of_plates_copy = number_of_plates
		for i in range(1,number_of_plates_copy+1):
			for j in range(1,number_of_plates_copy+1):
				lines.append('(smaller disk'+str(j)+' disk'+str(number_of_plates_copy)+')')
			number_of_plates_copy -= 1


		lines.append(')')




		#--------------------------------------------------------


		#-----------------------Goal----------------------------------
		lines.append('(:goal (and')
		for i in range(1,number_of_plates):
			lines.append('(on disk'+str(i)+" disk"+str(i+1)+')')

		lines.append('(on disk'+ str(number_of_plates) +' table3)')

		lines.append(')))')
		#-------------------------------------------------------------------
		return lines

	def make_pddl_file(self,lines,path):
		with open(path, 'w') as the_file:
			for line in lines:
				the_file.write(line+'\n')
