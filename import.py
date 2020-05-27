import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL")) # database engine object from SQLAlchemy that manages connections to the database
                                                    # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))
db.execute("CREATE TABLE books (idnumber VARCHAR PRIMARY KEY, title VARCHAR, author VARCHAR, years INTEGER)") 
f = open("books.csv")
g = csv.reader(f)
temp = True
for no, title, author, yea in g:
    if temp:
        temp = False
        continue
    db.execute('INSERT INTO books (idnumber, title, author, years) VALUES (:no, :title, :author, :years)', {"no": no, "title":title, "author": author,"years": yea})
db.commit()
