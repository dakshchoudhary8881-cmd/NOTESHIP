document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const chatContainer = document.getElementById('chat-container')
  const chatForm = document.getElementById('chat-form')
  const userInput = document.getElementById('user-input')
  const sendBtn = document.getElementById('send-btn')
  const chipsContainer = document.getElementById('chips-container')

  // State
  let isWaitingForResponse = false

  // --- Core Logic ---

  // Auto-resize textarea
  userInput.addEventListener('input', () => {
    userInput.style.height = 'auto'
    userInput.style.height = userInput.scrollHeight + 'px'
    // Limit max height check handled by CSS max-height
  })

  // Handle form submission
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    const message = userInput.value.trim()
    if (!message || isWaitingForResponse) return

    // UI Updates
    appendMessage('user', message)
    userInput.value = ''
    userInput.style.height = 'auto'
    setLoading(true)

    try {
      await fetchAIResponse(message)
    } catch (error) {
      handleError(error)
    } finally {
      setLoading(false)
      userInput.focus()
    }
  })

  // Handle 'Enter' key to submit (Shift+Enter for new line)
  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      chatForm.dispatchEvent(new Event('submit'))
    }
  })

  // Handle suggestion chips
  chipsContainer.addEventListener('click', (e) => {
    const chip = e.target.closest('.chip')
    if (!chip) return

    const query = chip.dataset.query
    if (query) {
      userInput.value = query
      chatForm.dispatchEvent(new Event('submit'))
    }
  })

  // --- API Interaction ---

  async function fetchAIResponse(prompt) {
    // Create typing indicator bubble
    const typingBubbleId = 'typing-' + Date.now()
    appendTypingIndicator(typingBubbleId)
    scrollToBottom()

    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: prompt }),
      })

      if (!response.ok) {
        if (response.status === 503) throw new Error('Service Unavailable')
        throw new Error(`Server Error: ${response.status}`)
      }

      const data = await response.json()

      // Remove typing indicator
      removeElement(typingBubbleId)

      if (data.status === 'success') {
        appendMessage('bot', data.reply)
      } else {
        throw new Error(data.message || 'Unknown error')
      }
    } catch (error) {
      removeElement(typingBubbleId)
      throw error // Propagate to caller
    }
  }

  // --- UI Helpers ---

  function appendMessage(sender, text) {
    const messageDiv = document.createElement('div')
    messageDiv.className = `message ${sender}-message`

    const avatarIcon = sender === 'user' ? 'person' : 'smart_toy'

    // Process text (Sanitize & Markdown)
    const processedContent =
      sender === 'bot'
        ? parseMarkdown(text)
        : escapeHtml(text).replace(/\n/g, '<br>')

    messageDiv.innerHTML = `
            <div class="avatar">
                <span class="material-symbols-rounded">${avatarIcon}</span>
            </div>
            <div class="message-content">
                ${processedContent}
                ${sender === 'bot' ? '<button class="copy-btn" title="Copy"><span class="material-symbols-rounded" style="font-size:16px">content_copy</span></button>' : ''}
            </div>
        `

    chatContainer.appendChild(messageDiv)
    scrollToBottom()

    // Add copy event listener if bot
    if (sender === 'bot') {
      const copyBtn = messageDiv.querySelector('.copy-btn')
      copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(text).then(() => {
          const icon = copyBtn.querySelector('span')
          icon.textContent = 'check'
          setTimeout(() => (icon.textContent = 'content_copy'), 2000)
        })
      })
    }
  }

  function appendTypingIndicator(id) {
    const div = document.createElement('div')
    div.id = id
    div.className = 'message bot-message'
    div.innerHTML = `
            <div class="avatar">
                <span class="material-symbols-rounded">smart_toy</span>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `
    chatContainer.appendChild(div)
  }

  function handleError(error) {
    const errorDiv = document.createElement('div')
    errorDiv.className = 'message bot-message'
    errorDiv.innerHTML = `
            <div class="avatar" style="background-color: #ef4444; color: white;">
                <span class="material-symbols-rounded">error</span>
            </div>
            <div class="message-content" style="border-color: #ef4444; color: #fca5a5;">
                <strong>Error:</strong> ${error.message || 'Something went wrong. Please try again.'}
            </div>
        `
    chatContainer.appendChild(errorDiv)
    scrollToBottom()
  }

  function removeElement(id) {
    const el = document.getElementById(id)
    if (el) el.remove()
  }

  function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight
  }

  function setLoading(isLoading) {
    isWaitingForResponse = isLoading
    sendBtn.disabled = isLoading
    userInput.disabled = isLoading
    if (!isLoading) {
      userInput.focus()
    }
  }

  // --- Utilities ---

  function escapeHtml(text) {
    if (!text) return ''
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;')
  }

  function parseMarkdown(text) {
    let safeText = escapeHtml(text)

    // Bold: **text**
    safeText = safeText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')

    // Italic: *text*
    safeText = safeText.replace(/\*(.*?)\*/g, '<em>$1</em>')

    // Code Block: ```code```
    safeText = safeText.replace(
      /```([\s\S]*?)```/g,
      '<pre><code>$1</code></pre>',
    )

    // Inline Code: `code`
    safeText = safeText.replace(/`(.*?)`/g, '<code>$1</code>')

    // Unordered Lists: - item (must be at start of line)
    // Fix: Replace newline + dash with <li>
    safeText = safeText.replace(/^\s*-\s+(.*)$/gm, '<li>$1</li>')

    // Wrap adjacent <li> in <ul> (Simplistic approach)
    // This is a simple regex capability, strictly vanilla logic
    // We will just wrap the whole thing if it contains <li> to ensure basic lists work,
    // or just accept standalone <li> styling in CSS (which we did).
    // A better approach without a parser is to just let <li> exist and style them.

    // Convert newlines to <br> if not inside pre/ul
    safeText = safeText.replace(/\n/g, '<br>')

    return safeText
  }
})
