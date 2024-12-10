import httpx
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_URL = "http://host.docker.internal:11434"

def format_response(response_text):
    """Format respons menjadi HTML dengan elemen daftar dan paragraf."""
    try:
        # Jika respons berisi daftar seperti "1. ...", ubah menjadi elemen <ol>
        if response_text.startswith("Berikut adalah") or "1." in response_text:
            items = response_text.split("1.")[1].split("  ")
            formatted = "<ol>"
            for item in items:
                if item.strip():
                    formatted += f"<li>{item.strip()}</li>"
            formatted += "</ol>"
            return formatted
        else:
            # Jika respons berupa teks biasa, bungkus dalam <p>
            return f"<p>{response_text}</p>"
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return f"<p>{response_text}</p>"

def handle_chat(prompt, model_name):
    """Panggil API Ollama tanpa streaming dengan pengaturan timeout."""
    try:
        url = f"{OLLAMA_URL}/api/chat"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        # Log permintaan ke API Ollama
        logger.info(f"Sending request to Ollama: {url}")
        logger.debug(f"Request payload: {data}")

        # Set timeout lebih panjang
        timeout = httpx.Timeout(180.0)  # 180 detik
        response = httpx.post(url, headers=headers, json=data, timeout=timeout)

        # Log status respons
        logger.info(f"Received response from Ollama with status code: {response.status_code}")

        # Raise error jika status bukan 2xx
        response.raise_for_status()

        # Parsing respons JSON
        response_data = response.json()
        if "message" in response_data and "content" in response_data["message"]:
            raw_content = response_data["message"]["content"]
            return format_response(raw_content)  # Format respons sebelum dikembalikan
        else:
            logger.error(f"Unexpected response format: {response_data}")
            return "<p>Unexpected response format from Ollama.</p>"
    except httpx.TimeoutException:
        logger.error("Timeout while contacting Ollama.")
        return "<p>Error contacting Ollama: Request timed out. Try a simpler or shorter prompt.</p>"
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return f"<p>Error contacting Ollama: {e}</p>"
    except KeyError as e:
        logger.error(f"KeyError encountered: {e}")
        return "<p>Unexpected response format from Ollama.</p>"
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return "<p>An unexpected error occurred while contacting Ollama.</p>"
