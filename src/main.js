
let history = [];

async function getResponse(prompt) {
  const response = await fetch('http://127.0.0.1:5000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: prompt })
  });

  if (!response.ok) {
    console.error('Error en la respuesta del servidor');
    return "Lo siento, hubo un error al procesar tu mensaje.";
  }

  const data = await response;
  return data;
}

// User chat div
export const userDiv = (data) => {
  return `
  <!-- User Chat -->
          <div class="flex items-center gap-2 justify-start m-2">
            <img src="public/human.png" alt="user icon" class="w-10 h-10 rounded-full"/>
            <div class="bg-gemDeep text-white p-1 rounded-md shadow-md mx-2">${data}</div>
          </div>
  `;
};

// AI Chat div
export const aiDiv = (data) => {
  return `
  <!-- AI Chat -->
          <div class="flex gap-2 justify-end m-2">
            <div class="bg-gemDeep text-white p-1 rounded-md shadow-md mx-2">${data}</div>
            <img src="public/bot.png" alt="bot icon" class="w-10 h-10 rounded-full"/>
          </div>
  `;
};

async function handleSubmit(event) {
  event.preventDefault();

  let userMessage = document.getElementById("prompt");
  const chatArea = document.getElementById("chat-container");

  var prompt = userMessage.value.trim();
  if (prompt === "") {
    return;
  }

  console.log("user message", prompt);

  chatArea.innerHTML += userDiv(md().render(prompt));
  userMessage.value = "";
  const aiResponse = await getResponse(prompt);
  chatArea.innerHTML += aiDiv(aiResponse);

  let newUserRole = {
    role: "user",
    parts: prompt,
  };
  let newAIRole = {
    role: "model",
    parts: aiResponse,
  };

  history.push(newUserRole);
  history.push(newAIRole);

  console.log(history);
}

const chatForm = document.getElementById("chat-form");
chatForm.addEventListener("submit", handleSubmit);

chatForm.addEventListener("keyup", (event) => {
  if (event.keyCode === 13) handleSubmit(event);
});

// Get the elements
const chatbotPopup = document.getElementById('chatbot-popup');
const openChatbotButton = document.getElementById('open-chatbot');

// Event to open the chatbot
openChatbotButton.addEventListener('click', () => {
    chatbotPopup.style.display = 'block';
});

const closeChatbotButton = document.getElementById('close-chatbot');

// Event to close the chatbot
closeChatbotButton.addEventListener('click', () => {
    chatbotPopup.style.display = 'none';
});
