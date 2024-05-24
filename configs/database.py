from databases import Database

username = 'root'
password = ''
host = 'localhost'
dbname = 'jxnu_teach_platform'
charset = 'utf8mb4'

# 数据库连接信息
DATABASE_URL = f"mysql://{username}:{password}@{host}/{dbname}?charset={charset}"

database = Database(DATABASE_URL)
