export FLASK_APP=app.py
export FLASK_DEBUG=true
export FLASK_ENV=development

flask run --host=0.0.0.0 
# add '--cert=adhoc' to use https instead of http