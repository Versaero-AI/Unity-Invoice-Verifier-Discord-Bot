import unittest
import asyncio
from src.database.db_handler import is_invoice_verified, store_verified_invoice
from src.utils.api_client import verify_invoice

class TestVerification(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_verify_invoice(self):
        # Mock API call to Unity Asset Store
        pass

    def test_database_operations(self):
        async def test_db():
            await store_verified_invoice("12345", 67890)
            result = await is_invoice_verified("12345")
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 67890)

        self.loop.run_until_complete(test_db())

if __name__ == '__main__':
    unittest.main()