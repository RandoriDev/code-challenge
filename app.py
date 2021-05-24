from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():  # Display index.html as default
    if request.method == 'POST':
        received_json = json.loads(request.form['text_field'])

        if received_json['is_malicious'] == 'is_malicious':
            return render_template('index.html', received_post=received_json, is_malicious='is_malicious')       # received_post = request.json['text_field'] )  # received_post=request.form['text_field'])
        else:
            return render_template('index.html', received_post=received_json)

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()