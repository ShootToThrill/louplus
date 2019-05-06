from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/challenge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)
client = MongoClient('127.0.0.1',27017)
mongodb = client.challenge


class File(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(80))
	create_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category',backref=db.backref('files', lazy=True))
	content = db.Column(db.Text)
	def __repr__(self):
		return '<File(title=%s)' % (self.title)

	def add_tag(self,tag_name):
		ret = mongodb.tag.update({'name':tag_name},{"$addToSet":{'files':self.id}},True)
		return ret


	def remove_tag(self,tag_name):
		tag = mongodb.tag.find_one({
			'name': tag_name
		})

		if tag:
			tag.get('files').remove(self.id)
			mongodb.tag.save(tag)
		else:
			return {'success':0,'msg':'tag {} not exist'.format(tag_name)}

		return {'success': 1 }

	@property
	def tags(self):
		return mongodb.tag.find({'files':self.id})

class Category(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80))
	def __repr__(self):
		return '<Category(name=%s)' % (self.name)

@app.errorhandler(404)
def notfound(err):
	return render_template('404.html'), 404

@app.route('/')
def index():
	files = File.query.all()
	return render_template('index.html',files=files)

@app.route('/files/<file_id>')
def file(file_id):
	_file = File.query.filter_by(id=file_id).first()
	if not _file:
		abort(404)
	return render_template('file.html',file=_file)

if __name__ == '__main__':
	app.run()

