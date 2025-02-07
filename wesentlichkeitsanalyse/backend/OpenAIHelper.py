

import openai
import yaml
from multipart import file_path


class OpenAIHelper:
    def __init__(self):
        """
        Initialisiert die OpenAI-Hilfsklasse mit dem API-Schlüssel aus der Konfigurationsdatei.

        Args:
            config_path (str): Der Pfad zur Konfigurationsdatei.
        """


    def get_openai_response(self, system_role: str, user_input: str, model: str = "gpt-3.5-turbo") -> dict:
      with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\conf.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        openai.api_key = config["api_key"]


        # Nachrichtenstruktur erstellen
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": user_input}
        ]

        # Anfrage an die OpenAI-API senden
        response = openai.chat.completions.create(
            model=model,
            messages=messages
        )
      return response.choices[0].message.content









