/**
 * Chat functionality for the Local AI Assistant.
 * This file handles chat UI interactions and communicates with the backend.
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-btn');
    const modeSelector = document.getElementById('mode-selector');
    const clearChatButton = document.getElementById('clear-chat');
    const voiceToggle = document.getElementById('voice-toggle');
    
    // State variables
    let voiceMode = false;
    
    // Initialize Socket.IO connection
    const socket = io();
    
    // Socket.IO event handlers
    socket.on('connect', function() {
        console.log('Connected to server');
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        addSystemMessage('Disconnected from server. Please refresh the page.');
    });
    
    socket.on('response', function(data) {
        // Remove typing indicator and add the response
        removeTypingIndicator();
        addAssistantMessage(data.response);
        scrollToBottom();
    });
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    clearChatButton.addEventListener('click', function() {
        chatContainer.innerHTML = '';
        addSystemMessage('Chat history cleared.');
    });
    
    voiceToggle.addEventListener('click', function() {
        voiceMode = !voiceMode;
        if (voiceMode) {
            voiceToggle.classList.remove('btn-outline-secondary');
            voiceToggle.classList.add('btn-primary');
            addSystemMessage('Voice mode enabled. Click the microphone to speak.');
            // Voice recognition will be implemented in Phase 2
        } else {
            voiceToggle.classList.remove('btn-primary');
            voiceToggle.classList.add('btn-outline-secondary');
            addSystemMessage('Voice mode disabled.');
        }
    });
    
    /**
     * Send a message to the server
     */
    function sendMessage() {
        const message = userInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addUserMessage(message);
            
            // Clear input
            userInput.value = '';
            
            // Get current mode
            const mode = modeSelector.value;
            
            // Send message to server via Socket.IO
            socket.emit('chat_message', {
                message: message,
                mode: mode
            });
            
            // Add typing indicator
            addTypingIndicator();
            
            // Scroll to bottom
            scrollToBottom();
        }
    }
    
    /**
     * Add a user message to the chat
     * @param {string} message - The message text
     */
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'user-message';
        messageDiv.textContent = message;
        chatContainer.appendChild(messageDiv);
    }
    
    /**
     * Add an assistant message to the chat
     * @param {string} message - The message text (markdown supported)
     */
    function addAssistantMessage(message) {
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = 'assistant-message';
        
        // Parse markdown in the message
        messageDiv.innerHTML = marked.parse(message);
        
        // Apply syntax highlighting to code blocks
        messageDiv.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
        
        // Add to chat
        chatContainer.appendChild(messageDiv);
    }
    
    /**
     * Add a system message to the chat
     * @param {string} message - The message text
     */
    function addSystemMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'system-message';
        messageDiv.textContent = message;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }
    
    /**
     * Add a typing indicator to show the AI is thinking
     */
    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'assistant-message typing-indicator';
        typingDiv.innerHTML = 'AI is thinking<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>';
        typingDiv.id = 'typing-indicator';
        chatContainer.appendChild(typingDiv);
    }
    
    /**
     * Remove the typing indicator
     */
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    /**
     * Scroll the chat container to the bottom
     */
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});