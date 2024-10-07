import app

# Since path inspects the view and its route,
# we need to be in a Flask request context
with app.app.test_request_context():
    app.spec.path(view=app.get_permissions)
# We're good to go! Save this to a file for now.
with open('swagger.yaml', 'w') as f:
    f.write(app.spec.to_yaml())