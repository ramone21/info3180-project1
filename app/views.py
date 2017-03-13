"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
import psycopg2
from datetime import datetime
from random import randint
from app import app,db
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify,Response,json
from models import UserProfile
from werkzeug.utils import secure_filename



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/profile',methods=['POST','GET'])
def profile():
    """Render the website's profile page."""
    
    file_folder = 'app/static/uploads'
    filename='no file'
   
    if request.method == 'POST':
        uid=720000000+randint(10000,99999)
        creation =datetime.now()
    
        fname=request.form.get('fname')
        lname=request.form.get('lname') 
        bio=request.form.get('bio')
        
        
        file = request.files['profile_image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(file_folder, filename))
        
        profile_image=filename
        age=request.form.get('age')
        gender=request.form.get('gender')
        user =UserProfile(id=uid,profile_creation=creation,first_name=fname,
        last_name=lname,bio=bio,imagename=profile_image,age=age,gender=gender)
        db.session.add(user)
        db.session.commit()
  
        flash("Information accepted")
        return redirect(url_for('home'))
    return render_template('profile.html')
    
@app.route('/profiles',methods=['GET','POST'])
def profiles():
    """Render the website's profiles page."""
    users =[]
    query='SELECT first_name,id FROM user_profile;'
    entries=db.session.execute(query)
    for entry in entries: 
        uname,uid =entry[0],entry[1]
        users+=[{"username":uname,"userid":uid}]
        results ={"users":users}
    response =app.response_class(response=json.dumps(results),status=200, mimetype='application/json' )
    return response

@app.route('/profile/<userid>',methods=['GET','POST'])
def profile_id(userid):
    """Render the website's unique profile page."""
    query="SELECT id,first_name,imagename,gender,age,profile_creation FROM user_profile WHERE id={0};".format(userid)
    profile_info=db.session.execute(query)
    for user in profile_info: 
        uid,uname,profile_pic,gender,age,created_on =user[0],user[1],user[2],user[3],user[4],user[5]
        results={"userid":uid,"username":uname, "image":profile_pic,
        "gender": gender, "age": age, "profile_created_on":created_on } 
    response =app.response_class(response=json.dumps(results),status=200, mimetype='application/json' )
    return response
    

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
