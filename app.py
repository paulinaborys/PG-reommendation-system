from flask import Flask

from recommendation_system.recommendation_system import RecommendationSystem


app = Flask(__name__, static_url_path='/static')

my_app = RecommendationSystem()  

@app.route('/')
def index():
    return my_app.index()
    
@app.route('/candidate_recommendation', methods=['POST'])
def candidate_recommendation():
    return my_app.candidate_recommendation()

if __name__ == '__main__':
    app.run()

    
