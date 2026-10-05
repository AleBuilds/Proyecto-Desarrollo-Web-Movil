// El token nunca llega al JavaScript: viaja en una cookie HttpOnly que administra el Gateway.
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const clp = (n) => "$" + Number(n).toLocaleString("es-CL");
const CATS = { hummus: "Hummus", falafel: "Falafel", shawarma: "Shawarma", parrilla: "Parrilla", pescados: "Pescados", ensaladas: "Ensaladas" };
const KEY = "el_mediterraneo_carrito";   // el carrito solo guarda {id, cantidad}; el precio lo decide el servidor
let user = null, platos = [], mantenerAviso = false;
// Cambia de ruta sin que el hashchange borre el aviso que acabamos de mostrar.
function ir(hash) { if (location.hash !== hash) { mantenerAviso = true; location.hash = hash; } else render(); }

const carrito = {
    get() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } },
    set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* sin storage */ } },
    cambiar(id, d) {
        const c = this.get(), i = c.find((x) => x.id === id);
        if (i) i.cantidad += d; else if (d > 0) c.push({ id, cantidad: d });
        this.set(c.filter((x) => x.cantidad > 0));
    },
    total() { return this.get().reduce((s, x) => s + x.cantidad, 0); },
};

async function api(url, opts = {}) {
    try {
        const r = await fetch(url, { credentials: "include", headers: { "Content-Type": "application/json" }, ...opts });
        let data = null; try { data = await r.json(); } catch (e) { /* sin cuerpo */ }
        return { ok: r.ok, status: r.status, data };
    } catch (e) { return { ok: false, status: 0, data: { detail: "Sin conexión con el servidor" } }; }
}
function aviso(texto, error = false) {
    const a = $("#aviso"); a.textContent = texto; a.className = error ? "error" : ""; a.hidden = !texto;
}
const detalle = (r) => (typeof r.data?.detail === "string" ? r.data.detail : "Datos inválidos, revisa el formulario");
const esAdmin = () => user?.roles.includes("admin");

async function cargarSesion() { const r = await api("/auth/me"); user = r.ok ? r.data : null; }
async function cargarCarta() { const r = await api("/public/menu"); platos = r.ok ? r.data.products : []; }

function tarjeta(p) {
    return `<article class="card"><img src="${esc(p.img)}" alt="${esc(p.nombre)}"><div><small>${esc(CATS[p.categoria] || p.categoria)}</small>
    <h3>${esc(p.nombre)}</h3><p>${esc(p.descripcion)}</p><div class="pie"><span class="precio">${clp(p.precio)}</span>
    <button data-agregar="${p.id}">Agregar</button></div></div></article>`;
}
const pedirLogin = (que) => `<div class="panel">Inicia sesión para ${que}. <a class="btn" href="#/login">Ingresar</a></div>`;

const VISTAS = {
    inicio: () => `<section class="hero"><h1>El Mediterráneo</h1><p>Hummus, falafel, shawarma y parrilla con recetas tradicionales.</p>
        <a class="btn" href="#/menu">Ver menú</a> <a class="btn" href="#/reservas">Reservar</a></section>
        <h2>Platos destacados</h2><div class="grid">${platos.slice(0, 3).map(tarjeta).join("")}</div>`,

    menu: (cat) => `<h2>Nuestro menú</h2><div class="filtros"><a href="#/menu" class="${cat ? "" : "activo"}">Todos</a>
        ${Object.entries(CATS).map(([k, v]) => `<a href="#/menu/${k}" class="${cat === k ? "activo" : ""}">${v}</a>`).join("")}</div>
        <div class="grid">${platos.filter((p) => !cat || p.categoria === cat).map(tarjeta).join("") || "<p>No hay platos en esta categoría.</p>"}</div>`,

    carrito: () => {
        const filas = carrito.get().map((x) => ({ ...x, p: platos.find((p) => p.id === x.id) })).filter((x) => x.p);
        if (!filas.length) return `<h2>Tu carrito</h2><p>Aún no agregas platos. <a href="#/menu">Ver menú</a></p>`;
        const sub = filas.reduce((s, x) => s + x.p.precio * x.cantidad, 0);
        return `<h2>Tu carrito</h2><div class="panel">${filas.map((x) => `<div class="fila"><span>${esc(x.p.nombre)}</span>
            <span><button class="sec" data-menos="${x.id}">−</button> ${x.cantidad} <button class="sec" data-mas="${x.id}">+</button></span>
            <b>${clp(x.p.precio * x.cantidad)}</b></div>`).join("")}<p>Subtotal: <b>${clp(sub)}</b> (el envío y el total los confirma el servidor)</p></div>
            ${user ? `<div class="panel"><h3>Método de entrega</h3><form id="f-pedido">
            <label>Método<select name="metodo"><option value="delivery">Delivery (+${clp(2500)})</option><option value="retiro">Retiro en local</option></select></label>
            <label>Nombre<input name="nombre" required maxlength="80"></label><label>Teléfono<input name="telefono" type="tel" required minlength="6" maxlength="20"></label>
            <label>Dirección (delivery)<input name="direccion" maxlength="160"></label><label>Notas<textarea name="notas" maxlength="300"></textarea></label>
            <button type="submit">Confirmar pedido</button></form></div>` : pedirLogin("confirmar tu pedido")}`;
    },

    reservas: () => !user ? `<h2>Reservar mesa</h2>${pedirLogin("reservar una mesa")}` : `<h2>Reservar mesa</h2><div class="panel"><form id="f-reserva">
        <label>Fecha<input name="fecha" type="date" required></label><label>Hora<input name="hora" type="time" required></label>
        <label>Personas<input name="personas" type="number" min="1" max="20" required></label><label>Nombre<input name="nombre" required maxlength="80"></label>
        <label>Teléfono<input name="telefono" type="tel" required minlength="6" maxlength="20"></label><button type="submit">Reservar</button></form></div>`,

    pedidos: async () => {
        if (!user) return `<h2>Mis pedidos</h2>${pedirLogin("ver tus pedidos")}`;
        const r = await api("/api/orders");
        const lista = r.ok ? r.data.orders : [];
        return `<h2>${esAdmin() ? "Todos los pedidos" : "Mis pedidos"}</h2>` + (lista.map((o) => `<div class="panel"><b>Pedido #${o.id}</b>
            ${esAdmin() ? ` · ${esc(o.username)}` : ""} · ${esc(o.metodo)} · ${esc(o.status)}<br>${o.items.map((i) => `${i.cantidad}× ${esc(i.nombre)}`).join(", ")}<br>
            <b>Total ${clp(o.total)}</b></div>`).join("") || "<p>Aún no hay pedidos.</p>");
    },

    admin: async () => {
        if (!user) return `<h2>Administración</h2>${pedirLogin("administrar la carta")}`;
        if (!esAdmin()) return `<h2>Administración</h2><div class="panel">No tienes permisos de administrador (403).</div>`;
        const r = await api("/api/reservations");
        return `<h2>Administración</h2><div class="panel"><h3>Carta</h3>${platos.map((p) => `<div class="fila"><span>${esc(p.nombre)} · ${clp(p.precio)}</span>
            <button class="sec" data-quitar="${p.id}">Eliminar</button></div>`).join("")}</div>
            <div class="panel"><h3>Nuevo plato</h3><form id="f-plato"><label>Categoría<select name="categoria">${Object.entries(CATS).map(([k, v]) => `<option value="${k}">${v}</option>`).join("")}</select></label>
            <label>Nombre<input name="nombre" required maxlength="80"></label><label>Descripción<input name="descripcion" maxlength="300"></label>
            <label>Precio (CLP)<input name="precio" type="number" min="1" required></label><label>Imagen (https://…)<input name="img" type="url"></label>
            <button type="submit">Agregar plato</button></form></div>
            <div class="panel"><h3>Reservas</h3>${(r.ok ? r.data.reservations : []).map((x) => `<div class="fila">${esc(x.fecha)} ${esc(x.hora)} · ${x.personas} pers. · ${esc(x.nombre)} · ${esc(x.telefono)}</div>`).join("") || "Sin reservas."}</div>`;
    },

    login: () => `<h2>Ingresar</h2><div class="panel"><form id="f-login"><label>Usuario<input name="username" autocomplete="username" required></label>
        <label>Contraseña<input name="password" type="password" autocomplete="current-password" required></label><button type="submit">Entrar</button></form>
        <p><small>Demo: <code>ana / 1234</code> (cliente) · <code>ernesto / admin123</code> (admin)</small></p></div>`,
};

function nav() {
    const ruta = location.hash.split("/")[1] || "inicio";
    const l = (id, txt) => `<a href="#/${id === "inicio" ? "" : id}" class="${ruta === id ? "activo" : ""}">${txt}</a>`;
    $("#nav").innerHTML = `<a class="logo" href="#/">EL MEDITERRÁNEO</a>${l("inicio", "Inicio")}${l("menu", "Menú")}${l("reservas", "Reservas")}
        ${user ? l("pedidos", "Pedidos") : ""}${esAdmin() ? l("admin", "Admin") : ""}${l("carrito", `Carrito (${carrito.total()})`)}
        ${user ? `<span class="usuario">${esc(user.username)}</span><button class="sec" data-salir>Salir</button>` : l("login", "Ingresar")}`;
}

async function render() {
    const [, ruta, arg] = location.hash.split("/");
    nav();
    $("#vista").innerHTML = await (VISTAS[ruta || "inicio"] || VISTAS.inicio)(arg);
}

document.addEventListener("click", async (ev) => {
    const b = ev.target.closest("button"); if (!b) return;
    const d = b.dataset;
    if (d.agregar) { carrito.cambiar(+d.agregar, 1); aviso("Agregado al carrito"); nav(); }
    else if (d.mas) { carrito.cambiar(+d.mas, 1); render(); }
    else if (d.menos) { carrito.cambiar(+d.menos, -1); render(); }
    else if ("salir" in d) {
        const r = await api("/auth/logout", { method: "POST" });
        user = null; aviso(r.ok ? "Sesión cerrada" : detalle(r), !r.ok); ir("#/");
    } else if (d.quitar) {
        const r = await api(`/api/products/${d.quitar}`, { method: "DELETE" });
        if (r.ok) await cargarCarta(); aviso(r.ok ? "Plato eliminado" : detalle(r), !r.ok); render();
    }
});

document.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const f = ev.target, v = Object.fromEntries(new FormData(f));
    if (f.id === "f-login") {
        const r = await api("/auth/login", { method: "POST", body: JSON.stringify(v) });
        if (!r.ok) return aviso(detalle(r), true);
        await cargarSesion(); aviso(`Bienvenido/a, ${user.username}`); ir("#/");
    } else if (f.id === "f-pedido") {
        const items = carrito.get().map(({ id, cantidad }) => ({ id, cantidad }));
        const r = await api("/api/orders", { method: "POST", body: JSON.stringify({ ...v, items }) });
        if (!r.ok) return aviso(r.status === 401 ? "Tu sesión expiró, vuelve a ingresar" : detalle(r), true);
        carrito.set([]); aviso(`Pedido #${r.data.id} confirmado. Total ${clp(r.data.total)}`); ir("#/pedidos");
    } else if (f.id === "f-reserva") {
        const r = await api("/api/reservations", { method: "POST", body: JSON.stringify({ ...v, personas: +v.personas }) });
        if (!r.ok) return aviso(detalle(r), true);
        aviso(`Reserva confirmada: ${r.data.fecha} a las ${r.data.hora} para ${r.data.personas} personas`); f.reset();
    } else if (f.id === "f-plato") {
        const r = await api("/api/products", { method: "POST", body: JSON.stringify({ ...v, precio: +v.precio }) });
        if (!r.ok) return aviso(detalle(r), true);
        await cargarCarta(); aviso("Plato agregado"); render();
    }
});

window.addEventListener("hashchange", () => { if (mantenerAviso) mantenerAviso = false; else aviso(""); render(); });
Promise.all([cargarSesion(), cargarCarta()]).then(render);
