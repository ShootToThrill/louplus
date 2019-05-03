import os,json

from flask import Flask,render_template,abort

app = Flask(__name__)
app.config['TEMPLATE_AUTO_RELOAD'] = True

def load_jsonfile(path):
	with open(path.get('path'),'r') as f:
		data = json.loads(f.read())
	data['name'] = path.get('name')
	return data

def getfiles_path():
	files = os.path.join(os.getcwd(),'files')
	files_path = [ {'path':os.path.join(files,f),'name':f} for f in os.listdir(files) if os.path.isfile(os.path.join(files,f))]
	return files_path

@app.errorhandler(404)
def notfound(err):
	return render_template('404.html'),404

@app.route('/')
def index():
	files_path = getfiles_path()
	files_data = [ load_jsonfile(p) for p in files_path  ]
	return render_template('index.html',data=files_data)

@app.route('/files/<filename>')
def file(filename):
	file_path = os.path.join(os.getcwd(),'files',filename+'.json')
	

	if not filename or not os.path.isfile(file_path):
		abort(404)

	data = load_jsonfile({'path':file_path}) 
	print(data)
	if not data:
		abort(404)

	return render_template('file.html',data=data)


if __name__ == '__main__':
	app.run()