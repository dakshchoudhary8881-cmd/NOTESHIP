const chatBox = document.getElementById('chat-box')
const userInput = document.getElementById('user-input')
const sendBtn = document.getElementById('send-btn')

function addMessage(text, sender) {
  const msg = document.createElement('div')
  msg.classList.add('message', sender)
  msg.textContent = text
  chatBox.appendChild(msg)
  chatBox.scrollTop = chatBox.scrollHeight
}

async function sendMessage() {
  const message = userInput.value.trim()
  if (!message) return

  addMessage(message, 'user')
  userInput.value = ''

  // show loading bubble
  const loading = document.createElement('div')
  loading.classList.add('message', 'bot')
  loading.textContent = 'Typing...'
  chatBox.appendChild(loading)
  chatBox.scrollTop = chatBox.scrollHeight

  try {
    const response = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    })

    const data = await response.json()

    loading.remove() // remove "Typing..." bubble

    addMessage(data.reply, 'bot')
  } catch (err) {
    loading.remove()
    addMessage('Error: Could not connect to server.', 'bot')
  }
}

sendBtn.addEventListener('click', sendMessage)
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage()
})
