#!venv/bin/python
from app import app
app.config.from_object(__name__)
app.run(host='0.0.0.0', port=5000, debug=True)