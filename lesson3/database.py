
"""ТЕХНИЧЕСКИЙ ФАЙЛ ДЛЯ ЭКСПЕРИМЕНТОВ"""

from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
import models
import sqlalchemy as db

engine = create_engine('sqlite:///gb_blog.db')
models.Base.metadata.create_all(bind=engine)
SessionMaker = sessionmaker(bind=engine)

# def get_db():
#     db =SessionMaker()
#     try:
#         yield db
#     finally:
#         db.close()


if __name__ == '__main__':
    db = SessionMaker()
    print(1)

    # a = db.execute("select * from author").scalar()
    # db.execute
    # a = select(['author']).where(author.columns.url == 'https://geekbrains.ru/users/3899893')

    select_stmt = select([Author])
    print(conn.execute(select_stmt).fetchall())

author = models.Writer(name='Writer 1', url='sdfsdgsgsdgwer23')
# tags = models.Tag(name='привет', url='sdfsdgsgsdgwer23')
# tags_posts = models.Base
 post = models.Post(url='sdfsdgsgsdgwer23', img_url='sdfsdfsdf', writer=author)
db.add(post)
# db.add(author)
# db.commit()
print(1)
# db.select([author]).where(author.columns.url == 'https://geekbrains.ru/users/3899893')
# query = db.select([author])
# ResultProxy = connection.execute(query)
# ResultSet = ResultProxy.fetchall()
db.close()