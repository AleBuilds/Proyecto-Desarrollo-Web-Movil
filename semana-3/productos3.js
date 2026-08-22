

const contenedor = document.getElementById('productos-container');


const crearTarjetaHTML = (producto) => {
    return `
        <div class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 col-xxl-1">
            <div class="card">
                <img class="card-img-top" src="${producto.imagen}" alt="${producto.nombre}">
                <div class="card-body">
                    <h4 class="card-title">${producto.nombre}</h4>
                    <p class="card-text">${producto.descripcion}</p>
                    <a href="#" class="btn btn-primary">Ver Producto</a>
                </div>
            </div>
        </div>
    `;
};


const mostrarMensaje = (texto, esError = false) => {
    const color = esError ? 'text-danger' : 'text-white';
    contenedor.innerHTML = `<div class="col-12 text-center py-4 ${color}">${texto}</div>`;
};


fetch('productos2.php')
    .then((respuesta) => {
        if (!respuesta.ok) {
            throw new Error('Respuesta HTTP no válida: ' + respuesta.status);
        }
        return respuesta.json();
    })
    .then((json) => {
        if (json.status !== 200 || !Array.isArray(json.data) || json.data.length === 0) {
            mostrarMensaje('No hay productos disponibles por ahora.');
            return;
        }

        
        let html = '';
        json.data.forEach((producto) => {
            html += crearTarjetaHTML(producto);
        });

        contenedor.innerHTML = html;
    })
    .catch((error) => {
        console.error(error);
        mostrarMensaje('No se pudo conectar con el servidor. Intenta más tarde.', true);
    });