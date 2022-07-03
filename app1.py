from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/', methods=['GET'])
@cross_origin()
def home_page():
    return render_template("index.html")

@app.route('/review', methods=['GET', 'POST'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace(' ','')
            site_url = "https://www.flipkart.com/search?q=" + search_string
            source = requests.get(site_url)
            site_html = bs(source.text, "html.parser")
            bigboxes = site_html.findAll("div", class_="_1AtVbE col-12-12")
            del bigboxes[0:2]
            box = bigboxes[0]
            product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
            prod_res = requests.get(product_link)
            prod_res.encoding = 'utf-8'
            prod_html = bs(prod_res.text, "html.parser")
            commentboxes = prod_html.find_all('div', class_='_16PBlm')

            reviews = []
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', class_='_2sc7ZR _2V5EHH')[0].text
                except:
                    name = 'No Name'

                try:
                    rating = commentbox.div.div.div.div.text
                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentbox.div.div.div.p.text
                except:
                    commentHead = 'No comment head'

                try:
                    commentDetails = commentbox.div.div.find_all('div', class_='')[1].text
                except:
                    commentDetails = 'No comment details'
                    
                myDict = {"Product": search_string, "Name":name, "Rating": rating, "CommentHead": commentHead, "Comment": commentDetails}
                
                reviews.append(myDict)
            return render_template("results.html", reviews = reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('Exception in getting reviews, error is:', e)
            return "Something went wrong. Please check!!"
        
    else:
        return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)

