function joinCode() {
  const inputs = document.querySelectorAll('.code-input-group input');
  const code = Array.from(inputs).map(i => i.value).join('');
  document.getElementById('code').value = code;
}

document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('.code-input-group input');
  inputs.forEach((input, index) => {
    input.addEventListener('input', () => {
      if (input.value && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
    });
  });
});
