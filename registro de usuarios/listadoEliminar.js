const URL = " http://127.0.0.1:5000/"

//Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//const URL = "https://USUARIO.pythonanywhere.com/"

// Obtiene el contenido del inventario
function obtenerUsuarios() {
    fetch(URL + 'usuarios') // Realiza una solicitud GET al servidor y obtener la lista de productos.
        .then(response => {
            // Si es exitosa (response.ok), convierte los datos de la respuesta de formato JSON a un objeto JavaScript.
            if (response.ok) { return response.json(); }
        })
        // Asigna los datos de los productos obtenidos a la propiedad productos del estado.
        .then(data => {
            const UsuariosTable = document.getElementById('usuarios-table').getElementsByTagName('tbody')[0];
            UsuariosTable.innerHTML = ''; // Limpia la tabla antes de insertar nuevos datos
            data.forEach(dato => {
                const row = UsuariosTable.insertRow();
                row.innerHTML = `
                    <td>${dato.id}</td>
                    <td>${dato.nombre}</td>
                    <td>${dato.edad}</td>
                    <td align="right">${dato.rango}</td>
                    <td><button onclick="eliminarUsuario('${dato.id}')">Eliminar</button></td>
                `;
            });
        })
        // Captura y maneja errores, mostrando una alerta en caso de error al obtener los productos.
        .catch(error => {
            console.log('Error:', error);
            alert('Error al eliminar el usuario.');
        });
}

// Se utiliza para eliminar un producto.
function eliminarUsuario(id) {
    // Se muestra un diálogo de confirmación. Si el usuario confirma, se realiza una solicitud DELETE al servidor a través de fetch(URL + 'productos/${codigo}', {method: 'DELETE' }).
    if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        fetch(URL + `usuarios/${id}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    // Si es exitosa (response.ok), elimina el producto y da mensaje de ok.
                    obtenerUsuarios(); // Vuelve a obtener la lista de productos para actualizar la tabla.
                    alert('Usuario eliminado correctamente.');
                }
            })
            // En caso de error, mostramos una alerta con un mensaje de error.
            .catch(error => {
                alert(error.message);
            });
    }
}

// Cuando la página se carga, llama a obtenerProductos para cargar la lista de productos.
document.addEventListener('DOMContentLoaded', obtenerUsuarios);