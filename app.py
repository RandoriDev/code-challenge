from flask import Flask, render_template, request, json, abort

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():  # Display index.html as default
    if request.method == 'POST':
        received_json = json.loads(request.form['text_field'])

        if received_json['is_malicious'] == 'is_malicious':
            abort(401)  # Respond with 401 unauthorized error
        else:
            # If the is_malicious key/value is not found, return the entire JSON response to display.
            return render_template('index.html', received_post=received_json)

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()