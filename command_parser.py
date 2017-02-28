"""
Handles the work of validating and processing command input.
"""
import os
from RunCmd import RunCmd
from base import Base, Command
from db import session, engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

def get_valid_commands(queue, fi):
    # TODO: efficiently evaluate commands
    valid_commands = []
    command_list = []
    flag = -1
    try:
    	with open(fi) as f:
    		for line in f:
    			line = line.replace('\n','')
    			if(line):
	    			if line == '[COMMAND LIST]':
	    				flag = 0
	    			elif line == '[VALID COMMANDS]':
	    				flag = 1
	    			else:
	    				if flag==0:
	    					command_list.append(line)
	    				else:
	    					valid_commands.append(line)
    except EnvironmentError as e:
    	print e

    for command in command_list:
    	if command in valid_commands:
    		#print command
    		queue.put(command)

    #print valid_commands
    #print command_list
    
    


def process_command_output(queue):
    # TODO: run the command and put its data in the db
    command = queue.get()
    
    command_executer = RunCmd([command],60)
    command_executer.Run()
    print 'Command --> ',command
    print command_executer.output,command_executer.err,command_executer.time

    
    record = Command(command_string=command,length=len(command),duration=round(command_executer.time),output=command_executer.output)
    print "record -->",record.command_string

    session.add(record)
    print session.query(Command).all()
    session.commit()
    
    #mysession.commit()
    #mysession.remove()
    print "####DOne"
    #for instance in mysession.query(Command).order_by(Command.id):
    #    print(instance.command_string, instance.output)
    


