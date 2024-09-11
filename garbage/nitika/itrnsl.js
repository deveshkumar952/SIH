document.getElementById('translate-btn').addEventListener('click', function() {
    const imageInput = document.getElementById('image-input');
    const languageSelect = document.getElementById('language-select');
    const outputContainer = document.getElementById('output-container');
    const extractedText = document.getElementById('extracted-text');
    const translatedText = document.getElementById('translated-text');

    if (imageInput.files.length === 0) {
        alert('Please select an image.');
        return;
    }

    const file = imageInput.files[0];
    const reader = new FileReader();

    reader.onload = function(event) {
        Tesseract.recognize(
            event.target.result,
            'eng',
            {
                logger: function(m) {
                    console.log(m);
                }
            }
        ).then(({ data: { text } }) => {
            extractedText.value = text;
            outputContainer.style.display = 'block';
            translateText(text, languageSelect.value);
        });
    };

    reader.readAsDataURL(file);
});

function translateText(text, targetLanguage) {
    const translatedText = document.getElementById('translated-text');

    fetch(`https://libretranslate.de/translate`, {
        method: 'POST',
        body: JSON.stringify({
            q: text,
            source: "en",
            target: targetLanguage
        }),
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(data => {
        translatedText.value = data.translatedText;
    })
    .catch(err => {
        console.error('Translation error:', err);
        alert('There was an error translating the text.');
    });
}
