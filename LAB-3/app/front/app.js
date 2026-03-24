// ─────────────────────────────────────────
// app.js  —  Frontend logic
// Talks to Flask API via fetch()
// ─────────────────────────────────────────

const API = "/api";

let selectedUserId = null;   // ← NEW: track which user is selected


// ─── GET all users ───────────────────────

async function getUsers() {
  const list = document.getElementById("user-list");
  list.innerHTML = '<p class="loading">Loading...</p>';

  try {
    const res   = await fetch(`${API}/users`);

    if (!res.ok) throw new Error(`Server error: ${res.status}`);

    const users = await res.json();

    if (users.length === 0) {
      list.innerHTML = '<p class="empty">No users yet — add one above!</p>';
      return;
    }

    list.innerHTML = users.map(renderUser).join("");

    // ← NEW: restore highlight after re-render (e.g. after delete)
    if (selectedUserId !== null) {
      const el = document.querySelector(`.user-item[data-id="${selectedUserId}"]`);
      if (el) el.classList.add("selected");
    }

  } catch (err) {
    list.innerHTML = `<p class="empty" style="color:#e74c3c">Error: ${err.message}</p>`;
  }
}


// ─── SELECT a user (highlight) ───────────   ← NEW FUNCTION

function selectUser(id) {
  // Deselect previously selected item
  document.querySelectorAll(".user-item").forEach(el => {
    el.classList.remove("selected");
  });

  // If clicking the same user again → deselect (toggle off)
  if (selectedUserId === id) {
    selectedUserId = null;
    return;
  }

  // Select the clicked user
  selectedUserId = id;
  const el = document.querySelector(`.user-item[data-id="${id}"]`);
  if (el) el.classList.add("selected");
}


// ─── POST a new user ─────────────────────

async function addUser() {
  const nameInput  = document.getElementById("inp-name");
  const emailInput = document.getElementById("inp-email");
  const btn        = document.getElementById("btn-add");

  const name  = nameInput.value.trim();
  const email = emailInput.value.trim();

  if (!name || !email) {
    showMsg("Please fill in both name and email.", "error");
    return;
  }

  btn.textContent = "Saving...";
  btn.disabled    = true;

  try {
    const res  = await fetch(`${API}/add-user`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ name, email })
    });

    const data = await res.json();

    if (res.status === 201) {
      showMsg("✓ User added successfully!", "success");
      nameInput.value  = "";
      emailInput.value = "";
      getUsers();
    } else {
      showMsg(`Error: ${data.error}`, "error");
    }

  } catch (err) {
    showMsg(`Network error: ${err.message}`, "error");
  } finally {
    btn.textContent = "+ Add User";
    btn.disabled    = false;
  }
}


// ─── DELETE a user ───────────────────────

async function deleteUser(id) {
  if (!confirm("Delete this user?")) return;

  try {
    const res = await fetch(`${API}/users/${id}`, { method: "DELETE" });

    if (res.ok) {
      if (selectedUserId === id) selectedUserId = null;  // ← NEW: clear if deleted
      getUsers();
    } else {
      alert("Could not delete user.");
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}


// ─── HELPERS ─────────────────────────────

function renderUser(user) {
  const initials = user.name
    .split(" ")
    .map(w => w[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return `
    <div class="user-item"
         data-id="${user.id}"
         onclick="selectUser(${user.id})">
      <div class="avatar">${initials}</div>
      <div class="user-info">
        <div class="user-name">${user.name}</div>
        <div class="user-email">${user.email}</div>
      </div>
      <div class="user-id">#${user.id}</div>
      <button class="btn-delete"
              onclick="deleteUser(${user.id}); event.stopPropagation()"
              title="Delete">✕</button>
    </div>
  `;
}

function showMsg(text, type) {
  const el = document.getElementById("form-msg");
  el.textContent  = text;
  el.className    = `form-msg ${type}`;
  setTimeout(() => { el.textContent = ""; }, 4000);
}


// ─── Load users on page open ─────────────
getUsers();