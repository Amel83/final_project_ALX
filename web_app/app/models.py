from app import db

class NamedDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    def __repr__(self):
        return f"NamedDay(name='{self.name}', date='{self.date}')"
