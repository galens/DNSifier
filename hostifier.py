#!/usr/bin/python

import os
hostfile = 'hosts.txt'
if os.path.isfile(hostfile):
  servers = []
  tmp = []
  print 'self.dns_config = dict()'
  print 'self.dns_config[\'prod - no dns override\'] = dict()'
  print 'self.dns_config[\'prod - no dns override\'][\'A\'] = dict()'
  print 'self.dns_config[\'prod - no dns override\'][\'A\'][\'foo.bar\'] = \'127.0.0.1\''
  with open(hostfile, 'r') as f:
    i = 0
    j = 1
    for line in f:
      if line[:1] != '#' and line.split():
        servers.append(line.rstrip())
        print 'self.dns_config[\'' + servers[-1] + '\'] = dict()'
        print 'self.dns_config[\'' + servers[-1] + '\'][\'A\'] = dict()'
      elif line[:1] == '#':
        line = line[1:]
        list_line = line.split()
        for column in list_line[1:]:
          print 'self.dns_config[\'' + servers[-1] + '\'][\'A\'][\'' + column + '\'] = ' + '\'' + list_line[0] + '\''
          #print 'self.dns_config_%s[\'A\'][\'%s\'] = \'%s\'' % (j, column, list_line[0])
      else:
        j +=1
      i += 1

print servers
			