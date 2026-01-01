const express = require("express");
const bcrypt = require("bcrypt");

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Fake user database
const users = {
  admin: bcrypt.hashSync("SuperSecretPassword!", 10),
  javier: bcrypt.hashSync("Password123!", 10)
};

// ❌ Vulnerable login endpoint (timing leak)
app.post("/login", async (req, res) => {
  const { username, password } = req.body;

  const storedHash = users[username];

  if (!storedHash) {
    // User does not exist → early return (fast)
    return res.status(401).json({ error: "Invalid username or password" });
  }

  // User exists → bcrypt comparison (slow)
  await bcrypt.compare(password, storedHash);

  return res.status(401).json({ error: "Invalid username or password" });
});

// Precomputed dummy hash (same cost)
const DUMMY_HASH = bcrypt.hashSync("dummy-password", 10);

// ✅ Fixed login endpoint
app.post("/login-fixed", async (req, res) => {
  const { username, password } = req.body;

  const storedHash = users[username] || DUMMY_HASH;

  await bcrypt.compare(password, storedHash);

  return res.status(401).json({ error: "Invalid username or password" });
});

app.listen(3000, () => {
  console.log("Demo auth server running on http://localhost:3000");
});
