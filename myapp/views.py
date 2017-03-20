from pyramid.request import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.session import check_csrf_token
from websauna.utils.slug import slug_to_uuid
from websauna.utils.slug import uuid_to_slug
from websauna.system.core import messages
from websauna.system.http import Request
from websauna.utils.slug import slug_to_uuid
from websauna.system.core.route import simple_route
from .models import Question
from myapp.models import Choice

@simple_route("/questions/{question_uuid}", route_name="detail", renderer="myapp/detail.html")
def detail(request: Request):

    # Convert base64 encoded UUID string from request path to Python UUID object
    question_uuid = slug_to_uuid(request.matchdict["question_uuid"])

    question = request.dbsession.query(Question).filter_by(uuid=question_uuid).first()
    if not question:
        raise HTTPNotFound()

    if request.method == "POST":

        question = request.dbsession.query(Question).filter_by(uuid=question_uuid).first()
        if not question:
            raise HTTPNotFound()

        if "choice" in request.POST:
            # Extracts the form choice and turn it to UUID object
            chosen_uuid = slug_to_uuid(request.POST['choice'])
            selected_choice = question.choices.filter_by(uuid=chosen_uuid).first()
            selected_choice.votes += 1
            messages.add(request, msg="Thank you for your vote", kind="success")
            return HTTPFound(request.route_url("results", question_uuid=uuid_to_slug(question.uuid)))
        else:
            error_message = "You did not select any choice."

    return locals()


@simple_route("/questions/{question_uuid}/results", route_name="results", renderer="myapp/results.html")
def results(request: Request):

    # Convert base64 encoded UUID string from request path to Python UUID object
    question_uuid = slug_to_uuid(request.matchdict["question_uuid"])

    question = request.dbsession.query(Question).filter_by(uuid=question_uuid).first()
    if not question:
        raise HTTPNotFound()
    choices = question.choices.order_by(Choice.votes.desc())
    return locals()


@simple_route("/", route_name="home", renderer="myapp/home.html")
def home(request: Request):
    """Render the site homepage."""
    latest_question_list = request.dbsession.query(Question).order_by(Question.published_at.desc()).all()
    return locals()
