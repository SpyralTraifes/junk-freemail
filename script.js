const emailField = document.getElementById("email");
const copyBtn = document.getElementById("copyBtn");
const generateBtn = document.getElementById("generateBtn");
const refreshBtn = document.getElementById("refreshBtn");
const messageList = document.getElementById("messageList");

let currentEmail = "";

function generateRandomEmail() {
  const user = Math.random().toString(36).substring(2, 10);
  return `${user}@yourdomain.com`; // Update with your real domain
}

function displayMessages(messages) {
  messageList.innerHTML = "";
  if (messages.length === 0) {
    messageList.innerHTML = "<li>No messages yet.</li>";
  } else {
    messages.forEach(msg => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${msg.subject}</strong><br>${msg.body}`;
      messageList.appendChild(li);
    });
  }
}

function fetchMessages(email) {
  fetch(`/messages/${email}`)
    .then(res => res.json())
    .then(data => displayMessages(data.messages || []))
    .catch(err => console.error("Error fetching messages", err));
}

generateBtn.addEventListener("click", () => {
  currentEmail = generateRandomEmail();
  emailField.value = currentEmail;
  fetchMessages(currentEmail);
});

refreshBtn.addEventListener("click", () => {
  if (currentEmail) {
    fetchMessages(currentEmail);
  }
});

copyBtn.addEventListener("click", () => {
  navigator.clipboard.writeText(emailField.value);
  copyBtn.textContent = "Copied!";
  setTimeout(() => (copyBtn.textContent = "Copy"), 1000);
});
