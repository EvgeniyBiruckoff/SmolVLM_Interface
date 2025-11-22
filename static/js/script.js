document.addEventListener('DOMContentLoaded', function() {
    const describeForm = document.getElementById('describe-form');
    describeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        fetchDescribeImage();
    });

    const questionForm = document.getElementById('question-form');
    questionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const prompt = document.getElementById('right-prompt').value;
        if (prompt) {
            fetchAskQuestion(prompt);
        }
    });
    const set_image_form = document.getElementById('upload-form')
    set_image_form.addEventListener('submit', function(e) {
        e.preventDefault();
        const url = document.getElementById('image-url').value;
        if (url) {
            fetchSetImage(url);
            closeUploadModal();
        } else {
            showResult('Введите URL изображения');
        }
    });

});

async function fetchDescribeImage() {
    try {
        // Передаем ссылку на сервер
        const response = await fetch(`/what_answer`);
        const data = await response.json();
        showResult(data.answer);
    } catch (error) {
        console.error('Ошибка:', error);
        showResult('Произошла ошибка при обработке запроса');
    }
}

async function fetchAskQuestion(prompt) {
    try {
        const response = await fetch(`/any_answer?prompt=${encodeURIComponent(prompt)}`);
        const data = await response.json();
        showResult(data.answer);
    } catch (error) {
        console.error('Ошибка:', error);
        showResult('Произошла ошибка при обработке запроса');
    }
}

async function fetchSetImage(link) {
    try {
        const response = await fetch(`/set_image?link=${encodeURIComponent(link)}`);
        const data = await response.json();
        showResult('Изображение успешно загружено');
    } catch (error) {
        console.error('Ошибка:', error);
        showResult('Произошла ошибка при обработке запроса');
    }
}

function showResult(result) {
    const h2Element = document.getElementById('result');
    h2Element.textContent = result;
    console.log('Результат:', result);
}

function openUploadModal() {
    document.getElementById('upload-modal').style.display = 'block';
}

function closeUploadModal() {
    document.getElementById('upload-modal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('upload-modal');
    if (event.target === modal) {
        closeUploadModal();
    }
}