from flask_app.config.mysqlconnection import connectToMySQL

class Forum:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
      

    @classmethod
    def get_all_forums(cls):
        try:
            return connectToMySQL('fixit').query_db("SELECT * FROM forums")
        except Exception as e:
            print(f"Error fetching forums: {e}")
            return []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO forums (title, description, user_id, created_at, updated_at) VALUES (%(title)s, %(description)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('fixit').query_db(query, data)
    


    @classmethod
    def get_all_forums_with_creators(cls):
        query = """
        SELECT forums.*, users.first_name, users.last_name FROM forums
        JOIN users ON forums.user_id = users.id;
        """
        results = connectToMySQL('fixit').query_db(query)
        forums_with_creators = []
        for row in results:
            forum_data = {
                "id": row['id'],
                "title": row['title'],
                "description": row['description'],
                "user_id": row['user_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
                "creator_first_name": row['first_name'],  
                "creator_last_name": row['last_name']     
            }
            forums_with_creators.append(cls(forum_data))
        return forums_with_creators
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM forums WHERE id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL('fixit').query_db(query, data)
        if results:
            return cls(results[0]) 
        return None
    
    @classmethod
    def get_by_key(cls, key):
        query = "SELECT * FROM forums WHERE key = %(key)s;"
        data = {'key': key}
        results = connectToMySQL('your_db_name').query_db(query, data)
        if results:
            return cls(results[0])  # Assuming the constructor can initialize from a dictionary
        return None