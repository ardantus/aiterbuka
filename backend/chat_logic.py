import httpx
import logging
from database import save_chat_to_db, query_response_by_keyword  # Mengimpor sesuai dengan database.py

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_URL = "http://host.docker.internal:11434"

def format_response(response_text):
    """Format respons menjadi HTML dengan elemen daftar dan paragraf."""
    try:
        if not response_text.strip():
            return "<p>No response received from the server.</p>"

        # Jika respons berisi daftar (ciri ada "1.")
        if "1." in response_text:
            items = response_text.split("1.")[1].split("  ")
            formatted = "<ol>"
            for item in items:
                if item.strip():
                    formatted += f"<li>{item.strip()}</li>"
            formatted += "</ol>"
            return formatted
        else:
            # Jika respons berupa teks biasa, bungkus dalam <p>
            return f"<p>{response_text.strip()}</p>"
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return f"<p>{response_text.strip()}</p>"

def handle_chat(prompt, model_name):
    """
    Handle chat request by first checking the database.
    If data exists, return it; otherwise, query the AI model and save the result.
    """
    try:
        # Cek database terlebih dahulu
        logger.info("Checking database for existing response...")
        saved_response = query_response_by_keyword(prompt)
        if saved_response:
            logger.info("Response found in database.")
            return saved_response

        # Jika tidak ditemukan di database, panggil API Ollama
        logger.info("Response not found in database. Querying AI model...")
        url = f"{OLLAMA_URL}/api/chat"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        logger.debug(f"Request payload: {data}")

        # Set timeout ke 180 detik
        timeout = httpx.Timeout(180.0)
        response = httpx.post(url, headers=headers, json=data, timeout=timeout)

        # Log status respons
        logger.info(f"Received response from Ollama with status code: {response.status_code}")
        response.raise_for_status()

        # Parsing respons JSON
        response_data = response.json()
        if "message" in response_data and "content" in response_data["message"]:
            raw_content = response_data["message"]["content"]

            # Simpan hasil baru ke database
            logger.info("Saving new response to database.")
            save_chat_to_db(prompt, raw_content)

            # Kembalikan hasil yang diformat
            return format_response(raw_content)
        else:
            logger.error(f"Unexpected response format: {response_data}")
            return "<p>Unexpected response format from AI.</p>"
    except httpx.TimeoutException:
        logger.error("Timeout while contacting Ollama.")
        return "<p>Error contacting Ollama: Request timed out. Try a simpler or shorter prompt.</p>"
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return f"<p>Error contacting Ollama: {e}</p>"
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        return "<p>An unexpected error occurred while contacting Ollama.</p>"
