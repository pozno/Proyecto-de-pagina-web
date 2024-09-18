const URL = " http://127.0.0.1:5000/"

// Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//const URL = "https://USUARIO.pythonanywhere.com/"


// Realizamos la solicitud GET al servidor para obtener todos los datos.
fetch(URL + 'usuarios')
    .then(function (response) {
        if (response.ok) {
            //Si la respuesta es exitosa (response.ok), convierte el cuerpo de la respuesta de formato JSON a un objeto JavaScript y pasa estos datos a la siguiente promesa then.
            return response.json(); 
    } else {
            // Si hubo un error, lanzar explícitamente una excepción para ser "catcheada" más adelante
            throw new Error('Error al obtener los datos.');
        }
    })

    //Esta función maneja los datos convertidos del JSON.
    .then(function (data) {
        let tablaUsuarios = document.getElementById('tablaUsuarios'); //Selecciona el elemento del DOM donde se mostrarán los datos.

        // Iteramos sobre cada dato y agregamos filas a la tabla
        for (let dato of data) {
            let fila = document.createElement('tr'); //Crea una nueva fila de tabla (<tr>) para cada dato.
            fila.innerHTML = '<td>' + dato.id + '</td>' +
                '<td>' + dato.nombre + '</td>' +
                '<td align="right">' + dato.edad + '</td>' +
                '<td align="right">' + dato.rango + '</td>' +
                // Mostrar miniatura de la imagen
                '<td><img src=./static/imagenes/' + dato.imagen_url +' alt="Imagen del dato" style="width: 100px;"></td>' + '<td align="right">' + dato.pais + '</td>';
                
                //Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
                //'<td><img src=https://www.pythonanywhere.com/user/USUARIO/files/home/USUARIO/mysite/static/imagenes/' + dato.imagen_url +' alt="Imagen del dato" style="width: 100px;"></td>' + '<td align="right">' + dato.proveedor + '</td>';
            
            //Una vez que se crea la fila con el contenido del dato, se agrega a la tabla utilizando el método appendChild del elemento tablaUsuarios.
            tablaUsuarios.appendChild(fila);
        }
    })

    //Captura y maneja errores, mostrando una alerta en caso de error al obtener los datos.
    .catch(function (error) {
        // Código para manejar errores
        alert('Error al obtener los datos.');
    });