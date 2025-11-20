const ask = document.getElementById('ask');
ask.onclick = async () => {
  const q = document.getElementById('question').value;
  const r = await fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question: q})
  });
  const j = await r.json();
  document.getElementById('answer').textContent = j.answer;
};