## Development Server
Install virtualenv
On macOS and Linux:
    python3 -m venv env
On Windows:
    py -m venv env

Next you will need to activate the virtual environment
On macOS and Linux:
    source env/bin/activate
On Windows:
    .\env\Scripts\activate

Use pip to install the requirements for the server
    pip install -r requirements.txt

Start the server
    python3 server.py