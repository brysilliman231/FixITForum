from flask_app.config.mysqlconnection import connectToMySQL

class Guide:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # Assume there are other attributes as needed

    @classmethod
    def get_all_guides(cls):
        query = "SELECT * FROM guides;"
        results = connectToMySQL('fixit').query_db(query)
        guides = []
        for guide in results:
            guides.append(cls(guide))
        return guides

    @classmethod
    def save(cls, data):
        query = "INSERT INTO guides (title, content, user_id, created_at, updated_at) VALUES (%(title)s, %(content)s, NOW(), NOW());"
        return connectToMySQL('fixit').query_db(query, data)
    
    # Additional class methods as needed for updating, deleting, etc.