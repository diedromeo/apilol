import os
from flask import Flask, request, jsonify, render_template_string

# The secret flag for this CTF. Don't tell anyone!
FLAG = "ctf7{Fl45k_4p15_C4n_B3_Tr1cky_D0nt_TrusT_The_D0c5}"
SECRET_KEY = "super_secret_ctf_key_12345"

app = Flask(__name__)

# Main route with a basic intro and a link to the docs.
# This serves as the entry point for the CTF.
@app.route('/')
def home():
    """Renders the main homepage."""
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Flask CTF Challenge</title>
            <style>
                body {
                    font-family: sans-serif;
                    background-color: #f0f4f8;
                    color: #333;
                    text-align: center;
                    padding: 50px;
                }
                .container {
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                }
                h1 {
                    color: #2c3e50;
                }
                a {
                    color: #3498db;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to the Flask CTF Challenge!</h1>
                <p>Your mission, should you choose to accept it, is to find the hidden flag.</p>
                <p>The journey begins with our simple API. Check out the <a href="/docs">API documentation</a> to get started.</p>
            </div>
        </body>
        </html>
    ''')

# Route to serve the documentation.
# In a real app, this would be more complex, but for this CTF, we'll
# just read the markdown file and serve it as plain text.
@app.route('/docs')
def api_docs():
    """Serves the API documentation."""
    try:
        # Note: In a real-world scenario, you should use a Markdown library to
        # convert this to HTML for a better user experience.
        with open('api_docs.md', 'r') as f:
            docs_content = f.read()
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>API Documentation</title>
                <style>
                    body {
                        font-family: monospace;
                        background-color: #2d2d2d;
                        color: #f8f8f2;
                        padding: 20px;
                    }
                    pre {
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    }
                </style>
            </head>
            <body>
                <pre>{{ docs_content }}</pre>
            </body>
            </html>
        ''', docs_content=docs_content)
    except FileNotFoundError:
        return "API documentation not found. Did you create the api_docs.md file?", 404

# The main CTF API endpoint.
# The documentation will guide users to provide a specific header, but there's a trick.
@app.route('/api')
def get_flag():
    """
    CTF API endpoint.
    Checks for a valid 'X-CTF-Token' header.
    A hidden parameter can reveal the flag.
    """
    
    # Get the value of the 'X-CTF-Token' header from the request.
    token = request.headers.get('X-CTF-Token')

    # Check for a specific, undocumented query parameter.
    if request.args.get('debug') == 'true':
        print(f"DEBUG_MODE_ACTIVATED: A debug query parameter was used.")
        return jsonify({
            "status": "success",
            "message": "Debug mode enabled. You found a secret!",
            "flag": FLAG
        })

    # The documented path, which requires a valid header.
    if token == SECRET_KEY:
        return jsonify({
            "status": "success",
            "message": "Token is valid. Good job! But this isn't the flag. You're on the right track, but something is missing..."
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid or missing X-CTF-Token header. Refer to the documentation."
        }), 401

if __name__ == '__main__':
    # Make sure the documentation file exists before running.
    if not os.path.exists('api_docs.md'):
        print("Warning: 'api_docs.md' not found. Please create the file to view the documentation.")
    # In a real CTF, debug=False would be used.
    # We set debug=True here for ease of development.
    app.run(debug=True)
