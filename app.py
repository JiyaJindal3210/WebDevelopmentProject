from flask import Flask,render_template
app=Flask{__name__}

@app.route("/")
def home():
    return  render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contactus.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/aboutus2")
def aboutus2():
    return render_template("aboutus2.html")

@app.route("/adoptingpets")
def adoptingpets():
    return render_template("adoptingpets.html")

@app.route("/cats")
def cats():
    return render_template("cats.html")

@app.route("/catKittenAdoption")
def catKittenAdoption():
    return render_template("catKittenAdoption.html")

@app.route("/cats")
def cats():
    return render_template("cats.html")

@app.route("/dogPuppiesAdoption")
def dogPuppiesAdoption():
    return render_template("dogPuppiesAdoption.html")

@app.route("dogs")
def dogs():
    return render_template("dogs.html")

@app.route("learnmore2.html")
def learnmore2():
    return render_template("learnmore2.html")

@app.route("learnmore3.html")
def learnmore3():
    return render_template("learnmore3.html")