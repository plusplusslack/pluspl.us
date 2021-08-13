from flask import Blueprint, make_response, redirect, render_template, url_for
from models import Team
import markdown

views = Blueprint('views', __name__, template_folder='/template')


@views.route('/')
def index():
    return redirect(url_for('sunset'))

@views.route('/archive/<team_uuid>.csv')
def index(team_uuid):
    team = Team.query.filter_by(team_archive_url=team_uuid).first()
    response = make_response(team.archive_csv)
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@views.route('/privacy_policy')
def privacy_policy():
    with open("plusplus/content/privacy.md", "r") as f:
        text = markdown.markdown(f.read())
    return render_template("document.html", title="Privacy Policy", content=text)


@views.route('/faq')
def faq():
    with open("plusplus/content/faq.md", "r") as f:
        text = markdown.markdown(f.read())
    return render_template("document.html", title="FAQ", content=text)


@views.route('/support')
def support():
    return render_template("support.html")


@views.route('/installed')
def success():
    with open("plusplus/content/success.md", "r") as f:
        text = markdown.markdown(f.read())
    return render_template("document.html", title="Install Complete!", content=text)


@views.route('/not_installed')
def failure():
    with open("plusplus/content/fail.md", "r") as f:
        text = markdown.markdown(f.read())
    return render_template("document.html", title="Install Failed", content=text)

@views.route('/sunset')
def sunset():
    with open("plusplus/content/sunset.md", "r") as f:
        text = markdown.markdown(f.read())
    return render_template("document.html", title="Saying Goodbye to pluspl.us", content=text)
