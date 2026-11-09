// Gestor de Carrito en localStorage
const CarritoStorage = {
    KEY: 'el_mediterraneo_carrito',
    
    obtener() {
        try {
            const data = localStorage.getItem(this.KEY);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    },

    guardar(items) {
        try {
            localStorage.setItem(this.KEY, JSON.stringify(items));
            this.actualizarBadge();
        } catch (e) {
            console.error('Error al guardar carrito', e);
        }
    },

    agregar(producto) {
        const items = this.obtener();
        const index = items.findIndex(item => item.nombre === producto.nombre);
        if (index >= 0) {
            items[index].cantidad += (producto.cantidad || 1);
        } else {
            items.push({
                nombre: producto.nombre,
                precio: producto.precio,
                cantidad: producto.cantidad || 1,
                img: producto.img
            });
        }
        this.guardar(items);
    },

    modificarCantidad(index, delta) {
        const items = this.obtener();
        if (items[index]) {
            items[index].cantidad += delta;
            if (items[index].cantidad <= 0) {
                items.splice(index, 1);
            }
            this.guardar(items);
        }
    },

    eliminar(index) {
        const items = this.obtener();
        if (items[index]) {
            items.splice(index, 1);
            this.guardar(items);
        }
    },

    totalCount() {
        const items = this.obtener();
        return items.reduce((sum, i) => sum + i.cantidad, 0);
    },

    actualizarBadge() {
        const badges = document.querySelectorAll('.badge-fuego, .carrito-badge');
        const count = this.totalCount();
        badges.forEach(b => {
            b.textContent = count;
        });
    }
};

document.addEventListener('DOMContentLoaded', () => {
    CarritoStorage.actualizarBadge();
});
