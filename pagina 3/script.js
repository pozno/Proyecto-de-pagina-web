const checkbox = document.getElementById('check');
const body = document.querySelector('body');

checkbox.addEventListener('change', function() {
    if (this.checked) {
        // Si el menú está activo, bloquea el desplazamiento vertical
        body.style.overflowY = 'hidden';
    } else {
        // Si el menú está inactivo, permite el desplazamiento vertical
        body.style.overflowY = 'auto';
    }
});
