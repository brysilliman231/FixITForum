from flask_app.config.mysqlconnection import connectToMySQL

class Guide:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']  
        self.creator_first_name = data.get('first_name') 
        self.creator_last_name = data.get('last_name') 

    @classmethod
    def get_all_guides(cls):
        try:
            return connectToMySQL('fixit').query_db("SELECT * FROM guides")
        except Exception as e:
            print(f"Error fetching guides: {e}")
            return []

 
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO guides (title, content, user_id, created_at, updated_at)
        VALUES (%(title)s, %(content)s, %(user_id)s, NOW(), NOW())
        """
        return connectToMySQL('fixit').query_db(query, data)
    
    @classmethod
    def get_all_guides_with_creators(cls):
        query = """
        SELECT guides.*, users.first_name, users.last_name 
        FROM guides 
        JOIN users ON guides.user_id = users.id;
        """
        results = connectToMySQL('fixit').query_db(query)
        guides = []
        for row in results:
            guide = cls(row)
            guides.append(guide)
        return guides
    
    @classmethod
    def get_by_id(cls, id):
            query = "SELECT * FROM guides WHERE id = %(id)s;"
            data = {'id': id}
            results = connectToMySQL('fixit').query_db(query, data)
            if results:
                return cls(results[0]) 
            return None
    

    @classmethod
    def get_by_key(cls, key):
        query = "SELECT * FROM guides WHERE key = %(key)s;"
        data = {'key': key}
        results = connectToMySQL('fixit').query_db(query, data)
        if results:
            return cls(results[0])  # Assuming the constructor can initialize from a dictionary
        return None