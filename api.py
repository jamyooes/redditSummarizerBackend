import comparison
import scraper
import summarizer
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
data = {"message" : "Sample Test"}

# Post endpoint - Recieve reddit URL
# Send summarized data back to frontend
@app.route('/api/get-url', methods = ['POST'])
def post_data():
    incoming_data = request.json
    url = incoming_data['url']
    scraped_text = scraper.scrape_reddit(url)
    summarized_text_list = summarizer.summarizer_pipeline(scraped_text)
    summary_comparison = comparison.compare_summaries(scraped_text, summarized_text_list)
    print(summary_comparison)
    print("summary")
    print("-" * 40)
    for i in summarized_text_list:
        print (i)
        print("-" * 40)
    # print("Recieved URL: ", incoming_data)
    
    # Update the summaries or whatever we're sending in the response
    response = {"message": "URL recieved successfully", "recieved_data" : incoming_data}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug = True)