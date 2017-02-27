import os
import os.path as op

PROJECT_DIR = op.dirname(__file__)
database_dir = op.join(PROJECT_DIR, 'data')
os.makedirs(database_dir, exist_ok=True)

DATABASE_URI = 'sqlite:///%s/data.sqlite' % database_dir
