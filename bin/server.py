#!/usr/bin/env python3

import json
import subprocess
import tempfile
import re

from ingredient_phrase_tagger.training import utils
from http.server import BaseHTTPRequestHandler, HTTPServer

from googletrans import Translator

def simplify(input_string):
    # Add space between number and text (e.g., "30cl" to "30 cl")
    updated_string = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', input_string)

    # Remove " of " from the string
    updated_string = updated_string.replace(" of ", " ")

    return updated_string

def _exec_crf_test(input_text, model_path):
    with tempfile.NamedTemporaryFile(mode='w') as input_file:
        input_file.write(utils.export_data(input_text))
        input_file.flush()
        return subprocess.check_output(
            ['crf_test', '--verbose=1', '--model', model_path,
             input_file.name]).decode('utf-8')


def _convert_crf_output_to_json(crf_output):
    return json.dumps(utils.import_data(crf_output), indent=2, sort_keys=True)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/parse":
            # Get the length of the data
            content_length = int(self.headers['Content-Length'])

            # Read the POST body
            post_data = self.rfile.read(content_length).decode('utf-8')

            print(post_data)
            text = ""

            try:
                translator = Translator()
                translation = translator.translate(post_data, dest='en')
                text = translation.text
            except Exception as e:
                print(e)
                text = post_data
            text = simplify(text)

            # Assuming ingredients are provided as a string with ingredients separated by \n
            ingredients = text.split('\n')

            raw_ingredient_lines = [x for x in ingredients if x]
            crf_output = _exec_crf_test(raw_ingredient_lines, "./model/model.crfmodel")
            response = json.loads(_convert_crf_output_to_json(crf_output.split('\n')))

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            print(json.dumps(response))

            # Convert response to JSON and send
            self.wfile.write(json.dumps(response).encode('utf-8'))

# Server setup
def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()