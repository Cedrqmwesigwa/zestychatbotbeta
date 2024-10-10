
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'Message is required'}), 400

    result = app.invoke(
        {"input": user_input},
        config=config,
    )
    return jsonify({'response': result['answer']})

if __name__ == '__main__':
    app.run(debug=True)