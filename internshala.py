from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests
import pandas as pd

app = Flask(__name__)

def course_review(query):
    internshala = "https://trainings.internshala.com/" + query
    urlclient = uReq(internshala)
    internshala_page = urlclient.read()
    beautify = bs(internshala_page,'html.parser')
    bigBox = beautify.findAll('div',{"class":"feedbacks-card-container h-100"})
    names = []
    for i in bigBox:
        names.append(i.div.findAll('div',{"class":"name"})[0].text)
    ratings = []
    for i in bigBox:
        ratings.append(i.div.findAll('span',{"class":"rating"})[0].text)
    review = []
    for i in bigBox:
        review.append(i.div.findAll('p',{"class":"feedback-body"})[0].text)
    institutes = []
    for i in bigBox:
        institutes.append(i.div.findAll('p',{"class":"institute"})[0].text)
    project_box = beautify.findAll('div',{"class":"project-card"})
    project_names = []
    for i in project_box:
        project_names.append(i.div.findAll('h4',{"class":"title"})[0].text)
    project_desc = []
    for i in project_box:
        project_desc.append((i.findAll('p',{"class":"description"})[0].text).replace("\n","").replace("\r",""))
    return names,institutes,ratings,review,project_names,project_desc
    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit",methods=['POST'])
def submit():
    query = request.form['content']
    data = {}
    names,institutes,ratings,review,project_names,project_desc = course_review(query)
    data = pd.DataFrame({
    "Name": names,
    "Institute": institutes,
    "Rating": ratings,
    "Review": review
})

    csv_file = 'data.csv'
    data.to_csv(csv_file, index=False)
    
    return render_template("index.html",names = names,institutes=institutes,ratings = ratings,review=review)

if __name__ == "__main__":
    app.run(debug=True)