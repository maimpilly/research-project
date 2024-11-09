from flask import Flask, render_template, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from filegen import generate_file_names
import sys
import os
sys.path.insert(1, "/usr/src/get_module") #for the docker env
from  transfer_files import File_downloader

app = Flask(__name__)

# Your SPARQL endpoint
sparql_endpoint = 'http://localhost:9090/sparql'

@app.route('/')
def index():
    return render_template('query_form.html')

@app.route('/query', methods=['POST'])
def query():
    sparql_query = request.form['query']
    destination_path = request.form['destination']  # Get the user-specified destination path

    # Query the SPARQL endpoint
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    file_names = generate_file_names(results)
    files = File_downloader(file_names, destination_path)
    files.ssh_file_transfer()
    files.cloud_file_transfer()
    
    if file_names is not None:
        # Create the success message with the destination path value
        message = "Success! File are copied to " + str(destination_path)

        # Create a dictionary with the message and file_names
        response_data = {
            'message': message,
            'file_names': file_names
        }
    else:
        # Handle the case where file_names is None
        response_data = {
            'message': "Success, but no file names available.",
            'file_names': None  # You can customize this message as needed
        }

    # Create a dictionary with the message and file_names
    response_data = {
        'Query Result': message,
        'SPARQL Query Result': results
    }

    # Return a JSON response with the message and file_names
    return jsonify(response_data)
    #return jsonify({'Query Results': results} )
    #return render_template('results.html', results=results, file_message="Files are transferred to the destination!")

if __name__ == '__main__':
    app.run(debug=True)
