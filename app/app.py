from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask import Flask, abort, request, make_response, jsonify
from waitress import serve
from http import client
from pprint import pprint
import json
import ssl
import base64
import requests
ssl._create_default_https_context = ssl._create_unverified_context


class DemoParameter(Schema):
    owner = fields.Str()
    repo = fields.Str()
    username = fields.Str()


class UserSchema(Schema):
    avatar_url = fields.Str()
    events_url = fields.Str()
    followers_url = fields.Str()
    following_url = fields.Str()
    gists_url = fields.Str()
    gravatar_id = fields.Str()
    html_url = fields.Str()
    id = fields.Int()
    login = fields.Str()
    node_id = fields.Str()
    organizations_url = fields.Str()
    permissions = fields.Dict()
    permissions.admin = fields.Bool()
    permissions.maintain = fields.Bool()
    permissions.pull = fields.Bool()
    permissions.push = fields.Bool()
    permissions.triage = fields.Bool()
    received_events_url = fields.Str()
    repos_url = fields.Str()
    role_name = fields.Str()
    site_admin = fields.Bool()
    starred_url = fields.Str()
    subscriptions_url = fields.Str()
    type = fields.Str()
    url = fields.Str()

class PermsSchema(Schema):
    permission = fields.Str()
    role_name = fields.Str()
    user = fields.Nested(UserSchema)


spec = APISpec(
    title="Simple WebService API",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(
        description="Simple WebService API",
        version="1.0.0-oas3",
        license=dict(
            name="Apache 2.0",
            url='http://www.apache.org/licenses/LICENSE-2.0.html'
            )
        ),
    servers=[
        dict(
            description="Simple WebService",
            url="http://localhost:8080"
            )
        ],
    tags=[
        dict(
            name="Demo",
            description="Endpoints related to Demo"
            )
        ],
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("Perms", schema=PermsSchema)

# Extensions initialization
# =========================
app = Flask(__name__)

@app.route("/repository/<owner>/<repo>/collaborators/<username>/permission", methods=["GET"])
def get_permissions(owner, repo, username):
    """Gist detail view.
    ---
    get:
      parameters:
      - in: path
        schema: DemoParameter
      responses:
        404:
          description: Resource not found
          content:
            application/json:
                schema: 
                    title: Basic Error
                    description: Basic Error
                    type: object
                    properties:
                        message:
                            type: string
                        documentation_url:
                            type: string
                        url:
                            type: string
                        status:
                            type: string
        200:
          description: Get the permission of a collaborator in a repository
          content:
            application/json:
                schema: Perms
    """

    cli_headers = request.headers
    authorization_header = cli_headers.get('Authorization')

    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/collaborators/{username}', headers={'authorization': authorization_header})

    if response.status_code == 404:
        return response.json(), response.status_code

    response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/collaborators/{username}/permission', headers={'authorization': authorization_header})

    return response.json(), response.status_code


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8080)

# # Since path inspects the view and its route,
# # we need to be in a Flask request context
# with app.test_request_context():
#     spec.path(view=get_permissions)
# # We're good to go! Save this to a file for now.
# with open('swagger.yaml', 'w') as f:
#     f.write(spec.to_yaml())