app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'Message is required'}), 400
    
    # #streaming the output 
    # chain = rag_chain.pick('answer')
    # for chunk in chain.stream({'input': 'what is decomposition?'}):
    #     print(chunk, end= " ")
        
    result = app.invoke({"input": user_input}, config=config, stream_mode="values" )
    
    return jsonify({'response': result['answer']})

if __name__ == '__main__':
    app.run(debug=True)