from app import db

class NamedDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"NamedDay(name='{self.name}', date='{self.date}')"
