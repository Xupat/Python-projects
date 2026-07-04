class Matrix:
	def __init__(self, matrix):
		self.matrix=matrix
		self.rows=len(matrix)
		self.cols=len(matrix[0])
	
	def __repr__(self):
		return f'{self.matrix}'
	def __add__(self, other):
		if self.rows != other.rows or self.cols!=other.cols:
			raise ValueError ('Matrix size do not match')
		result=[]
		for i in range(self.rows):
			row=[]
			for j in range(self.cols):
				row.append(self.matrix[i][j]+other.matrix[i][j])
			result.append(row)
		return Matrix(result)
		
	def __sub__(self, other):
		if self.rows != other.rows or self.cols!=other.cols:
			raise ValueError ('Matrix size do not match')
		result=[]
		for i in range(self.rows):
			row=[]
			for j in range(self.cols):
				row.append(self.matrix[i][j]-other.matrix[i][j])
			result.append(row)
		return Matrix(result)
		
	def __mul__(self, other):
		if self.cols!=other.rows:
			raise ValueError ('Invalid matrix multiplication')
		result=[]
		for i in range(self.rows):
			row=[]
			for j in range(other.cols):
				s=0
				for k in range(self.cols):
					s+=self.matrix[i][k]*other.matrix[k][j]
				row.append(s)
			result.append(row)
		return Matrix(result)
	
	