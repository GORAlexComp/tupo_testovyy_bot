from threading import Thread

from flask import Flask, render_template

app = Flask('')


@app.route('/')
def home():
    project_name = "Tupo Tesovyy Bot"
    variables = "[\"BOT\", \"БОТ\"]"
    developer = "GORAlex Comp"
    github = "https://github.com/GORAlexComp/tupo_testovyy_bot"

    return render_template('index.html',
                           project_name=project_name,
                           variables=variables,
                           developer=developer,
                           github=github)


def run():
    app.run(
        host='0.0.0.0',
        port=8080
        )


def keep_alive():
    t = Thread(target=run)
    t.start()
