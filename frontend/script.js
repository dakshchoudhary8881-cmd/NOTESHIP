const chatBox = document.getElementById('chat-box')
const userInput = document.getElementById('user-input')
const sendBtn = document.getElementById('send-btn')

// Suggestions
document.querySelectorAll('.suggestion-chip').forEach((chip) => {
  chip.addEventListener('click', () => {
    userInput.value = chip.textContent
    userInput.focus()
  })
})

async function copyToClipboard(text, btn) {
  try {
    await navigator.clipboard.writeText(text)
    const icon = btn.querySelector('span')
    const original = icon.textContent
    icon.textContent = 'check'
    setTimeout(() => (icon.textContent = original), 2000)
  } catch (err) {
    console.error('Failed to copy', err)
  }
}

// Improved Markdown Rendering
function renderMarkdown(text) {
  // Escape HTML first to prevent XSS
  const safeText = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')

  let html = safeText
    // Bold
    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
    // Italic
    .replace(/\*(.*?)\*/g, '<i>$1</i>')
    // Code Block (basic)
    .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
    // Inline Code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Headers (###)
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    // Bullet points
    .replace(/^- (.*$)/gim, '• $1')
    // Line breaks
    .replace(/\n/g, '<br>')
  return html
}

function addMessage(text, sender) {
  const wrapper = document.createElement('div')
  wrapper.classList.add('message', sender)

  // Avatar
  const avatar = document.createElement('div')
  avatar.classList.add('avatar', sender)
  // Use Material Icons
  const iconSpan = document.createElement('span')
  iconSpan.classList.add('material-symbols-rounded')
  iconSpan.textContent = sender === 'user' ? 'person' : 'smart_toy'
  avatar.appendChild(iconSpan)

  // Content
  const content = document.createElement('div')
  content.classList.add('message-content')
  content.innerHTML = renderMarkdown(text)

  if (sender === 'user') {
    wrapper.appendChild(content)
    wrapper.appendChild(avatar) // Avatar on right for user
  } else {
    wrapper.appendChild(avatar) // Avatar on left for bot
    wrapper.appendChild(content)

    // Add Copy Button for bot messages
    const copyBtn = document.createElement('button')
    copyBtn.className = 'copy-btn'
    copyBtn.innerHTML =
      '<span class="material-symbols-rounded">content_copy</span>'
    copyBtn.ariaLabel = 'Copy message'
    copyBtn.onclick = () => copyToClipboard(text, copyBtn)
    content.appendChild(copyBtn)
  }

  chatBox.appendChild(wrapper)
  scrollToBottom()
}

function addTypingIndicator() {
  const wrapper = document.createElement('div')
  wrapper.classList.add('message', 'bot')

  const avatar = document.createElement('div')
  avatar.classList.add('avatar', 'bot')
  avatar.innerHTML = '<span class="material-symbols-rounded">smart_toy</span>'

  const content = document.createElement('div')
  content.classList.add('message-content')

  const dots = document.createElement('div')
  dots.classList.add('typing-dots')
  dots.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `
  content.appendChild(dots)

  wrapper.appendChild(avatar)
  wrapper.appendChild(content)

  chatBox.appendChild(wrapper)
  scrollToBottom()
  return wrapper
}

function scrollToBottom() {
  chatBox.scrollTop = chatBox.scrollHeight
}

async function sendMessage() {
  const message = userInput.value.trim()
  if (!message) return

  addMessage(message, 'user')
  userInput.value = ''

  // Auto-focus back to input
  userInput.focus()

  const typingIndicator = addTypingIndicator()

  try {
    const res = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    })

    if (!res.ok) {
      const errorText = await res.text()
      throw new Error(`Error ${res.status}: ${errorText || res.statusText}`)
    }

    const data = await res.json()

    typingIndicator.remove()
    addMessage(data.reply, 'bot')
  } catch (err) {
    typingIndicator.remove()
    addMessage(`⚠️ ${err.message}`, 'bot')
  }
}

sendBtn.addEventListener('click', sendMessage)
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage()
})

// Initialize existing bot messages with copy buttons
document
  .querySelectorAll('.message.bot .message-content')
  .forEach((content) => {
    if (!content.querySelector('.copy-btn')) {
      const copyBtn = document.createElement('button')
      copyBtn.className = 'copy-btn'
      copyBtn.innerHTML =
        '<span class="material-symbols-rounded">content_copy</span>'
      copyBtn.ariaLabel = 'Copy message'
      // Find the text content (excluding nested elements if complex, but simple innerText is usually fine for copy)
      // For markdown rendered content, we might want the raw text or the innerText.
      // Here we just use innerText.
      const text = content.innerText
      copyBtn.onclick = () => copyToClipboard(text, copyBtn)
      content.appendChild(copyBtn)
    }
  })
