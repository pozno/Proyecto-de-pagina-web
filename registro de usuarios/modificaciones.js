const URL = " http://127.0.0.1:5000/"

// Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//const URL = "https://USUARIO.pythonanywhere.com/"

// Variables de estado para controlar la visibilidad y los datos del formulario
let id= '';
let nombre = '';
let rango = '';
let edad= '';
let pais = '';
let imagen_url = '';
let imagenSeleccionada = null;
let imagenUrlTemp = null;
let mostrarDatosProducto = false;

document.getElementById('form-obtener-usuario').addEventListener('submit', obtenerProducto);
document.getElementById('form-guardar-cambios').addEventListener('submit', guardarCambios);
document.getElementById('nuevaImagen').addEventListener('change', seleccionarImagen);

// Se ejecuta cuando se envía el formulario de consulta. Realiza una solicitud GET a la API y obtiene los datos del producto correspondiente al código ingresado.
function obtenerUsuarios(event) {
    event.preventDefault();
    id = document.getElementById('codigo').value;
    fetch(URL + 'usuarios/' + id)
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error('Error al obtener los datos del usuario.')
            }
        })
        .then(data => {
            nombre = data.nombre;
            rango = data.rango;
            edad = data.edad;
            pais = data.pais;
            imagen_url = data.imagen_url;
            mostrarDatosUsuario = true; //Activa la vista del segundo formulario
            mostrarFormulario();
        })
        .catch(error => {
            alert('id no encontrado.');
        });
}

// Muestra el formulario con los datos del producto
function mostrarFormulario() {
    if (mostrarDatosProducto) {
        document.getElementById('nombreModificar').value = nombre;
        document.getElementById('rangoModificar').value = rango;
        document.getElementById('edadModificar').value = edad;
        document.getElementById('paisModificar').value = pais;

        const imagenActual = document.getElementById('imagen-actual');
        if (imagen_url && !imagenSeleccionada) { // Verifica si imagen_url no está vacía y no se ha seleccionado una imagen

            imagenActual.src = './static/imagenes/' + imagen_url;                    
            
            //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
            //imagenActual.src = 'https://www.pythonanywhere.com/user/USUARIO/files/home/USUARIO/mysite/static/imagenes/' + imagen_url;

            imagenActual.style.display = 'block'; // Muestra la imagen actual
        } else {
            imagenActual.style.display = 'none'; // Oculta la imagen si no hay URL
        }

        document.getElementById('datos-usuario').style.display = 'block';
    } else {
        document.getElementById('datos-usuario').style.display = 'none';
    }
}

// Se activa cuando el usuario selecciona una imagen para cargar.
function seleccionarImagen(event) {
    const file = event.target.files[0];
    imagenSeleccionada = file;
    imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa

    const imagenVistaPrevia = document.getElementById('imagen-vista-previa');
    imagenVistaPrevia.src = imagenUrlTemp;
    imagenVistaPrevia.style.display = 'block';
}

// Se usa para enviar los datos modificados del producto al servidor.
function guardarCambios(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('id', id);
    formData.append('nombre', document.getElementById('nombreModificar').value);
    formData.append('rango', document.getElementById('rangoModificar').value);
    formData.append('pais', document.getElementById('paisModificar').value);
    formData.append('edad', document.getElementById('edadModificar').value);

    // Si se ha seleccionado una imagen nueva, la añade al formData. 
    if (imagenSeleccionada) {
        formData.append('imagen', imagenSeleccionada, imagenSeleccionada.name);
    }

    fetch(URL + 'usuarios/' + id, {
        method: 'PUT',
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                throw new Error('Error al guardar los nuevos datos.')
            }
        })
        .then(data => {
            alert('datos actualizados correctamente.');
            limpiarFormulario();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al actualizar datos.');
        });
}

// Restablece todas las variables relacionadas con el formulario a sus valores iniciales, lo que efectivamente "limpia" el formulario.
function limpiarFormulario() {
    document.getElementById('codigo').value = '';
    document.getElementById('nombreModificar').value = '';
    document.getElementById('rangoModificar').value = '';
    document.getElementById('edadModificar').value = '';
    document.getElementById('paisModificar').value = '';
    document.getElementById('nuevaImagen').value = '';

    const imagenActual = document.getElementById('imagen-actual');
    imagenActual.style.display = 'none';

    const imagenVistaPrevia = document.getElementById('imagen-vista-previa');
    imagenVistaPrevia.style.display = 'none';

 id= '';
 nombre = '';
 rango = '';
 edad= '';
 pais = '';
 imagen_url = '';
 imagenSeleccionada = null;
 imagenUrlTemp = null;
 mostrarDatosProducto = false;

    document.getElementById('datos-usuario').style.display = 'none';
}