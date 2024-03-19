#-*- coding: utf-8 -*-
'''
Created on 2016. 11. 19
Updated on 2016. 01. 09
'''
from __future__ import print_function

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from commons import Subjects
from results.Items import ResultItem, BugSummaryItem, ProjectSummaryItem


class Evaluator():
	'''
	Evaluate the result of IRBL Techniques
	input : program, project, versions
	output : program-project sheet data, summary_bugs, summary_project
	'''
	__name__ = u'Evaluator'
	program = u''
	project = u''
	projectSummary = None
	k = 1000
	# top-k LOC

	rawData = None
	bugSummaries = None

	def __init__(self, _type, _program, _group, _project, _version):
		self.type = _type
		self.program = _program
		self.group = _group
		self.project = _project
		self.version = _version
		self.projectSummary = ProjectSummaryItem(_project)
		self.S = Subjects()
		pass

	def cmp(self, _x, _y):
		if _x.rank < _y.rank:
			return -1
		elif _x.rank > _y.rank:
			return 1
		return 0

	def evaluate(self, _ansCnts, _bugcnt, _isFile):
		'''
		evaluate merged data
		:param _files:
		:param _bugs:
		:return:
		'''
		data_keys = self.rawData.keys()
		data_keys.sort()
		for bugID in data_keys:
			if bugID in _ansCnts:
				# print('this bug id is %s'%bugID)
				self.rawData[bugID].sort(self.cmp)
				best_recommended = ["", 99999]
				version = self.rawData[bugID][0].version
				rankList = self.S.getPath_bugid_result(self.type, self.program, self.group, self.project, version, bugID)
				for order in range(len(self.rawData[bugID])):			# for each bug id's results
					this = self.rawData[bugID][order]
					if this.rank < best_recommended[1]:
						best_recommended[0] = this
						best_recommended[1] = this.rank
					# calculation
					this.top1 = 1 if this.rank < 1 else 0
					this.top5 = 1 if this.rank < 5 else 0
					this.top10 = 1 if this.rank < 10 else 0
					this.AnsOrder = order
					this.AP = float(this.AnsOrder+1) / (this.rank+1)
					this.TP = (1.0/(this.rank+1)) if this.AnsOrder == 0 else 0
				# print('%s best rank is %s : %s'%(bugID, best_recommended[0].filename, best_recommended[1]))
				this.loc = 0 if best_recommended[1] == 0 else self.calcLOC(best_recommended[0], rankList, version, _isFile)
				this.topkLoc[0] = 1 if this.loc < 100 else 0
				this.topkLoc[1] = 1 if this.loc < 500 else 0
				this.topkLoc[2] = 1 if this.loc < 1000 else 0
				this.topkLoc[3] = 1 if this.loc < 5000 else 0
			else:
				continue

		# make summary
		self.bugSummaries = {}
		for bugID in data_keys:
			if bugID in _ansCnts:
				item = BugSummaryItem(bugID, self.rawData[bugID][0].version)
				for this in self.rawData[bugID]:
					item.top1 += this.top1
					item.top5 += this.top5
					item.top10 += this.top10
					for i in range(len(this.topkLoc)):
						item.topkLoc[i] += this.topkLoc[i]
					item.loc = this.loc
					item.AP += this.AP
					item.TP += this.TP

				# item.top1 = 1 if item.top1 >= 1 else 0
				# item.top5 = 1 if item.top5 >= 1 else 0
				# item.top10 = 1 if item.top10 >= 1 else 0
				item.AP = item.AP / _ansCnts[bugID]   #len(self.rawData[bugID])
				self.bugSummaries[bugID] = item
			else:
				continue

		# evaluate
		for bugID in data_keys:
			if bugID in _ansCnts:
				item = self.bugSummaries[bugID]
				self.projectSummary.top1 += 1 if item.top1 >= 1 else 0
				self.projectSummary.top5 += 1 if item.top5 >= 1 else 0
				self.projectSummary.top10 += 1 if item.top10 >= 1 else 0
				for i in range(len(item.topkLoc)):
					self.projectSummary.topkLoc[i] += 1 if item.topkLoc[i] >= 1 else 0
				self.projectSummary.loc += item.loc
				self.projectSummary.MAP += item.AP
				self.projectSummary.MRR += item.TP
			else:
				continue

		print(len(self.bugSummaries))
		recommendedBugCnt = len(self.bugSummaries)
		self.projectSummary.top1P  = (self.projectSummary.top1 / float(recommendedBugCnt)) if recommendedBugCnt > 0 else 0
		self.projectSummary.top5P  = (self.projectSummary.top5 / float(recommendedBugCnt)) if recommendedBugCnt > 0 else 0
		self.projectSummary.top10P = (self.projectSummary.top10 / float(recommendedBugCnt)) if recommendedBugCnt > 0 else 0
		for i in range(len(self.projectSummary.topkLoc)):
			self.projectSummary.topkLocP[i] = (self.projectSummary.topkLoc[i] / float(recommendedBugCnt)) if recommendedBugCnt > 0 else 0
		self.projectSummary.MAP    = (self.projectSummary.MAP / float(recommendedBugCnt)) if recommendedBugCnt > 0 else 0
		self.projectSummary.MRR    = (self.projectSummary.MRR / float(recommendedBugCnt)) if recommendedBugCnt > 0 else 0
		pass

	def load(self, _files):
		'''
		load specific project's data set
		:param _files:
		:return: data = {id:[ResultItem(), ...], ...}
		'''
		def line_iterator(_filename):
			data = open(_filename, 'r')
			while True:
				line = data.readline()
				if line is None or len(line) == 0: break
				line = line[:-1]

				columns = line.split('\t')
				if len(columns) != 4: continue

				yield columns
			data.close()

		self.rawData = {}
		for filename in _files:
			if os.path.exists(filename) is False:
				print('There are no file : %s' % filename)
				continue

			version = self.getVersion(filename)
			for columns in line_iterator(filename):
				bid = int(columns[0])
				# if (version,bid) not in [('COLLECTIONS_3_0', 384), ('COLLECTIONS_4_0', 512)]:
				# 	print('exclude bug id=%s' % bid)
				# 	continue
				if bid not in self.rawData:
					self.rawData[bid] = []
				if columns[3]=='NaN':
					columns[3] = '0'
				self.rawData[bid].append(ResultItem(bid, version, columns[1], int(columns[2]), float(columns[3])))

		return self.rawData

	def getVersion(self, _filepath):
		idx1 = _filepath.rfind(u'/')
		idx2 = _filepath.rfind(u'\\')
		if idx1 < idx2:
			idx1 = idx2
		filename = _filepath[idx1+1:]
		idx1 = filename.find(u'_')
		idx2 = filename.find(u'_', idx1 + 1)
		version = filename[idx2+1:]
		return version[:version.rfind(u'_')]

	def output(self, _filepath):
		f = open(_filepath, 'w')
		f.write('Evaluation:\n\t%s' % self.projectSummary)
		f.write('\nSummary:\n')
		for bugID in self.bugSummaries.keys():
			item = self.bugSummaries[bugID]
			f.write('\t%s\n' % item.get_rwa())

		f.write('\n\n----------------------------------\nData:\n')
		for bugID in self.rawData.keys():
			items = self.rawData[bugID]
			for item in items:
				f.write('\t%s\n' % item.get_raw())
		pass

	def calcLOC(self, _best, _filepath, _version, _isFile):
		'''
		calculate line of code
		:param _best, _filepath:
		:return: loc
		'''
		def line_iterator(rank ,_filepath):
			data = open(_filepath, 'r')
			while rank > 0:
				line = data.readline()
				if line is None or len(line) == 0: break
				line = line[:-1]

				columns = line.split('\t')
				if len(columns) != 3: continue

				yield columns
				rank-=1
			data.close()

		if os.path.exists(_filepath) is False:
			print('There are no file : %s' % _filepath)
			return 0
		else:
			import subprocess
			loc = 0
			for columns in line_iterator(_best.rank , _filepath):
				if _isFile is False:
					str = columns[2].split('.')
					name = (str[-2] + '.' + str[-1]).replace('#', '\#').replace('(','\(').replace(')','\)')
					cmd = 'find %s -name %s | xargs grep -v -e \'^\s*import\' -e \'^\s*$\' | wc -l'%(self.S.getPath_source(self.group, self.project, _version).decode(), name)
				else:
					str = columns[2].split('.')
					name = str[-2] + ('\#')
					cmd = 'find %s -name %s* | xargs grep -v -e \'^\s*import\' -e \'^\s*$\' | wc -l'%(self.S.getPath_Msource(self.group, self.project, _version).decode(), name)
				# print('CMD:: %s'%cmd)
				loc += int(subprocess.check_output(cmd, shell=True))
		return loc


if __name__ == "__main__":
	pass