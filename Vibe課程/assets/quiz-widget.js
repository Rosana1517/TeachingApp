/* Quiz Widget — reusable interactive quiz component */
function checkAnswer(el, isCorrect) {
  const siblings = el.parentElement.querySelectorAll('li');
  siblings.forEach(s => {
    s.style.pointerEvents = 'none';
  });
  if (isCorrect) {
    el.classList.add('correct');
  } else {
    el.classList.add('wrong');
    siblings.forEach(s => {
      if (s.onclick && s.onclick.toString().includes('true')) {
        s.classList.add('correct');
      }
    });
  }
}

function revealAnswer(btn) {
  const answer = btn.nextElementSibling;
  if (answer.style.display === 'block') {
    answer.style.display = 'none';
    btn.textContent = '查看答案';
  } else {
    answer.style.display = 'block';
    btn.textContent = '隱藏答案';
  }
}
