#!venv/bin/python
from app import app

context = ('chamayetu.com.crt', 'chamayetu.com.key')

app.config.from_object(__name__)
app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=context, threaded=True)
