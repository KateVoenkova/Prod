import unittest
from app import create_app, db
from app.models import Country


class EndpointsTestCase(unittest.TestCase):

    def setUp(self):
        # Устанавливаем тестовый клиент и тестовую базу данных
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Добавляем тестовые данные
            test_country = Country(name="Testland", code="TL")
            db.session.add(test_country)
            db.session.commit()

    def tearDown(self):
        # Очищаем базу данных после теста
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_ping_endpoint(self):
        response = self.client.get('/api/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_get_countries(self):
        response = self.client.get('/api/countries')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]['name'], "Testland")
        self.assertEqual(response.get_json()[0]['code'], "TL")


if __name__ == "__main__":
    unittest.main()
