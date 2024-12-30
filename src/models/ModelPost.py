from datetime import datetime

class ModelPost:
    @classmethod
    def create_post(cls, db, post):
        try:
            cursor = db.connection.cursor()
            sql = """
                INSERT INTO posts (username, title, photo_path, description, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (post.username, post.title, post.photo_path, post.description, datetime.now()))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(f"Error during post creation: {ex}")