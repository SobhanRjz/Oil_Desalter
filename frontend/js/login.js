const form = document.getElementById('loginForm');
const submitBtn = document.getElementById('submitBtn');
const hint = document.getElementById('formHint');
const togglePwd = document.getElementById('togglePwd');
const pwd = document.getElementById('password');
const email = document.getElementById('email');

togglePwd.addEventListener('click', () => {
  const showing = pwd.type === 'text';
  pwd.type = showing ? 'password' : 'text';
  togglePwd.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  hint.textContent = '';
  hint.classList.remove('error');

  // Simple client validation
  if (!email.value.trim() || !pwd.value.trim()) {
    hint.textContent = 'Please enter email and password.';
    hint.classList.add('error');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Signing in…';

  // Simulate call to your backend (replace with real fetch to FastAPI)
  try {
    await new Promise(r => setTimeout(r, 900));
    // Example payload you would send:
    // const res = await fetch('/api/login', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ email: email.value, password: pwd.value, remember: document.getElementById('remember').checked })});
    // const data = await res.json();
    hint.textContent = 'Login successful! Redirecting to input page...';

    // Navigate to input page after successful login
    setTimeout(() => {
      window.location.href = '/input';
    }, 1000); // Brief delay to show success message

  } catch (err) {
    hint.textContent = 'Something went wrong. Please try again.';
    hint.classList.add('error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Get Started';
  }
});
