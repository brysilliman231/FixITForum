from flask_app.config.mysqlconnection import connectToMySQL

class Forum:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Assume there are other attributes as needed

    @classmethod
    def get_all_forums(cls):
        query = "SELECT * FROM forums;"
        results = connectToMySQL('your_db_name').query_db(query)
        forums = []
        for forum in results:
            forums.append(cls(forum))
        return forums

    @classmethod
    def save(cls, data):
        query = "INSERT INTO forums (title, description, created_at, updated_at) VALUES (%(title)s, %(description)s, NOW(), NOW());"
        return connectToMySQL('your_db_name').query_db(query, data)
    
    # Additional class methods as needed for updating, deleting, etc.