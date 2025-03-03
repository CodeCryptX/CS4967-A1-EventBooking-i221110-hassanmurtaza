from db import app
import routes  # Import routes to register API endpoints

if __name__ == "__main__":
    app.run(debug=True,port=5002)