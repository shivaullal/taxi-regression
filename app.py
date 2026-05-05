from flask import Flask, render_template, request, redirect, session, url_for, flash
import numpy as np
import pickle
from supabase_config import supabase
from hashlib import sha256

app = Flask(__name__)
app.secret_key = '4321'

with open("Taxi.pkl", "rb") as f:
    model = pickle.load(f)
  
# def hash_password(password):
#     return sha256(password.encode()).hexdigest()    

@app.route("/")
def index():
    # if "user_id" not in session:
    #     return redirect(url_for("login"))
    
    return render_template("index.html")

# --- NEW ROUTE ADDED HERE ---
@app.route("/about")
def about():
    # Do NOT check for "user_id" in session here 
    # if you want the public to see your model accuracy.
    return render_template("about.html")

# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         existing = supabase.table("users").select("*").eq("email", email).execute()
#         if existing.data:
#             flash("Email already exists", "error")
#             return redirect(url_for("register"))
#         hashed_password = hash_password(password)
#         supabase.table("users").insert({
#             "uname": name,
#             "email": email,
#             "password": hashed_password
#         }).execute()
#         flash("Registered successfully", "success")
#         return redirect(url_for("index"))
#     return render_template("register.html")

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")
#         response = supabase.table("users").select("*").eq("email", email).execute()
#         user = None
#         if response.data:
#             user = response.data[0]

#             if user and hash_password(password) == user["password"]:
#                 session['user_id'] = user["u_id"]
#                 session['username'] = user["uname"]
#                 session['email'] = user["email"]

#                 flash("Login successful", "success")
#                 return redirect(url_for("index"))
#             else:
#                 flash("Invalid email or password", "error")
#                 return redirect(url_for("login"))
#     return render_template('login.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            distance = float(request.form.get("distance"))
            time_of_day = int(request.form.get("time_of_day"))  
            day_of_week = int(request.form.get("day_of_week"))  
            passengers = float(request.form.get("passengers"))
            traffic = int(request.form.get("traffic"))       
            weather = int(request.form.get("weather"))        
            base_fare = float(request.form.get("base_fare"))
            per_km = float(request.form.get("per_km"))
            per_min = float(request.form.get("per_min"))
            duration = float(request.form.get("duration"))

            features = np.array([[
                distance, time_of_day, day_of_week, passengers, 
                traffic, weather, base_fare, per_km, per_min, duration
            ]])

            prediction = model.predict(features)
            return render_template("predict.html", prediction=round(prediction[0], 2))
        
        except Exception as e:
            return f"Error in prediction: {str(e)}"

    return render_template("predict.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=7000,host='0.0.0.0')