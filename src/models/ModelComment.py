from .entities.Comment import Comment

class ModelComment:
    @classmethod
    def add_comment(cls, db, comment):
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO comments (post_id, username, comment) VALUES (%s, %s, %s)"
            cursor.execute(sql, (comment.post_id, comment.username, comment.comment))
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(f"Error adding comment: {ex}")

    @classmethod
    def get_comments_by_post_id(cls, db, post_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, post_id, username, comment, created_at FROM comments WHERE post_id = %s ORDER BY created_at DESC"
            cursor.execute(sql, (post_id,))
            rows = cursor.fetchall()
            comments = []
            for row in rows:
                comment = Comment(row[0], row[1], row[2], row[3], row[4])
                comments.append(comment)
            return comments
        except Exception as ex:
            raise Exception(f"Error fetching comments: {ex}")