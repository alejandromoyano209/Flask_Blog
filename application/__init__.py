from flask import Flask
import os



def init_app():
	"""Initialize the core application."""
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'database.db'))

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass



	#### Include our Flask Login System
	from flask_login import LoginManager, UserMixin
	login_manager = LoginManager()
	login_manager.login_view = "auth_bp.login"
	login_manager.init_app(app)


	# Import User model.
	from .models import User


	# User loader (FlaskLogin Extension to load users between pages)
	from application.db import get_db
	@login_manager.user_loader
	def load_user(user_id):
		conn = get_db()
		curs = conn.cursor()
		curs.execute("SELECT * from login_usuario where id = (?)",[user_id])
		lu = curs.fetchone()
		if lu is None:
			return None
		else:
			return User(int(lu[0]), lu[1], lu[2])



	with app.app_context():

		# Include our routes
		from . import routes

		# Register Blueprints
		app.register_blueprint(routes.blog_bp)
		app.register_blueprint(routes.auth_bp)

		# Import and call DB functions
		from . import db
		db.init_app(app)


		return app