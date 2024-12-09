from flask import request, jsonify
from .models import Country, User, db


def register_routes(app):
    @app.route('/api/ping', methods=['GET'])
    def ping():
        return jsonify({"status": "ok"}), 200

    @app.route('/api/countries', methods=['GET'])
    def get_countries():
        countries = Country.query.all()
        return jsonify([{"id": country.id, "name": country.name, "code": country.code} for country in countries]), 200

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

        # Check if country exists
        country = Country.query.filter_by(code=country_code.upper()).first()
        if not country:
            return jsonify({"error": "Invalid country code"}), 400

        # Check if user already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return jsonify({"error": "User already exists"}), 400

        # Create new user
        new_user = User(username=username, email=email, country=country)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201
