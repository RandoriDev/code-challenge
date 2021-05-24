from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():  # Display index.html as default
    if request.method == 'POST':
        received_post = request.form['text_field']
        return render_template('index.html', received_post=received_post)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()