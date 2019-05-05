from app import *
db.create_all()
# ?? MySQL ????
java = Category(name='Java')
python = Category(name='Python')
file1 = File(title='Hello Java', create_time=datetime.utcnow(), category=java, content='File Content - Java is cool!')
file2 = File(title='Hello Python', create_time=datetime.utcnow(), category=python, content='File Content - Python is cool!')
db.session.add(java)
db.session.add(python)
db.session.add(file1)
db.session.add(file2)
db.session.commit()

# ?? MongoDB ????
file1.add_tag('tech')
file1.add_tag('java')
file1.add_tag('linux')
file2.add_tag('tech')
file2.add_tag('python')