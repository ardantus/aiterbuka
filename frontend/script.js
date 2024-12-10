document.getElementById('send').addEventListener('click', async () => {
    const prompt = document.getElementById('prompt').value;
    const chatBox = document.getElementById('chat-box');

    // Validasi input
    if (!prompt.trim()) {
        alert("Please enter a message!");
        return;
    }

    // Tambahkan pesan pengguna ke chat box segera
    chatBox.innerHTML += `<p><b>You:</b> ${prompt}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll ke bawah otomatis

    // Bersihkan input sebelum mengirim permintaan
    document.getElementById('prompt').value = "";

    try {
        // Tampilkan placeholder sementara
        chatBox.innerHTML += `<p><b>AI:</b> <span class="typing-indicator">...</span></p>`;
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll ke bawah otomatis

        // Kirim permintaan ke backend
        const response = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt })
        });

        // Hapus placeholder setelah respons diterima
        const typingIndicator = document.querySelector(".typing-indicator");
        if (typingIndicator) typingIndicator.parentElement.remove();

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Tambahkan respons AI ke chat box sebagai elemen HTML
        chatBox.innerHTML += `<div><b>AI:</b> ${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error("Error:", error);
        chatBox.innerHTML += `<p><b>AI:</b> <span style="color: red;">An error occurred while processing your request.</span></p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
        alert("An error occurred while sending your message. Please check the console for details.");
    }
});
