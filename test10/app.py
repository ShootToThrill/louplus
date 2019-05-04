from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/challenge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class File(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(80))
	create_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category',backref=db.backref('files', lazy=True))
	content = db.Column(db.Text)
	def __repr__(self):
		return '<File(title=%s)' % (self.title)

class Category(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80))
	def __repr__(self):
		return '<Category(name=%s)' % (self.name)


# db.create_all()

if __name__ == '__main__':
	app.run()

