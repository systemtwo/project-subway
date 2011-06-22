#This is the db_sync()er for the SERVER ONLY

import safeevalnew
def db_sync(newdb):
	print "Opening old DB (Reading)"
	tempdb = {}
	newdbhosts = []
	olddbhosts = []
	try:
		g = open ("db", "r")
		olddb = safeevalnew.safe_eval(g.read())
		g.close()
	except IOError:
		#File does not exist, so just dump all what you have in file
		g = open ("db", "w")
		g.write(str(newdb))
		g.close
		return 1
	print "Syncing old with recv'd DB"
	print newdb
	#Update where newdb's date-modified is newer
	inter = set(newdb.iterkeys()).intersection(set(olddb.iterkeys())) #Find common entries
	print inter

	#for i in inter:
		#if (olddb[i]["host"] == newdb[i]["host"]):
			#if (olddb[i]["date-modified"] < newdb[i]["date-modified"]):
				#print "Updating Old entry"
				#tempdb[i] = {"date-modified": newdb[i]["date-modified"], "host": newdb[i]["host"]}
			#elif (olddb[i]["date-modified"] >= newdb[i]["date-modified"]):
				#tempdb[i] = {"date-modified": olddb[i]["date-modified"], "host": newdb[i]["host"]}
	
	for i in inter:
		filehostsarray = [] #This is the array which the hosts for ONE file should be stored in
		tempdb[i] = []
		print "Working on", i
		print "Operating Data", len(olddb[i]), len(newdb[i])
		print olddb[i]
		print newdb
		for j in range(len(olddb[i])):
			print olddb[i][j]
			olddbhosts.append(olddb[i][j]["host"])
			for k in range(len(newdb[i])):
				newdbhosts.append(newdb[i][k]["host"])
				print "On Loop", i, j, k
				if (olddb[i][j]["host"] == newdb[i][k]["host"]):
					if (olddb[i][j]["date-modified"] < newdb[i][k]["date-modified"]):
						#if (olddb[i][j]["host"] == newdb[i][k]["host"]):
						print "Entry", i, "is newer in new"
						tempdb[i].append (newdb[i][k])
						print "Entry appended to index", j
						print tempdb
					elif (olddb[i][j]["date-modified"] >= newdb[i][k]["date-modified"]):
						#if (olddb[i][j]["host"] == newdb[i][k]["host"]):
						print "olddb is newer for entry", i
						print "Adding entry for host:", olddb[i][j]["host"]
						tempdb[i].append(olddb[i][j])
						print "Entry appended from index", j
						#print tempdb
						#print "!!!!!!!!!!!!!"
						#print "filehostsarray is currently"
						#print filehostsarray
						print "**********"
						#print tempdb[i]
						#print i,j
						#tempdb[i].append(olddb[i][j])
						#print tempdb[i]
					
		#Add in entries from other hosts for same file
		#Get rid of duplicates
		newdbhosts.sort()
		last = newdbhosts[-1]
		for t in range(len(newdbhosts)-2, -1, -1):
			if (last == newdbhosts[t]):
				del newdbhosts[t]
			else:
				last = newdbhosts[t]
		print newdbhosts

		olddbhosts.sort()
		last = olddbhosts[-1]
		for t in range(len(olddbhosts)-2, -1, -1):
			if (last == olddbhosts[t]):
				del olddbhosts[t]
			else:
				last = olddbhosts[t]
		print olddbhosts

		#Hosts to be added to the same file but different host
		commonhosts = list (set (newdbhosts) & set (olddbhosts))
		uniquehosts = list (set(newdbhosts) - set (commonhosts))
		print "UniqueHosts", uniquehosts

		#Add entries listed in uniquehosts
		if (len(uniquehosts) > 0):
			for k in range(len(newdb[i])):
				for l in range(len(uniquehosts)):
					if (newdb[i][k]["host"] == uniquehosts[l]):
						print "Adding new entry for file", i
						tempdb[i].append (newdb[i][k])
		print "\n\n=========="
		# Clean up the newdbhosts and olddbhosts arrays
		del olddbhosts[:]
		del newdbhosts[:]
					
	print tempdb
	
	#Add new file (not host) Entries
	#This implementation is BAD because it includes files from both DBs
		#c = set(newdb).union(set(olddb))
		#d = set(newdb).intersection(set(olddb))
		#uninter = c-d
	#uninter = set(newdb.iterkeys()) - set(inter)
	#print uninter
	#print newdb
		#for i in uninter:
			#tempdb[i] = newdb[i]
		

	#Add olddb entries NOT present in newdb
	c = set(newdb).intersection(set(olddb))
	d = set(olddb)
	oldunique = d-c

	for a in oldunique:
		print "Adding from olddb (oldunique)", a
		tempdb[a] = olddb[a]
	
	#Add newdb entries NOT present in olddb
	e = set (newdb)
	newunique = e-c

	for b in newunique:
		print "Adding from newdb (newunique)", b
		tempdb[b] = newdb[b]
	
	#Save newly constructed db
	print "Sync'd DB Saved"
	return tempdb
