#!/usr/bin/python

with open('hosts', 'r') as f:
	for line in f:
		list_line = line.split()
		print list_line
		if line[:1] != '#':
			host_set_name = line
		else:
			for column in list_line:
				  print 'self.dns_config_%s[\'A\'][\'%s\'] = \'%s\'' % (j, column, list_line[0])
		