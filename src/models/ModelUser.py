from .entities.User import User
from werkzeug.security import generate_password_hash

class ModelUser:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, password, fullname FROM user WHERE username=%s"
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row is not None:
                if User.check_password(row[2], user.password):
                    user = User(row[0], row[1], row[2], row[3])
                    return user
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error during login: {ex}")
        
    @classmethod
    def register(cls, db, user):
        try:
            cursor = db.connection.cursor()
            # Generar el hash con pbkdf2:sha256
            hashed_password = generate_password_hash(user.password, method='pbkdf2:sha256')
            
            sql = "INSERT INTO user (username, password, fullname) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user.username, hashed_password, user.fullname))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(f"Error during registration: {ex}")
        
    @classmethod
    def post(cls, db, user):
        try:
            cursor = db.connection.cursor()
            # Generar el hash con pbkdf2:sha256
            hashed_password = generate_password_hash(user.password, method='pbkdf2:sha256')
            
            sql = "INSERT INTO user (username, password, fullname) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user.username, hashed_password, user.fullname))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(f"Error during registration: {ex}")

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, fullname FROM user WHERE id=%s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error fetching user by ID: {ex}")
        