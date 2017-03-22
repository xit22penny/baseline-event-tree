__author__ = 'Xian Teng'

import time

# Strong pruning
def StrongPrune(Tree,G,v,MapV):
	Tree['V']['vmark'][MapV[v]] = 1 # 1 indicates visited
	if len(Tree['V']['vneig'][MapV[v]]) > 0:
		for u in Tree['V']['vneig'][MapV[v]]:
			if Tree['V']['vmark'][MapV[u]] != 1:
				StrongPrune(Tree,G,u,MapV)
				if G[v,u] >= Tree['V']['vprize'][MapV[u]]:
					Tree['V']['vmark'][MapV[u]] = -1 # -1 indicates removing
				else:
					Tree['V']['vprize'][MapV[v]] = Tree['V']['vprize'][MapV[v]] + Tree['V']['vprize'][MapV[u]] - G[v,u]
	return Tree
# Prize collective steiner tree problem
def PCSTr(G,vp,r,gamma):
	F = [] # storing outputs
	nVertex = len(vp) # number of vertices
	nComp = len(vp) # number of components
	RootComp = r
	d = [0]*nVertex # d increases to reduce edge deficit
	
	# ---------- initialize dictionary object `Comp` ---------- #
	w = [] # w increases to reduce vertex surplus
	C = [] # the set of vertices belonging to this component
	Id = [] # component Id
	lamda = [] # active or not
	VertexBelong = [] # what's the position of component the vertex belongs to
	for i in range(0, nVertex): # vertex id starting from 0
		w.append(0)
		Id.append(i)
		VertexBelong.append(i)
		C.append({i}) # add set to list
		if(i == r):
			lamda.append(0)
		else:
			lamda.append(1)
	Comp = {'w':w, 'C':C, 'Id':Id, 'lamda':lamda}
	next_id = nVertex # next component Id
	

	# ---------- The process continues until either all vertices are in the root component
	# ---------- or all non-root component surpluses are 0.
	while(1):
		flag = 0
		for i in range(0,len(Comp['lamda'])):
			if Comp['lamda'][i] == 1:
				flag = 1
				break
		if flag == 0:
			break
		# ---- vertex surpluses paying down edge deficits ---- #
		# find an edge to minimize e1
		e1 = float("inf")
		Edge_chosen_i = 0
		Edge_chosen_j = 0
		for i in range(0,nVertex):
			for j in range(i+1,nVertex):
				if VertexBelong[i] == VertexBelong[j] or not(G[i,j] >= 0):
					continue
				if Comp['lamda'][VertexBelong[i]] == 0 and Comp['lamda'][VertexBelong[j]] == 0:
					etmp == float("inf")
				else:
					etmp = float((G[i,j]-d[i]-d[j])/(Comp['lamda'][VertexBelong[i]]+Comp['lamda'][VertexBelong[j]]))
				if etmp < e1:
					e1 = etmp
					Edge_chosen_i = i
					Edge_chosen_j = j
		# print "e1",e1
		# print "edge", Edge_chosen_i, Edge_chosen_j
		# find an edge to minimize e2
		e2 = float("inf")
		Ct_idx = 1
		for i in range(0,len(Comp['lamda'])):
			if Comp['lamda'][i] == 1:
				etmp = sum(vp[x] for x in Comp['C'][i])
				etmp = etmp - Comp['w'][i]
				if etmp < e2:
					e2 = etmp
					Ct_idx = i
			else:
				continue
		# print "e2",e2
		e = min(e1,e2)

		# increase w for all components <-> decrease component surplus
		for i in range(0,len(Comp['w'])):
			Comp['w'][i] = Comp['w'][i] + e*Comp['lamda'][i]

		# increase d for all vertices <-> decrease edge deficit
		for v in range(0,len(VertexBelong)):
			d[v] = d[v] + e*Comp['lamda'][VertexBelong[v]]

		if e == e2 and e1 > e2:
			Comp['lamda'][Ct_idx] = 0
		else:
			F.append([Edge_chosen_i,Edge_chosen_j])
			# ---- union Ci and Cj ---- #
			Comp['C'].append(Comp['C'][VertexBelong[Edge_chosen_i]].union(Comp['C'][VertexBelong[Edge_chosen_j]]))
			Comp['w'].append(Comp['w'][VertexBelong[Edge_chosen_i]] + Comp['w'][VertexBelong[Edge_chosen_j]])
			Comp['Id'].append(next_id)
			next_id = next_id + 1

			if VertexBelong[r] == VertexBelong[Edge_chosen_i] or VertexBelong[r] == VertexBelong[Edge_chosen_j]:
				Comp['lamda'].append(0)
			else:
				Comp['lamda'].append(1)

			# ---- remove Ci and Cj ---- #
			remove_index = VertexBelong[Edge_chosen_i], VertexBelong[Edge_chosen_j]
			Comp['w'] = [i for j, i in enumerate(Comp['w']) if j not in remove_index]
			Comp['C'] = [i for j, i in enumerate(Comp['C']) if j not in remove_index]
			Comp['Id'] = [i for j, i in enumerate(Comp['Id']) if j not in remove_index]
			Comp['lamda'] = [i for j, i in enumerate(Comp['lamda']) if j not in remove_index]
			
			# ---- update component number ---- #
			nComp = len(Comp['lamda'])

			# update VertexBelong for vertices in new component
			# for v in Comp['C'][nComp-1]:
			# 	VertexBelong[v] = nComp

			# update VertexBelong for all vertices
			for i in range(0,nComp):
				for v in Comp['C'][i]:
					VertexBelong[v] = i
					if v == r:
						RootComp = i
		# print Comp

	# print F
	# --- remove the edges --- #
	for edge in F:
		if VertexBelong[edge[0]] != RootComp and VertexBelong[edge[1]] != RootComp:
			F.remove(edge)

	# --- generate a structure for the tree --- #
	# --- The tree contains two components: 1. set of edge objects and 2. set of vertex objects
	if len(F) > 0:
		vt = set()
		eid = []
		ecost = []
		for i in range(0,len(F)):
			vt.add(F[i][0])
			vt.add(F[i][1])
			eid.append(F[i])
			ecost.append(G[F[i][0],F[i][1]])
		# edge object
		E = {'eid':eid, 'ecost':ecost}
	
		vid = []
		vneig = []
		vprize = []
		vmark = []
		MapV = [0]*len(vp) # map vid into position
		cnt = 0
		for v in vt:
			MapV[v] = cnt
			cnt = cnt + 1
			vid.append(v) # original vertex id
			cur_neig = set() # neighbor set for current vertex
			vprize.append(vp[v]) # vertex prize
			vmark.append(0) # mark pruning
			for edge in F:
				if edge[0] == v:
					cur_neig.add(edge[1])
				elif edge[1] == v:
					cur_neig.add(edge[0])
			vneig.append(cur_neig) # add neighbor set

		# vertex object
		V = {'vid':vid, 'vprize':vprize, 'vneig':vneig, 'vmark':vmark}
		# Tree object
		Tree = {'E':E, 'V':V}
		# strong prune tree
		Tree = StrongPrune(Tree,G,r,MapV) # to-be-removed vertices are marked as 1
		# --- remove marked vertices and edges --- #
		rm_vid = []
		for i in range(0,len(Tree['V']['vid'])):
			if Tree['V']['vmark'][i] == -1: # -1 indicates removing
				rm_vid.append(Tree['V']['vid'][i])

		Tree['E']['ecost'] = [i for j,i in enumerate(Tree['E']['ecost']) if Tree['E']['eid'][j][0] not in rm_vid and Tree['E']['eid'][j][1] not in rm_vid]
		Tree['E']['eid'] = [i for j,i in enumerate(Tree['E']['eid']) if Tree['E']['eid'][j][0] not in rm_vid and Tree['E']['eid'][j][1] not in rm_vid]

		vt = set()
		if len(Tree['E']['eid']) > 0:
			for i in range(0, len(Tree['E']['eid'])):
				vt.add(Tree['E']['eid'][i][0])
				vt.add(Tree['E']['eid'][i][1])
		
		Tree['V']['vid'] = [i for j,i in enumerate(Tree['V']['vid']) if j in vt]
		Tree['V']['vprize'] = [i for j,i in enumerate(Tree['V']['vprize']) if j in vt]
		Tree['V']['vneig'] = [i for j,i in enumerate(Tree['V']['vneig']) if j in vt]
		Tree['V']['vmark'] = [i for j,i in enumerate(Tree['V']['vmark']) if j in vt]

		# calculate score
		score = sum(vp)
		for i in range(0,len(Tree['V']['vid'])):
			score = score - vp[Tree['V']['vid'][i]]
		score = score*gamma
		for i in range(0,len(Tree['E']['eid'])):
			score = score + Tree['E']['ecost'][i]
		Tree = {'V':Tree['V'], 'E':Tree['E'], 'score':score}
		return Tree
	else:
		return {'V':{},'E':{},'score':sum(vp)}

def FindTree(G,vp,gamma):
	score = float("inf")
	T = {}
	sorted_index = [i[0] for i in sorted(enumerate(vp), key=lambda x:x[1], reverse=True)] # sort vp by decscending order
	for i in range(0,int(0.5*len(sorted_index))):
		print "the ",i,"th root..."
		v = sorted_index[i] # vertex index
		Temp = PCSTr(G,vp,v,gamma)
		Temp_score = Temp['score']
		if Temp_score < score:
			score = Temp_score
			T = Temp
	return T









