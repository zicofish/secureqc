eval `ps awux | grep 'java .*parallel' | grep -v 'grep' | awk '{print "kill -9 " $2}'`
