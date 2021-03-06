"""
Details the various flask endpoints for processing and retrieving
command details as well as a swagger spec endpoint
"""

from multiprocessing import Process, Queue
import sys
from flask import Flask, request, jsonify
from flask_swagger import swagger

from db import session, engine
from base import Base, Command
from command_parser import get_valid_commands, process_command_output

app = Flask(__name__)


@app.route('/commands', methods=['GET'])
def get_command_output():
    """
    Returns as json the command details that have been processed
    ---
    tags: [commands]
    responses:
      200:
        description: Commands returned OK
      400:
        description: Commands not found
    """
    

    #fi = request.args.get('filename')
    #mysession = Session()
    #session = Session()
    try:
        commands = session.query(Command).all()
    except:
        return "No table found"
    #commands = session.query(Command).all()
    print "####",commands
    record_list = []
    for instance in session.query(Command).group_by(Command.command_string):
        record_list.append({'command_string':instance.command_string, 'length':instance.length,'duration':instance.duration,'output':instance.output})
    return jsonify(results = record_list)
    #return 'Successfully processed commands.'
    #Session.remove()
    # TODO: format the query result
    # return jsonify(commands)


@app.route('/commands', methods=['POST'])
def process_commands():
    """
    Processes commmands from a command list
    ---
    tags: [commands]
    parameters:
      - name: filename
        in: formData
        description: filename of the commands text file to parse
                     which exists on the server
        required: true
        type: string
    responses:
      200:
        description: Processing OK
    """
    #print request.args.get('filename')
    fi = request.args.get('filename')


    if fi:
        queue = Queue()
        get_valid_commands(queue, fi)
        processes = [Process(target=process_command_output, args=(queue,))
                     for num in range(2)]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        
        return 'Successfully processed commands.'
    else:
        return 'Filename not given'


@app.route('/database', methods=['POST'])
def make_db():
    """
    Creates database schema
    ---
    tags: [db]
    responses:
      200:
        description: DB Creation OK
    """
    
    Base.metadata.create_all(engine)
    f = open('reload.py','wb')
    f.close()
    
    return 'Database creation successful.'


@app.route('/database', methods=['DELETE'])
def drop_db():
    """
    Drops all db tables
    ---
    tags: [db]
    responses:
      200:
        description: DB table drop OK
    """
    Base.metadata.drop_all(engine)
    f = open('reload.py','wb')
    f.close()
    return 'Database deletion successful.'


if __name__ == '__main__':
    """
    Starts up the flask server
    """
    port = 8080
    use_reloader = True

    # provides some configurable options
    for arg in sys.argv[1:]:
        if '--port' in arg:
            port = int(arg.split('=')[1])
        elif '--use_reloader' in arg:
            use_reloader = arg.split('=')[1] == 'true'

    app.run(port=port, debug=True, use_reloader=use_reloader)


@app.route('/spec')
def swagger_spec():
    """
    Display the swagger formatted JSON API specification.
    ---
    tags: [docs]
    responses:
      200:
        description: OK status
    """
    spec = swagger(app)
    spec['info']['title'] = "Nervana cloud challenge API"
    spec['info']['description'] = ("Nervana's cloud challenge " +
                                   "for interns and full-time hires")
    spec['info']['license'] = {
        "name": "Nervana Proprietary License",
        "url": "http://www.nervanasys.com",
    }
    spec['info']['contact'] = {
        "name": "Nervana Systems",
        "url": "http://www.nervanasys.com",
        "email": "info@nervanasys.com",
    }
    spec['schemes'] = ['http']
    spec['tags'] = [
        {"name": "db", "description": "database actions (create, delete)"},
        {"name": "commands", "description": "process and retrieve commands"}
    ]
    return jsonify(spec)
