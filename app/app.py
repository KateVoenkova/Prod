from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Замените на вашу реальную базу данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Модели базы данных
class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(3), nullable=False, unique=True)

    def __repr__(self):
        return f'<Country {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)

    country = db.relationship('Country', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'


# Маршруты
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"}), 200


@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    result = [{"id": country.id, "name": country.name, "code": country.code} for country in countries]
    return jsonify(result), 200


@app.route('/api/countries/<code>', methods=['GET'])
def get_country_by_code(code):
    country = Country.query.filter_by(code=code.upper()).first()
    if country:
        return jsonify({"id": country.id, "name": country.name, "code": country.code}), 200
    else:
        return jsonify({"error": "Country not found"}), 404


@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    country_code = data.get('country_code')

    if not all([username, email, country_code]):
        return jsonify({"error": "Missing required fields"}), 400

    # Проверяем, существует ли страна
    country = Country.query.filter_by(code=country_code.upper()).first()
    if not country:
        return jsonify({"error": "Invalid country code"}), 400

    # Проверяем, существует ли пользователь
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "User already exists"}), 400

    # Создаём нового пользователя
    new_user = User(username=username, email=email, country=country)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201


# Основной запуск
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создаёт таблицы, если их нет
    app.run(debug=True)
