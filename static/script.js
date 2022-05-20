const labels = document.querySelectorAll('label');
const inputs = document.querySelectorAll('input');

labels.forEach((label)=>{
    label.classList.add('form-label');
})
inputs.forEach((input)=>{
    input.classList.add('form-control');
})