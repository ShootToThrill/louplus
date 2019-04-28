import os

parent_path = os.getcwd()
common_file = {
	'name': '__init__.py',
	'type': 'file'
}


tree = [{
	'name': 'syl',
	'type': 'dir',
	'children': [{
		'name': 'A',
		'type': 'dir',
		'children':[common_file]
	},{
		'name': 'B',
		'type': 'dir',
		'children':[common_file]
	},{
		'name': 'C',
		'type': 'dir',
		'children':[common_file]
	},common_file]
}]

def create_node(path,_type):
	print(path,_type)
	if _type== 'file':
		open(path,'w').close()
	elif _type == 'dir':
		os.mkdir(path)

def gen_node(parent_path,node):
	path = os.path.join(parent_path,node['name'])
	create_node(path,node.get('type','dir'))
	if node.get('children'):
		for i in node['children']:
			gen_node(path,i)

for i in tree:
	gen_node(parent_path,i)


