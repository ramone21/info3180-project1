from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_creation = db.Column(db.DateTime)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    bio =db.Column(db.String(255))
    imagename =db.Column(db.String(80))
    age= db.Column(db.Integer)
    gender= db.Column(db.String(80))
    
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
