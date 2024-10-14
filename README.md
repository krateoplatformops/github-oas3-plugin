# GitHub API Collaborator Permission Mitigation Service

## Overview

This web service addresses an inconsistency in the GitHub API's behavior regarding collaborator permissions. Specifically, it mitigates the issue with the endpoint `https://api.github.com/repos/{owner}/{repo}/collaborators/{username}/permission`, which returns a 200 status code even if the username is no longer a collaborator (when a 404 would be expected).

### Problem Statement

The GitHub API endpoint `https://api.github.com/repos/{owner}/{repo}/collaborators/{username}/permission` returns a 200 status code regardless of whether the user is still a collaborator or not, leading to potential misinterpretation of user permissions.

### Solution

This service resolves the issue by first calling the API endpoint `https://api.github.com/repos/{owner}/{repo}/collaborators/{username}` to check if the status code is 200 (indicating the user is a collaborator). Only if this check passes does it then call `https://api.github.com/repos/{owner}/{repo}/collaborators/{username}/permission` to retrieve the actual permissions.

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
  - `200 OK`: If the user is a collaborator, returns the permission details.
  - `404 Not Found`: If the user is not a collaborator.

## OpenAPI Specification Generation

This web service leverages the `apispec` library to generate the OpenAPI Specification of the API endpoint exposed. To update the swagger.yaml file, you can run:

```sh
python app/generate_spec.py
```

## Example

To check if a user is a collaborator and get their permissions:

```sh
curl -X GET "http://localhost:5000/check_permission?owner=octocat&repo=Hello-World&username=someuser"
```

This will first verify if the user is a collaborator and then, if they are, return their permission details.