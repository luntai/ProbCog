from MLN import MLN
from math import exp, log
import random

class StringBuffer:
	def __init__(self):
		self.buf = ""
	
	def write(self, s):
		self.buf += s
		
	def __str__(self):
		return self.buf

def createRandomMLN(numVars, numFeatures, maxCliqueSize, maxWeight, numProbConstraints):
	f = StringBuffer()
	# write declarations
	f.write("obj = {X}\n")
	vars = []
	for i in xrange(numVars):
		f.write("p%d(obj)\n" % i)
		vars.append("p%d(X)" % i)
	# write formulas
	for i in xrange(numFeatures):
		cliqueSize = random.randint(1, maxCliqueSize)
		clique = random.sample(vars, cliqueSize)
		lits = []
		for var in clique:
			lits.append("%s%s" % ({0: "!", 1: ""}[random.randint(0,1)], var))		
		#weight = log(random.uniform(1, exp(maxWeight)))
		weight = random.gauss(0, maxWeight/2)
		f.write("%f %s\n" % (weight, " v ".join(lits)))
	# write probability constraints
	pcVars = random.sample(vars, numProbConstraints)
	for v in pcVars:
		f.write("R(%s)=%f\n" % (v,random.uniform(0,1)))
		f.write("0 %s\n" % v)
	return (vars, str(f), pcVars)

def test():
	# create MLN
	vars, mlnContent, pcVars = createRandomMLN(4, 4, 4, log(50), 2)		
	#print mlnContent
	# run IPFP-M
	if True:
		mln = MLN(mlnContent=mlnContent, verbose=False)
		mln.combine({})	
		print mln.inferIPFPM(vars)
	# run MC-SAT-PC
	mln = MLN(mlnContent=mlnContent, verbose=False)
	mln.combine({})
	print mln.inferMCSAT(vars, maxSteps=10000, infoInterval=1000, resultsInterval=1000, verbose=False, details=False)

test()