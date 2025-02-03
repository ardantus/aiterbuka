# Panduan Instalasi dan Penggunaan Ollama dengan Model deepseek-r1

## 1. Download dan Instalasi Ollama

Ollama dapat diunduh sesuai dengan sistem operasi yang digunakan:

- **MacOS**: [Download Ollama untuk MacOS](https://ollama.com/download)
- **Windows**: [Download Ollama untuk Windows](https://ollama.com/download)
- **Linux**: [Download Ollama untuk Linux](https://ollama.com/download)

Setelah diunduh, lakukan instalasi sesuai dengan petunjuk yang diberikan oleh sistem operasi masing-masing.

## 2. Download Model deepseek-r1

Ollama mendukung berbagai model yang dapat diunduh dari:

- [Daftar model Ollama](https://ollama.com/search)

Untuk mendownload model **deepseek-r1**, jalankan perintah berikut di terminal atau command prompt:

```sh
ollama run deepseek-r1
```

Saat proses ini berjalan, sistem akan mengunduh model dengan ukuran sekitar **4,7GB**. Semakin besar model yang digunakan, semakin tinggi kebutuhan RAM, CPU, dan GPU.

### Hasil Download:
```sh
ollama run deepseek-r1
pulling manifest
pulling 96c415656d37... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏ 4.7 GB
pulling 369ca498f347... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏  387 B
pulling 6e4c38e1172f... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏ 1.1 KB
pulling f4d24e9138dd... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏  148 B
pulling 40fb844194b2... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▏  487 B
verifying sha256 digest
writing manifest
success
```

Untuk mengecek apakah model berhasil dijalankan, coba perintah berikut:

```sh
ollama run deepseek-r1
```

## 3. Menjalankan Ollama di Web Interface dengan Open WebUI

Agar lebih nyaman digunakan seperti ChatGPT, kita bisa menggunakan **Open WebUI**. 

### 3.1 Instalasi Open WebUI dengan Docker

Jalankan perintah berikut untuk menjalankan Open WebUI dengan Docker:

```sh
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

### 3.2 Akses Open WebUI

Setelah instalasi selesai, buka browser dan akses:

```
http://localhost:3000
```

Pilih model **deepseek-r1** yang telah diunduh sebelumnya agar dapat digunakan di browser.

Sekarang, Anda dapat menggunakan Ollama seperti ChatGPT langsung melalui web browser!

## Selesai 🎉
Sekarang Anda sudah bisa menjalankan **Ollama dengan model deepseek-r1** baik melalui terminal maupun browser dengan Open WebUI.

