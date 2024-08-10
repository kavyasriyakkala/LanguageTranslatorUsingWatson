document.addEventListener('DOMContentLoaded', function () {
    const textToTranslateInput = document.getElementById('textToTranslate');
    const fromLanguageSelect = document.getElementById('fromLanguage');
    const toLanguageSelect = document.getElementById('toLanguage');
    const translateButton = document.getElementById('translateButton');
    const translationResult = document.getElementById('translationResult');
    const pronunciationAudio = document.getElementById('pronunciation');


    translateButton.addEventListener('click', function () {
        const textToTranslate = textToTranslateInput.value;
        const fromLanguage = fromLanguageSelect.value;
        const toLanguage = toLanguageSelect.value;

        // Make a POST request to the server to translate the text
        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: textToTranslate,
                from_language: fromLanguage,
                to_language: toLanguage,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            translationResult.textContent = data.translation;

            pronunciationAudio.src = data.pronunciation_url;
            pronunciationAudio.load(); // Load the new audio source

            pronunciationAudio.play();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
