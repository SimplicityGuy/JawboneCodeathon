from force import app
from force.notes import notes_app
from force.auth import auth_flask_login

# Register Blueprints
app.register_blueprint(notes_app)
app.register_blueprint(auth_flask_login)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
