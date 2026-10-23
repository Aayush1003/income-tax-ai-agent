const inputPan = document.getElementById('pan');
const consentBox = document.getElementById('consent');
const fetchButton = document.getElementById('fetchButton');
const statusBox = document.getElementById('status');

const fieldIds = [
  'full_name',
  'father_name',
  'date_of_birth',
  'address',
  'city',
  'state',
  'pincode',
  'email',
  'mobile',
];

function setStatus(message, type = 'neutral') {
  statusBox.textContent = message;
  statusBox.className = `status ${type}`;
}

function fillForm(fields) {
  fieldIds.forEach((fieldName) => {
    const input = document.getElementById(fieldName);
    if (input) {
      input.value = fields[fieldName] || '';
    }
  });
}

async function submitAutofill() {
  const pan = (inputPan.value || '').trim();

  if (!pan) {
    setStatus('Please enter a PAN number.', 'error');
    return;
  }

  if (!consentBox.checked) {
    setStatus('Please confirm consent before fetching profile data.', 'error');
    return;
  }

  fetchButton.disabled = true;
  setStatus('Validating PAN and fetching the verified profile…', 'neutral');

  try {
    const response = await fetch('/api/autofill', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pan, consent: true }),
    });

    const data = await response.json();

    if (!response.ok) {
      const message = data.detail || 'Unable to fetch profile.';
      setStatus(message, 'error');
      return;
    }

    if (!data.success) {
      setStatus(data.message || 'No verified record found for this PAN.', 'error');
      return;
    }

    fillForm(data.fields);
    setStatus(data.message || 'Profile autofilled successfully.', 'success');
  } catch (error) {
    setStatus('Something went wrong while fetching PAN data.', 'error');
  } finally {
    fetchButton.disabled = false;
  }
}

fetchButton.addEventListener('click', submitAutofill);
inputPan.addEventListener('input', () => {
  inputPan.value = inputPan.value.toUpperCase();
});
