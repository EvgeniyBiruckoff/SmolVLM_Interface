document.addEventListener('DOMContentLoaded', function() {
    // Форма "Описать картинку"
    const describeForm = document.getElementById('describe-form');
    describeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const link = document.getElementById('left-link').value;
        if (link) {
            fetchDescribeImage(link);
        }
    });

    // Форма "Задать вопрос"
    const questionForm = document.getElementById('question-form');
    questionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const prompt = document.getElementById('right-prompt').value;
        const link = document.getElementById('right-link').value;
        if (prompt && link) {
            fetchAskQuestion(prompt, link);
        }
    });
});

// Функция для описания картинки
async function fetchDescribeImage(link) {
    try {
        const response = await fetch(`/what_answer?link=${encodeURIComponent(link)}`);
        const data = await response.json();
        showResult(data.answer);
    } catch (error) {
        console.error('Ошибка:', error);
        showResult('Произошла ошибка при обработке запроса');
    }
}

// Функция для вопроса о картинке
async function fetchAskQuestion(prompt, link) {
    try {
        const response = await fetch(`/any_answer?promt=${encodeURIComponent(prompt)}&link=${encodeURIComponent(link)}`);
        const data = await response.json();
        showResult(data.answer);
    } catch (error) {
        console.error('Ошибка:', error);
        showResult('Произошла ошибка при обработке запроса');
    }
}

// Функция для отображения результата (добавьте куда хотите выводить результат)
function showResult(result) {
    const h2Element = document.getElementById('result');
    h2Element.textContent = result;
    console.log('Результат:', result);
}
