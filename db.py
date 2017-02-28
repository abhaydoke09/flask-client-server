from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


engine = create_engine('sqlite:///commands.db')
session = sessionmaker(autocommit=True,autoflush=True,bind=engine)()
#Session = scoped_session(session)
#Base.metadata.create_all(engine)
#record = Command(command_string='abcd',length=1,duration=1,output='output')
#print "record -->",record.command_string
    #session = Session()
#session.add(record)
#for instance in session.query(Command).order_by(Command.id):
#	print(instance.command_string, instance.output)




