#!/usr/bin/python

with open('hosts.txt', 'r') as f:
	i = 0
	j = 0
	for line in f:
		if line[:1] == '#':
			line = line[1:]
		list_line = line.split()
		#print list_line
		#print "LN: %s" % (i)
		if not list_line:
			#print "Set: %s" % (j)
			j += 1
		for column in list_line[1:]:
			print 'self.dns_config_%s[\'A\'][\'%s\'] = \'%s\'' % (j, column, list_line[0])
		i += 1