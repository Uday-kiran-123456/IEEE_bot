from flask import Flask, request, jsonify, render_template
from br import br

app = Flask(__name__)
chatbot = br()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chatbot.gmodel.process(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
