from flask import Blueprint, render_template
import markdown

views = Blueprint('views', __name__, template_folder='/template')


@views.route('/')
def index():
    return render_template("index.html")


@views.route('/privacy_policy')
def privacy_policy():
    with open("content/privacy.md", "r") as f:
        text = markdown.markdown(f.read())
    return render_template("document.html", title="Privacy Policy", content=text)


@views.route('/faq')
def faq():
    with open("content/faq.md", "r") as f:
        text = markdown.markdown(f.read())
    return render_template("document.html", title="FAQ", content=text)


@views.route('/support')
def support():
    return render_template("support.html")
