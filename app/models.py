from app import db


class User(db.Model):
    # Dummy token_v2
    dummy_token_v2 = 'a08d5b0a9c758029ce4178b82cb142b0b778f04fb1971c3e8bc8f1b314c1d2b1b3636a874287baccfddd57dbf4912cdb47d62c493bbb067bcbdb0e72a3fd890a4469752808122bc650c6033ab563'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    token_v2 = db.Column(db.String(156), nullable=False,
                         default=dummy_token_v2)
    password = db.Column(db.String(60), nullable=False)
    highlights = db.relationship('Highlight', backref='curator', lazy=True)

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}')"


class Highlight(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30))
    highlight = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Highlight ('{self.id}', '{self.title}, '{self.author}')"
