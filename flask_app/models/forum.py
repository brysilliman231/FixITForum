from flask_app.config.mysqlconnection import connectToMySQL

class Forum:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # make sure to not forget if more fields are added as the project progresses

    @classmethod
    def get_all_forums(cls):
        query = "SELECT * FROM forums;"
        results = connectToMySQL('fixit').query_db(query)
        forums = []
        for forum in results:
            forums.append(cls(forum))
        return forums

    @classmethod
    def save(cls, data):
        query = "INSERT INTO forums (title, description, user_id, created_at, updated_at) VALUES (%(title)s, %(description)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('fixit').query_db(query, data)
    # Additional class methods as needed for updating, deleting, etc.


    @classmethod
    def get_all_forums_with_creators(cls):
        query = """
        SELECT forums.*, users.first_name, users.last_name FROM forums
        JOIN users ON forums.user_id = users.id;
        """
        results = connectToMySQL('your_db_name').query_db(query)
        forums_with_creators = []
        for row in results:
            forum_data = {
                "id": row['id'],
                "title": row['title'],
                "description": row['description'],
                "user_id": row['user_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
                "creator_first_name": row['first_name'],  # User's first name
                "creator_last_name": row['last_name']     # User's last name
            }
            forums_with_creators.append(cls(forum_data))
        return forums_with_creators