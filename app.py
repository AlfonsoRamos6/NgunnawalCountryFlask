from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(Config)  # loads the configuration for the database
db = SQLAlchemy(app)            # creates the db object using the configuration