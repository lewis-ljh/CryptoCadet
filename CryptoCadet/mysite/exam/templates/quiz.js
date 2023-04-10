const quizForm = document.getElementById('quiz-form');
const resultsDiv = document.getElementById('results');

const correctAnswers = ['a', 'c', 'b', 'b', 'a','c','c','b'];

quizForm.addEventListener('submit', (event) => {
  event.preventDefault();
  
  let score = 0;
  const userAnswers = [quizForm.q1.value, quizForm.q2.value, quizForm.q3.value, quizForm.q4.value, quizForm.q5.value];
  
  userAnswers.forEach((answer, index) => {
    if (answer === correctAnswers[index]) {
      score += 1;
    }
  });
  
  resultsDiv.innerHTML = `<h2>Your Score: ${score}/${correctAnswers.length}</h2>`;
});