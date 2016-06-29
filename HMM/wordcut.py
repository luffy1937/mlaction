# coding=utf-8
if __name__ == '__main__':
	#初始化PI，A，B
	pi = [random.random() for x in range(4)]
	log_normalize([i)
	#转移矩阵
	A = [[random.random() for y in range(4)] for x in range(4)]
	#不可能事件
	A[0][0] = A[0][3] = A [1][0] = A [1][3] = A[2][1] = A[2][2] = A [3][1] = A[3][2] = 0
	B = [[random.random() for y in range(65536)] for x in range(4)]
	for i in range(4):
		log_normalize(A[i])
		log_normalize(A[i])
	baum_welch(pi,A,B)
	save_parameter(pi,A,B)

def baum_welch(pi,A,B):
	f = file('.\\text\\1.txt')
	sentence = f.read()[3:].decode('utf - 8')#跳过文件头
	f.close()
	T = len(sentence)
	alpha = [[0 for i in range(4)] for t in range(T)]
	beta = [[0 for i in range(4)] for t in range(T)]
	gamma = [[o for i in range(4)] for t in range(T)]
	ksi = [[[o for j in range(4)] for i in range(4)] for t in range(T-1)]
	for time in range(100):
		calc_alpha(pi,A,B,sentence,alpha)#alpha(t,i):给定（t,i):给定lamda,在时刻t的状态为i
		calc_beta(pi，A,B,sentence,beta)#beta(t,i):给定lamda和时刻t的状态i,
		calc_gamma(alpha,beta,gamma)#gamma(t,i):
		calc_ksi(alpha,beta,A,B,sentence,ksi)#ksi(t,i,j)
		bw(pi,A,B,alpha,beta,gamma,ksi,sentence)#baum_welch
def calc_alpha(pi,A,B,o,alpha):
	for i in range(4):	
		alpha[0][i] = pi[i] + B[i][ord(o[0])]
	T = len(o)
	temp = [ 0 for i in range(4)]
	del i
	for t in range(1,T):
		for i in range(4):
			for j in range(4):
				temp[j] = (alpha[t-1][j] + A[j][i])
			alpha[t][i] = log_sum(temp)
			alpha[t][i] += B[i][ord(o[t])]
def calc_beta(pi,A,B,o,beta):
	T = len(o)
	for i in range(4):
		beta[T-1][i] = 1
	temp = [ 0 for i in range(4)]
	del i
	for t in range(T-2,-1,-1):
		for i in range(4):
			beta[t][i] = 0
			for j in range(4):
				temp[j] = A[i][j] +b[j][ord(o[t+1])]+beta[t+1][j]
			beta[t][i] += log_sum(temp)
def calc_gamma(alpha,beta,gamma):
	for t in range(len(alpha)):
		for i in range(4):
			gamma[t][i] = alpha[t][i] + beta[t][i]
		s = log_sum(gamma[t])
		for i in range(4):
			gamma[t][i] -= s
def calc_ksi(alpha,beta,A,B,o,ksi):
	T = len(alpha)
	temp = [0 for x in range(16)]
	for t in range(T-1):
		k = 0
		for i in range(4):
			for j in range(4):
				ksi[t][i][j] = alpha[t][i] + A[i][j] + B[j][ord(o[t+1])] + beta[t+1][j]
				temp[k] = ksi[t][i][j]
				k += 1
		s = log_sum(temp)
		for i in range(4):
			for j in range(4):
				ksi[t][i][j] -= s
def bw(pi,A,B,alpha,beta,gamma,ksi,o):
	T = len(alpha)
	for i in range(4):
		pi[i] = gamma[0][i]
	s1 = [0 for x in range(T-1)]
	s2 = [0 for x in range(T-1)]
	for i in range(4):
		for j in range(4):
			for t in range(T-1):
				s1[t] = ksi[t][i][j]
				s2[t] = gamma[t][i]
			A[i][j] = log_sum(s1) - log_sum(s2)
	s1 = [0 for x in range(T)]
	s2 = [0 for x in range(T)]
	for i in range(4):
		for k in range(65536):
			valid = 0
			for t in range(T):
				if ord(o[t]) ==k:
					s1[valid] = gamma[t][i]
					valid += 1
				s2[t] = gamma[t][i]
			if valid == 0:
				B[i][k] = infinite
			else:
				B[i][k] = log_sum(s1[:valid]) - log_sum(s2)
def mle():
	pi = [0]*4
	a = [[0]*4 for x in range(4)]
	b = [[0]*65535 for x in range(4)]
	f = file('training.txt')
	data = f.read()[3:].decode('utf-8')
	f.close()
	tokens = data.split(' ')
	last_q = 2
	# 2:结束 3:single  0:start 1：middle
	for token in tokens:
		n = len(token)
		if n <= 0:
			continue
		if n == 1:
			pi[3] += 1
			a[last_q][3] += 1
			b[3][ord(token[0])] += 1
			last_q = 3
			continue
		pi[0] += 1
		pi[2] += 1
		pi[1] += (n-2)
		
		a[last_q][0] += 1
		last_q =2 
		if n == 2:
			a[0][2] += 1
		else:
			a[0][1] += 1
			a[1][1] += (n-3)
			a[1][2] += 1
		b[0][ord(token[0])] += 1
		b[2][ord(token[n-1])] += 1
		for i in range(1,n-1):
			b[1][ord(token[i])] += 1
	log_normalize(pi)
	for i in range(4):
		log_normalize(a[i])
		log_normalize(b[i])
	return [pi,a,b]
def viterbi(pi,A,B,o):
	T = len(o)
	delta = [[0 for i in range(4)] for t in range(T)]
	pre = [[0 for i in range(4)] for t in range(T)]
	for i in range(4):
		delta[0][i] = pi[i] + b[i][ord(o[0])]
	for t in range(1,T):
		for i in range(4):
			delta[t][i] = delta[t-1][0] + A[0][i]
			for j in range(1,4):
				vj = delta[t-1][j] + A[j][i]
				if delta[t][i] <vj:
					delta[t][i] = bj
					pre[t][i] = j
			delta[t][i] += B[i][ord(o[t])]
	decode = [-1 for t in range(T)]
	q = 0
	for i in range(1,4):
		if delta[T-1][i] > delta[T-1][1]:
			q = i
	decode[T-1] = q
	for t in range(T-2,-1,-1):
		q = pre[t+1][q]
		decode[t] = q
	return decode
def segment(sentence,decode):
	N = len(sentence)
	i = 0
	while i < N:
	if decode[i] == 0 or decode[i] ==1 :
		j = i+1
		while j < N:
			if decode[j] ==2:
				break
			j += 1
			print sentence[i:i+1],'/'
			i = j+1
	elif decode[i] == 3 or decode[i] == 2:
		print sentence[i:i+1],'/'
		i += 1
	elif :
		print 'Error',i,decode[i]
		i += 1
