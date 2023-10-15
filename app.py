from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder="template")

@app.route('/get_array', methods=['GET', 'POST'])
def get_array():
    if request.method == 'POST':
        data = request.json
        print(data)
        return jsonify(result="Data received successfully")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
