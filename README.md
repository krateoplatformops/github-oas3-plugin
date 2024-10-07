# GitHub API Collaborator Permission Mitigation Service

This web service mitigates the behavior of the GitHub API endpoint `https://api.github.com/repos/{owner}/{repo}/collaborators/{username}/permission` which returns a 200 status code even if the username is no longer a collaborator (expected 404).

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the web service:
    ```sh
    python app.py
    ```

2. The service will be available at `http://localhost:8080`.

## API Endpoints

### Check Collaborator Permission

- **URL**: `/check_permission`
- **Method**: `GET`
- **Query Parameters**:
    - `owner` (string): The owner of the repository.
    - `repo` (string): The name of the repository.
    - `username` (string): The username to check.

- **Response**:
    - `200 OK`: If the user is a collaborator.
    - `404 Not Found`: If the user is not a collaborator.

## OpenApi Specification Generation

This webservice leverages `apispec` library to generate the OpenApi Specification of the API endpoint exposed. To update the swagger.yaml file you can run.

```sh
python app/generate_spec.py
```

## Example

To check if a user is a collaborator:

```sh
curl -X GET "http://localhost:5000/check_permission?owner=octocat&repo=Hello-World&username=someuser"