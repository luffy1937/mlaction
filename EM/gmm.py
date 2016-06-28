def calcEM(height):
	N = len(height)
	gp = 0.5
	bp = 0.5
	gmu,gsigma = min(height),1
	bmu,bsigma = max(height),1
	ggamma = range(N)
	ggamma = range(N)
	cur = [gp, bp, gmu, gsigma, bmu, bsigma]
	now = []
	times = 0
	while times < 100:
		i = 0
		for x in height:
			ggamma[i] = gp*gauss(x,gmu,gsigma)
			bgamma[i] = bp*gauss(x,bmu,bsigma)
			s = ggamma[i] + bgamma[i]
			ggamma[i] /= s
			bgamma[i] /= s
			i += 1
		gn = sum(ggamma)
		gp = float(gn)/float(N)
		bn = sum(bgamma)
		bp = float(bn) /float(N)
		gmu = averageWeight(height,ggamma,gn)
		gsigma = varianceWeight(height,ggamma,gmu,gn)
		bmu = averageWeight(height,bgamma,bn)
		bsigma = varianceWeight(height,bgamma,bmu,bn)
		now = [gp,bp,gmu,gsigma,bmu,bsigma]
		if isSame(cur,now):
			break
		cur = now
		print 'times:',times
		print 'girl mean/gsigma:',gmu,gsigma
		print 'bog mean/bsigma:',bmu,bsigma
		print 'bog/girl:',bn,gn,bn+gn
		times += 1
	return now
