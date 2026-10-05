// El Mediterráneo (frontend antiguo) conectado al Gateway. Sin JS en línea: compatible con el CSP estricto.
// El carrito guarda {id, cantidad}; nombre/precio/foto son solo para mostrar y se refrescan desde /public/menu.
// Al confirmar se envía únicamente {id, cantidad}: el total lo calcula el backend.
(() => {
    const KEY = 'el_mediterraneo_carrito', ENVIO = 2500;
    const CATS = { hummus: 'Hummus', falafel: 'Falafel', shawarma: 'Shawarma', parrilla: 'Parrilla', pescados: 'Pescados', ensaladas: 'Ensaladas' };
    const $ = (s) => document.querySelector(s);
    const $$ = (s) => [...document.querySelectorAll(s)];
    const clp = (n) => '$' + new Intl.NumberFormat('es-CL').format(n);
    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    let carta = [], usuario = null;

    const leer = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
    const guardar = (v) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* sin storage */ } badge(); };
    const badge = () => $$('.carrito-badge').forEach((b) => { b.textContent = leer().reduce((s, i) => s + i.cantidad, 0); });
    const agregar = (p, n = 1) => {
        const c = leer(), i = c.find((x) => x.id === p.id);
        if (i) i.cantidad += n; else c.push({ id: p.id, nombre: p.nombre, precio: p.precio, img: p.img, cantidad: n });
        guardar(c);
    };
    // Refresca nombre/precio/foto con los datos del servidor y descarta platos que ya no existen.
    const sincronizar = () => {
        if (!carta.length) return;  // sin respuesta del backend no se toca el carrito
        guardar(leer().filter((i) => carta.some((p) => p.id === i.id))
            .map((i) => { const p = carta.find((x) => x.id === i.id); return { id: p.id, nombre: p.nombre, precio: p.precio, img: p.img, cantidad: i.cantidad }; }));
    };

    async function api(url, opts = {}) {
        try {
            const r = await fetch(url, { credentials: 'include', headers: { 'Content-Type': 'application/json' }, ...opts });
            let data = null; try { data = await r.json(); } catch (e) { /* sin cuerpo */ }
            return { ok: r.ok, status: r.status, data };
        } catch (e) { return { ok: false, status: 0, data: null }; }
    }
    const detalle = (r) => (typeof r.data?.detail === 'string' ? r.data.detail : 'Revisa los datos del formulario');
    const aLogin = (msg) => { alert(msg); location.href = '/panel#/login'; };

    const tarjeta = (p, col, h) => `<div class="${col}"><article class="card h-100 border-0 shadow-sm card-hover rounded-3 overflow-hidden">
        <a href="/producto.html"><img src="${esc(p.img)}" class="card-img-top img-cover ${h}" alt="${esc(p.nombre)}"></a>
        <div class="card-body d-flex flex-column p-4 bg-white">
            <small class="text-oliva text-uppercase fw-bold tracking-wider mb-1">${esc(CATS[p.categoria] || p.categoria)}</small>
            <h4 class="card-title font-cinzel fw-bold mt-1 mb-2"><a href="/producto.html" class="text-carbon text-decoration-none fs-5">${esc(p.nombre)}</a></h4>
            <p class="text-secondary small mb-4 flex-grow-1">${esc(p.descripcion)}</p>
            <div class="d-flex justify-content-between align-items-center border-top pt-3 mt-auto">
                <span class="fw-bold text-fuego fs-5">${clp(p.precio)}</span>
                <button type="button" class="btn btn-fuego btn-sm text-uppercase px-3 fw-bold" data-agregar="${p.id}">Agregar</button>
            </div></div></article></div>`;

    const PAGINAS = {
        index() { $('#destacados').innerHTML = carta.slice(0, 3).map((p) => tarjeta(p, 'col-12 col-md-4', 'h-220')).join(''); },

        menu() {
            const cat = new URLSearchParams(location.search).get('categoria') || 'todos';
            $('#filtros').innerHTML = [['todos', 'Todos'], ...Object.entries(CATS)].map(([k, v]) =>
                `<a class="filtro-pill ${cat === k ? 'activo' : ''}" href="/menu.html${k === 'todos' ? '' : '?categoria=' + k}">${v}</a>`).join('');
            $('#grilla').innerHTML = carta.filter((p) => cat === 'todos' || p.categoria === cat).map((p) => tarjeta(p, 'col-12 col-md-6 col-lg-4', 'h-230')).join('')
                || '<p class="text-center text-secondary">No hay platos en esta categoría.</p>';
        },

        carrito() {
            sincronizar();
            const items = leer(), cont = $('#contenedor-items'), btn = $('#btn-continuar');
            if (!items.length) {
                cont.innerHTML = `<div class="card border-0 shadow-sm p-5 rounded-3 text-center bg-white mb-3"><i class="fa fa-shopping-basket text-muted fs-1 mb-3"></i>
                    <h5 class="font-cinzel text-carbon fw-bold mb-2">Tu carrito está vacío</h5><p class="text-secondary small mb-4">Aún no has agregado ningún plato de nuestro menú.</p>
                    <div><a href="/menu.html" class="btn btn-fuego rounded-3 text-uppercase fw-bold px-4 py-2">Explorar el Menú</a></div></div>`;
                $('#subtotal-txt').textContent = clp(0); $('#total-txt').textContent = clp(0); btn.classList.add('disabled'); return;
            }
            btn.classList.remove('disabled');
            cont.innerHTML = items.map((i, n) => `<div class="card border-0 shadow-sm mb-3 rounded-3 overflow-hidden p-3 bg-white"><div class="d-flex align-items-center flex-wrap gap-3">
                <img src="${esc(i.img)}" class="rounded-3 img-cover img-85" alt="${esc(i.nombre)}">
                <div class="flex-grow-1"><h6 class="font-cinzel fw-bold text-carbon mb-1 fs-6">${esc(i.nombre)}</h6>
                    <small class="text-secondary">Precio unitario: <span class="text-fuego fw-bold">${clp(i.precio)}</span></small></div>
                <div class="input-group rounded-2 w-105"><button class="btn btn-sm btn-outline-secondary" type="button" data-mod="${n}:-1">-</button>
                    <input type="text" class="form-control form-control-sm text-center bg-white fw-bold" value="${i.cantidad}" readonly>
                    <button class="btn btn-sm btn-outline-secondary" type="button" data-mod="${n}:1">+</button></div>
                <div class="fw-bold text-carbon fs-6 text-end px-2 mw-90">${clp(i.precio * i.cantidad)}</div>
                <button class="btn btn-link text-danger p-1 border-0" type="button" title="Eliminar producto" data-del="${n}"><i class="fa fa-trash fs-5"></i></button></div></div>`).join('');
            const sub = items.reduce((s, i) => s + i.precio * i.cantidad, 0);
            $('#subtotal-txt').textContent = clp(sub); $('#total-txt').textContent = clp(sub + ENVIO);
        },

        entrega() {
            const f = $('form'), metodo = location.pathname.includes('retiro') ? 'retiro' : 'delivery';
            if (metodo === 'retiro') { const d = $('#direccion'); d.required = false; d.closest('.col-md-6').hidden = true; }  // retiro: no hay dirección de entrega
            f.addEventListener('submit', async (ev) => {
                ev.preventDefault();
                const v = Object.fromEntries(new FormData(f)), items = leer().map(({ id, cantidad }) => ({ id, cantidad }));
                if (!items.length) return alert('Tu carrito está vacío');
                const r = await api('/api/orders', { method: 'POST', body: JSON.stringify({ metodo, nombre: v.nombre, telefono: v.telefono, direccion: v.direccion || '', notas: v.notas || '', items }) });
                if (r.status === 401) return aLogin('Inicia sesión para confirmar tu pedido (tu carrito se conserva).');
                if (!r.ok) return alert(detalle(r));
                try { sessionStorage.setItem('ultimo_pedido', JSON.stringify({ id: r.data.id, total: r.data.total, items: r.data.items, metodo })); } catch (e) { /* sin storage */ }
                guardar([]); location.href = '/confirmacion.html';
            });
        },

        confirmacion() {
            let p = null; try { p = JSON.parse(sessionStorage.getItem('ultimo_pedido')); } catch (e) { /* sin pedido */ }
            if (!p) { location.replace('/carrito.html'); return; }
            const n = p.items.reduce((s, i) => s + i.cantidad, 0), set = (k, t) => { const e = $(`[data-pedido="${k}"]`); if (e) e.textContent = t; };
            set('numero', p.id); set('cantidad', `${n} producto${n === 1 ? '' : 's'}`); set('total', clp(p.total));
            set('metodo_entrega', p.metodo === 'retiro' ? 'Retiro en Local' : 'Despacho a Domicilio'); set('tiempo_estimado', p.metodo === 'retiro' ? '15 - 20 min' : '30 - 45 min');
        },

        reservas() {
            const f = $('form');
            f.addEventListener('submit', async (ev) => {
                ev.preventDefault();
                const v = Object.fromEntries(new FormData(f));
                const r = await api('/api/reservations', { method: 'POST', body: JSON.stringify({ fecha: v.fecha, hora: v.hora, personas: +v.personas, nombre: v.nombre, telefono: v.telefono }) });
                if (r.status === 401) return aLogin('Inicia sesión para reservar una mesa.');
                if (!r.ok) return alert(detalle(r));
                Object.entries({ fecha: r.data.fecha, hora: r.data.hora, personas: r.data.personas, nombre: r.data.nombre }).forEach(([k, t]) => { $(`[data-reserva="${k}"]`).textContent = t; });
                f.reset();
            });
        },

        contacto() {  // el backend aún no tiene endpoint de contacto
            const f = $('form');
            f.addEventListener('submit', (ev) => { ev.preventDefault(); alert('Formulario de demostración: el backend todavía no guarda mensajes de contacto.'); f.reset(); });
        },

        producto() {
            $$('[data-cant]').forEach((b) => b.addEventListener('click', () => { const e = $('#cant'); e.value = Math.max(1, (parseInt(e.value, 10) || 1) + +b.dataset.cant); }));
            $('[data-agregar-detalle]').addEventListener('click', () => {
                const p = carta.find((x) => x.nombre === $('h1').textContent.trim());
                if (!p) return alert('Este plato no está disponible en la carta actual.');
                agregar(p, parseInt($('#cant').value, 10) || 1); alert('¡Producto agregado al carrito!');
            });
        },
    };

    document.addEventListener('click', async (ev) => {
        const b = ev.target.closest('[data-agregar],[data-mod],[data-del],[data-salir]'); if (!b) return;
        const d = b.dataset;
        if (d.agregar) { const p = carta.find((x) => x.id === +d.agregar); if (p) { agregar(p); alert('¡Producto agregado al carrito!'); } }
        else if (d.mod || d.del) {
            const c = leer(), [n, delta] = (d.mod || `${d.del}:0`).split(':').map(Number);
            if (d.del) c.splice(n, 1); else if (c[n]) { c[n].cantidad += delta; if (c[n].cantidad <= 0) c.splice(n, 1); }
            guardar(c); PAGINAS.carrito();
        } else if ('salir' in d) { ev.preventDefault(); await api('/auth/logout', { method: 'POST' }); location.reload(); }
    });

    function cuenta() {
        const e = $('#cuenta'); if (!e) return;
        e.innerHTML = usuario
            ? `<a href="/panel#/pedidos" class="text-light text-decoration-none"><i class="fa fa-user me-1"></i>${esc(usuario.username)}</a>
               ${usuario.roles.includes('admin') ? ' · <a href="/panel#/admin" class="text-light text-decoration-none">Admin</a>' : ''} · <a href="#" class="text-light" data-salir>Salir</a>`
            : '<a href="/panel#/login" class="text-light text-decoration-none"><i class="fa fa-sign-in me-1"></i>Ingresar</a>';
    }

    (async () => {
        badge();
        const [m, s] = await Promise.all([api('/public/menu'), api('/auth/me')]);
        carta = m.ok ? m.data.products : []; usuario = s.ok ? s.data : null;
        cuenta();
        (PAGINAS[document.body.dataset.page] || (() => {}))();
        badge();
    })();
})();
