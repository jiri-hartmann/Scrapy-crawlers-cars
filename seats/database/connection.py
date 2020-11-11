import keyring
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# db settings
db_service = "MariaDB"  # name of service in Windows valet
db_user = "root"
db_name = "ades"
db_server = 'localhost'
db_password = keyring.get_password(db_service, db_user)

if not db_password:
    password = input(f'Input password to system {db_service} for user '
                     f'{db_user}: ')
    keyring.set_password(db_service, db_user, db_password)

conn_string = f"mysql+pymysql://{db_user}:{db_password}@{db_server}/{db_name}"
engine = create_engine(conn_string)

db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))