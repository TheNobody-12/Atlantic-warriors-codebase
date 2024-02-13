from geopy.geocoders import Nominatim
from flask import request, session, Flask, jsonify, render_template, redirect, url_for, flash
import fileapp
import flask
import logging
import urllib
from ultralytics import YOLO
from PIL import Image
from google.cloud import storage
from fileobjects import DisplayInfo
import bcrypt
from waitress import serve
from PIL import Image
import pandas as pd
import plotly.express as px
import pandas as pd
import exifread
import sqlite3
from fractions import Fraction
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# import ultralytics

# how to load model name from .env file

model_to_load = 'Final_phase3.pt'
model = YOLO(model_to_load, task='detect')
# use geopy to get location from lat and lon
geolocator = Nominatim(user_agent="object-detection-app")

app = Flask(__name__)
_BUCKET_NAME = 'trial-sk'
CORS(app)
db_path = 'REVA.db'
# Old sqlite3 database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
#  new database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret-key'
db = SQLAlchemy(app)
# Model definitions


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    detections = db.relationship(
        'ObjectDetectionData', backref='user', lazy=True)


class ObjectDetectionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(100))
    x1 = db.Column(db.Float)
    y1 = db.Column(db.Float)
    x2 = db.Column(db.Float)
    y2 = db.Column(db.Float)
    object_type = db.Column(db.String(50))
    probability = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)


"""
#######################################################################################################################################################################333
THIS SECTION CONTAIN OBJECT DETECTION RELATED CODE
"""

# Location of the image taken fuctions


def get_image_geolocation(file):
    # Function to extract geolocation from image metadata using exifread library
    file.seek(0)
    tags = exifread.process_file(file)

    latitude_ref = tags.get("GPS GPSLatitudeRef")
    latitude = tags.get("GPS GPSLatitude")
    longitude_ref = tags.get("GPS GPSLongitudeRef")
    longitude = tags.get("GPS GPSLongitude")

    if latitude_ref and latitude and longitude_ref and longitude:
        latitude = parse_exif_gps_value(latitude)
        longitude = parse_exif_gps_value(longitude)

        # Convert the latitude and longitude from degrees, minutes, seconds to decimal degrees
        latitude_dec = convert_dms_to_dd(latitude)
        longitude_dec = convert_dms_to_dd(longitude)

        # Adjust the sign of latitude and longitude based on their reference
        if latitude_ref.values == "S":
            latitude_dec = -latitude_dec
        if longitude_ref.values == "W":
            longitude_dec = -longitude_dec

        return {"latitude": latitude_dec, "longitude": longitude_dec}
    else:
        raise ValueError("Geolocation data not found in image metadata.")


def parse_exif_gps_value(value):
    # Helper function to parse EXIF GPS coordinates in the format "[x, y, z]"
    parts = str(value).replace("[", "").replace("]", "").split(", ")
    degrees = float(parts[0])
    minutes_frac = Fraction(parts[1])
    seconds_frac = Fraction(parts[2])

    # Convert fractions to float
    minutes = minutes_frac.numerator / minutes_frac.denominator
    seconds = seconds_frac.numerator / seconds_frac.denominator

    return degrees, minutes, seconds


def convert_dms_to_dd(dms):
    # Function to convert degrees, minutes, seconds to decimal degrees
    degrees, minutes, seconds = dms
    dd = degrees + minutes / 60.0 + seconds / 3600.0
    return dd


# Array of YOLOv8 class labels
yolo_classes = ["0"]


"""

#######################################################################################################################################################################333
Service Based Function
"""


def fetch_lat_lon_from_db_1(filename):
    # connection = None  # Initialize the connection variable outside the try block

    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            user = session.get("user")
            # Fetch one of the latitudes and longitudes for the given filename from the database as per user
            query = "SELECT latitude, longitude FROM object_detection_data WHERE user_id = ? AND filename = ? LIMIT 1"
            cursor.execute(query, (user, filename))
            result = cursor.fetchone()

        return result

    except sqlite3.Error as error:
        print("Error fetching data from the database:", error)

    finally:
        if connection:
            connection.close()

    # Handle the case where an error occurred
    return None  # You might want to return an appropriate value or raise an exception here


def fetch_lat_lon_from_db():
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch unique filenames and their count from the database as per user
    user = session.get("user")
    cursor.execute(
        "SELECT filename, COUNT(filename) FROM object_detection_data WHERE user_id = ? GROUP BY filename", (user,))
    filenames_data = cursor.fetchall()

    # Fetch unique latitudes and longitudes from the database as per user
    cursor.execute(
        "SELECT latitude, longitude FROM object_detection_data WHERE user_id = ? GROUP BY latitude, longitude", (user,))
    lat_lon_data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return filenames_data, lat_lon_data


def Bubble_map(db_name):
    # get the data from the sqlite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Fetch unique filenames and their count with their unique lat and long from the database as per user
    cursor.execute("SELECT filename, COUNT(filename), latitude, longitude FROM object_detection_data WHERE user_id = ? GROUP BY filename, latitude, longitude", (session.get("user"),))
    rows = cursor.fetchall()

    # Create a dataframe from the rows
    df = pd.DataFrame(
        rows, columns=['filename', 'Plastic_count', 'latitude', 'longitude'])
    # Mapbox plot
    mapbox_fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', size='Plastic_count',
                                   color='Plastic_count', color_continuous_scale='plasma',
                                   zoom=18, mapbox_style='open-street-map')
    mapbox_fig.update_traces(hovertemplate='<b>%{text}</b><br>' +
                             'Plastic Count: %{marker.size:,}<br>' +
                             'Latitude: %{lat}<br>' +
                             'Longitude: %{lon}<br>',
                             text=df['filename'])

    # Bar plot
    bar_fig = px.bar(df, x='filename', y='Plastic_count',
                     color='Plastic_count', color_continuous_scale='plasma')
    # add filename to the hover data
    bar_fig.update_traces(hovertemplate='<b>%{text}</b><br>' +
                          'Plastic Count: %{y:,}<br>',
                          text=df['filename'])
    # line plot

    mapbox_plot_div = mapbox_fig.to_html(full_html=False)
    bar_plot_div = bar_fig.to_html(full_html=False)
    # dist_plot_div = dist_fig.to_html(full_html=False)

    return mapbox_plot_div, bar_plot_div


"""
#######################################################################################################################################################################333
THIS SECTION CONTAIN DATA BASE RELATED CODE

"""
# Function to add a user to the database


def get_user_by_email(email):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Fetch the user by email
        query = "SELECT * FROM User WHERE email = ?"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        return user

    except sqlite3.Error as error:
        print("Error fetching user by email:", error)

    finally:
        if connection:
            connection.close()

    # Handle the case where an error occurred
    return None  # You might want to return an appropriate value or raise an exception here


def add_user(email, password, name):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        connection.commit()
        return True
    except sqlite3.Error as e:
        print("Error adding user:", e)
        return False
    finally:
        if connection:
            connection.close()

# Function to add object detection data to the database


def add_object_detection_data(user_id, filename, x1, y1, x2, y2, object_type, probability, latitude, longitude):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO object_detection_data (user_id, filename, x1, y1, x2, y2, object_type, probability, latitude, longitude) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?,?)",
            (user_id, filename, x1, y1, x2, y2,
             object_type, probability, latitude, longitude)
        )
        connection.commit()
        return True
    except sqlite3.Error as e:
        print("Error adding object detection data:", e)
        return False
    finally:
        if connection:
            connection.close()

# Function to get object detection data for a user


def get_object_detection_data(user_id):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM object_detection_data WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchall()
    except sqlite3.Error as e:
        print("Error fetching object detection data:", e)
        return []
    finally:
        if connection:
            connection.close()

# Function to get a user by user_id


def get_user(user_id):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id,)
        )
        return cursor.fetchone()
    except sqlite3.Error as e:
        print("Error fetching user:", e)
        return None
    finally:
        if connection:
            connection.close()


"""

#######################################################################################################################################################################333
FLASK ROUTES
"""


# ################## Login Register Function ##############################
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Add the new user to the database
        if add_user(email, hashed_password, name):
            return redirect('/login')
        else:
            flash('Error registering user. Please try again.')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve the user from the database
        user = get_user_by_email(email)

        if user and bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'):
            session['user'] = user[0]
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user_id = session['user']
        user = get_user(user_id)

        if user:
            return render_template('index.html', user=user)
        else:
            flash('User not found')
            return redirect('/login')
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route("/")
def root():
    """
    Site main page handler function.
    :return: Content of index.html file
    """

    # with open("templates/index.html") as file:
    #     return file.read()
    return render_template("home.html")


# create different route for the database
@app.route("/database", methods=["GET"])
def database():
    """
    Handler of /database GET endpoint
    Retrieves data from the SQLite database and returns it as a JSON array
    :return: a JSON array of objects containing bounding boxes in format [[x1, y1, x2, y2, object_type, probability], ...]
    """
    # Fetch data from the database
    filenames_data, lat_lon_data = fetch_lat_lon_from_db()

    d_b = {
        "filenames": filenames_data,
        "lat_lon": lat_lon_data
    }

    return jsonify(d_b)


@app.route("/get_lat_lon/<filename>")
def get_lat_lon(filename):
    print("Received filename:", filename)
    lat_lon = fetch_lat_lon_from_db_1(filename)
    print("Latitude and Longitude:", lat_lon)
    return jsonify(lat_lon)


@app.route("/get_location/<lat>/<lon>")
def get_location(lat, lon):
    print("Received lat and lon:", lat, lon)
    location = geolocator.reverse(f"{lat}, {lon}", exactly_one=True)
    print("Location:", location)

    if location:
        location_data = {
            "address": location.address,
            "country": location.raw.get("address", {}).get("country"),
            "postcode": location.raw.get("address", {}).get("postcode")
        }
    else:
        location_data = {
            "address": "Location data not found",
            "country": "Unknown",
            "postcode": "Unknown"
        }

    return location_data

# create route to get plastic count for a filename

# Function to create the database tables


def create_database_tables():
    try:
        with app.app_context():
            db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print("Error creating database tables:", e)


create_database_tables()


@app.route("/get_plastic_count/<filename>")
def get_plastic_count(filename):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch unique filenames and their count from the database as per user
    user = session.get("user")
    cursor.execute(
        "SELECT COUNT(filename) FROM object_detection_data WHERE user_id = ? AND filename = ?", (user, filename))
    plastic_count = cursor.fetchone()[0]

    # Close the database connection
    conn.close()

    return jsonify(plastic_count)


@app.route("/db_data")
def db_data():
    # Fetch data from the database
    filenames_data, lat_lon_data = fetch_lat_lon_from_db()

    # get total number of plastic
    total_plastic = 0
    for i in range(len(filenames_data)):
        total_plastic += filenames_data[i][1]

    d_b = {
        "filenames": filenames_data,
        "lat_lon": lat_lon_data,
        "total_plastic": total_plastic
    }

    return jsonify(d_b)


@app.route("/db")
def db():
    return render_template("db.html")


@app.route("/visualize")
def bubblemap():
    mapbox, bar = Bubble_map(db_path)
    return render_template('visualize.html', mapbox_plot_div=mapbox, bar_plot_div=bar)


@app.route("/locate")
def locate():
    return render_template("locate.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/predict")
def predict():
    return render_template("predict.html")


@app.route("/login_reg")
def login_reg():
    return render_template("login.html")


@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        con = sqlite3.connect(db_path)
        user_id = session.get("user")

        di = DisplayInfo('File Upload')
        img = flask.request.files.get('my_image')
        if not img:
            di.add_error('No file uploaded.')

        # img = request.files['my_image']
        filename = img.filename

        if not filename:
            di.add_error('No file name provided.')

        if di.errors:
            return flask.render_template('predict.html', di=di)
        gcs_client = storage.Client()
        storage_bucket = gcs_client.get_bucket(_BUCKET_NAME)

        source = "static/" + filename
        img.save(source)

        results = model(source, task="detect", imgsz=2176,
                        conf=0.25)  # results list

        r = results[0]  # img1 predictions (tensor)
        # plot a BGR numpy array of predictions
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        output = "static/detected_{0}".format(filename)
        im.save(output)
        blob = storage_bucket.blob(output)
        blob.upload_from_filename(output)

        detect_path = "https://storage.googleapis.com/trial-sk/" + output

        # contain coordinates of the detected objects
        boxes = results[0].boxes.xyxy.tolist()
        probability = results[0].boxes.conf.tolist()

        # # Get geolocation from the image metadata
        geolocation = get_image_geolocation(img)
        for i in range(len(boxes)):
            x1 = boxes[i][0]
            y1 = boxes[i][1]
            x2 = boxes[i][2]
            y2 = boxes[i][3]
            object_type = "Plastic"
            c = probability[i]
            latitude = geolocation.get("latitude")
            longitude = geolocation.get("longitude")

            add_object_detection_data(
                user_id, filename, x1, y1, x2, y2, object_type, c, latitude, longitude)

        latitude = geolocation.get("latitude")
        longitude = geolocation.get("longitude")
        # return save im to static folder
        location = geolocator.reverse(
            f"{latitude}, {longitude}", exactly_one=True)

        address = location.address
        country = location.raw.get("address", {}).get("country")
        postcode = location.raw.get("address", {}).get("postcode")
        total_plastic = len(boxes)
        return render_template('predict.html', image_name=detect_path, lat=latitude, lon=longitude, address=address, country=country, postcode=postcode, total_plastic=total_plastic)

    return render_template("predict.html")


@app.route("/about")
def about():
    # redirect to about us id of  home page
    return redirect(url_for('home', _anchor='AboutUs'))


@app.route("/contact")
def contact():
    # redirect to contact us id of  home page
    return redirect(url_for('home', _anchor='Contact'))


@app.route("/team")
def team():
    # redirect to team id of  home page
    return redirect(url_for('home', _anchor='team'))


@app.route("/Services")
def Services():
    # redirect to services id of  home page
    return redirect(url_for('home', _anchor='Services'))


@app.route("/Testimonials")
def Testimonials():
    # redirect to testimonials id of  home page
    return redirect(url_for('home', _anchor='Testimonials'))


@app.route("/log_about")
def log_about():
    # redirect to about us id of  home page
    return redirect(url_for('dashboard', _anchor='AboutUs'))


@app.route("/log_contact")
def log_contact():
    # redirect to contact us id of  home page
    return redirect(url_for('dashboard', _anchor='Contact'))


@app.route("/log_team")
def log_team():
    # redirect to team id of  home page
    return redirect(url_for('dashboard', _anchor='team'))


@app.route("/log_Services")
def log_Services():
    # redirect to services id of  home page
    return redirect(url_for('dashboard', _anchor='Services'))


@app.route("/log_Testimonials")
def log_Testimonials():
    # redirect to testimonials id of  home page
    return redirect(url_for('dashboard', _anchor='Testimonials'))


if __name__ == "__main__":
    # serve(app, port=8080)
    app.run(debug=True)
