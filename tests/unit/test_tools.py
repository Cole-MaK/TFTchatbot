import unittest
from unittest.mock import patch, mock_open
from src.tools import Tool

class TestChampionInfo(unittest.TestCase):
    @patch("json.load")
    @patch("builtins.open", new_callable=mock_open)
    def test_get_champion_info_zyra(self, mock_open_fn, mock_json_load):
        mock_json_load.return_value = {
            "Zyra": {
                "cost": "1 gold",
                "traits": "Street Demon, Techie",
                "passive": "None",
                "ability": "Vine description..."
            }
        }

        result = Tool.champion_info("Zyra")

        expected = {
            "cost": "1 gold",
            "traits": "Street Demon, Techie",
            "passive": "None",
            "ability": "Vine description..."
        }

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
