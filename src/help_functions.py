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
	if not num_par_right-num_par_left == 0:
		raise ValueError('get_elements() error in: ',line,'. Inconsistent number of parantheses')
	return elements

def join(arr):
	#sets an array of chars to string
	return "".join(arr)
