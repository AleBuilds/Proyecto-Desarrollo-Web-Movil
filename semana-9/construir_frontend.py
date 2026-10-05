#!/usr/bin/env python3
"""Convierte el frontend antiguo (semana-7, PHP) a HTML estático que sirve el Gateway.

Uso (desde semana-9):  python construir_frontend.py
No necesita PHP. Los estilos y onclick en línea se sacan a archivos para mantener el CSP estricto.
"""
import datetime
import re
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ORIGEN = RAIZ.parent / "semana-7" / "fronted-1ra-entrega"
DESTINO = RAIZ / "gateway" / "static" / "site"
# (archivo php, salida html, variables forzadas)
PAGINAS = [("index", "index", {}), ("menu", "menu", {}), ("carrito", "carrito", {}), ("entrega", "entrega", {"metodo": "delivery"}),
           ("entrega", "entrega-retiro", {"metodo": "retiro"}), ("confirmacion", "confirmacion", {}), ("reservas", "reservas", {}),
           ("contacto", "contacto", {}), ("nosotros", "nosotros", {}), ("producto", "producto", {})]
ENLACES = [("inicio", "Inicio", "index.php"), ("menu", "Menú", "menu.php"), ("nosotros", "Nosotros", "nosotros.php"),
           ("reservas", "Reservas", "reservas.php"), ("contacto", "Contacto", "contacto.php")]
EXTRA_CSS = ".h-220{height:220px}.h-230{height:230px}.img-85{width:85px;height:85px;object-fit:cover}.w-105{width:105px}.mw-90{min-width:90px}\n"

# ---------- mini intérprete de lo poco de PHP que usan las páginas ----------
TOK = re.compile(r"\s*(?:(=>)|([\[\],])|'((?:[^'\\]|\\.)*)'|(-?\d+))", re.S)


def parse(s, i=0):
    m = TOK.match(s, i)
    if m.group(2) == "[":
        i, lista, dic = m.end(), [], {}
        while True:
            m2 = TOK.match(s, i)
            if m2.group(2) == "]":
                return (dic or lista), m2.end()
            if m2.group(2) == ",":
                i = m2.end()
                continue
            v, i = parse(s, i)
            m3 = TOK.match(s, i)
            if m3 and m3.group(1):
                dic[v], i = parse(s, m3.end())
            else:
                lista.append(v)
    if m.group(3) is not None:
        return m.group(3).replace("\\'", "'"), m.end()
    return int(m.group(4)), m.end()


def cabecera(src):
    m = re.match(r"\s*<\?php(.*?)\?>", src, re.S)
    env, bloque = {}, m.group(1)
    for v in re.finditer(r"\$(\w+)\s*=\s*", bloque):
        txt = bloque[v.end():]
        if txt.startswith(("[", "'")) or re.match(r"-?\d", txt):
            env[v.group(1)] = parse(txt)[0]
        elif txt.startswith("isset"):  # $x = isset($_GET[..]) ? ... : 'valor por defecto';
            env[v.group(1)] = re.search(r":\s*'([^']*)'\s*;", txt).group(1)
    return env, src[m.end():]


def valor(expr, env):
    expr = expr.strip()
    if expr.startswith("date("):
        return str(datetime.date.today().year)
    m = re.fullmatch(r"(.+?)\s*===\s*'([^']*)'\s*\?\s*'([^']*)'\s*:\s*'([^']*)'", expr)
    if m:
        return m.group(3) if valor(m.group(1), env) == m.group(2) else m.group(4)
    m = re.fullmatch(r"(clp|number_format)\((.+?)(?:,.*)?\)", expr)
    if m:
        return ("$" if m.group(1) == "clp" else "") + f"{valor(m.group(2), env):,}".replace(",", ".")
    m = re.fullmatch(r"\$(\w+)((?:\['\w+'\])*)", expr)
    v = env[m.group(1)]
    for k in re.findall(r"\['(\w+)'\]", m.group(2)):
        v = v[k]
    return v


def eco(txt, env):
    def f(m):
        res = str(valor(m.group(1), env))
        w = re.search(r"\$(pedido|reserva)\['(\w+)'\]", m.group(1))  # marca para que el JS rellene el dato real
        return f'<span data-{w.group(1)}="{w.group(2)}">{res}</span>' if w else res
    return re.sub(r"<\?php echo (.+?);\s*\?>", f, txt)


def bucles(txt, env):
    def f(m):
        return "".join(eco(m.group(3), {**env, m.group(2): it}) for it in valor(m.group(1), env))
    return re.sub(r"<\?php foreach \((\$[\w\[\]']+) as \$(\w+)\): \?>(.*?)<\?php endforeach; \?>", f, txt, flags=re.S)


def leer(nombre):
    return (ORIGEN / nombre).read_text(encoding="utf-8").replace("\r\n", "\n")


def navbar(activo):
    html = re.sub(r"^\s*<\?php.*?\?>\s*", "", leer("navbar.php"), count=1, flags=re.S)
    items = "".join(
        f'<li class="nav-item"><a class="nav-link text-uppercase fw-semibold px-3 '
        f'{"active text-sol border-bottom border-2 border-warning" if activo == k else "text-light"}" href="{href}">{label}</a></li>'
        for k, label, href in ENLACES)
    html = re.sub(r"<\?php foreach \(\$enlaces.*?<\?php endforeach; \?>", items, html, flags=re.S)
    html = html.replace('<script src="carrito.js"></script>', "")
    return html.replace('<a href="carrito.php"', '<span id="cuenta" class="me-3 small text-nowrap"></span>\n            <a href="carrito.php"', 1)


# ---------- transformaciones ----------
ESTILOS = {}


def extraer_estilos(html):
    def f(m):
        tag, css = m.group(0), m.group(2).strip()
        nombre = ESTILOS.setdefault(css, f"st{len(ESTILOS)}")
        tag = tag.replace(m.group(1), "", 1)
        if re.search(r'\sclass="', tag):
            return re.sub(r'\sclass="', f' class="{nombre} ', tag, count=1)
        fin = re.search(r"\s*(/?)>$", tag)
        return tag[:fin.start()] + f' class="{nombre}"{fin.group(1)}>'
    return re.sub(r'<[a-zA-Z][^<>]*?(\sstyle="([^"]*)")[^<>]*>', f, html)


def enlaces(html):
    def f(m):
        attr, nombre, query = m.group(1), m.group(2), m.group(3) or ""
        if nombre == "entrega":
            return f'{attr}="/entrega-retiro.html"' if "retiro" in query else f'{attr}="/entrega.html"'
        return f'{attr}="/{"" if nombre == "index" else nombre + ".html"}{query}"'
    return re.sub(r'(href|action)="(\w+)\.php(\?[^"]*)?"', f, html)


def dinamico(nombre, html):
    """Menú y destacados del inicio salen del backend (/public/menu) y los pinta mediterraneo.js."""
    if nombre == "menu":
        html = re.sub(r'<main class="container mb-5 flex-grow-1">.*?</main>',
                      '<main class="container mb-5 flex-grow-1"><div class="filtros mb-4 text-center" id="filtros"></div>'
                      '<div class="row g-4" id="grilla"></div></main>', html, flags=re.S)
    if nombre == "index":
        html = re.sub(r'<div class="row g-4">\s*<!-- Tarjeta 1 -->.*?(\s*</div>\s*</div>\s*</section>\s*<!-- Banner Promocional -->)',
                      r'<div class="row g-4" id="destacados">\1', html, flags=re.S)
    if nombre == "producto":  # stepper de cantidad y botón agregar: de onclick a data-*
        nuevos = iter(['data-cant="-1"', 'data-cant="1"', "data-agregar-detalle"])
        html = re.sub(r'onclick="[^"]*"', lambda m: next(nuevos, ""), html)
    return html


def construir(php, salida, forzadas):
    env, cuerpo = cabecera(leer(f"{php}.php"))
    env.update(forzadas)
    html = dinamico(php, cuerpo)
    html = html.replace("<?php include 'navbar.php'; ?>", navbar(env.get("activo", "")))
    html = html.replace("<?php include 'footer.php'; ?>", leer("footer.php"))
    html = eco(bucles(html, env), env)
    html = re.sub(r"<script>.*?</script>", "", html, flags=re.S)           # scripts en línea (el JS vive en mediterraneo.js)
    html = re.sub(r'\sonclick="[^"]*"', "", html)
    html = enlaces(extraer_estilos(html))
    html = html.replace('<link rel="stylesheet" href="style.css">',
                        '<link rel="stylesheet" href="/static/site/style.css">\n    <link rel="stylesheet" href="/static/site/site.css">')
    html = re.sub(r"<body", f'<body data-page="{php}"', html, count=1)
    html = html.replace("</body>", '<script src="/static/site/mediterraneo.js"></script>\n</body>')
    assert "<?" not in html and "?>" not in html, f"Quedó PHP sin convertir en {salida}"
    (DESTINO / f"{salida}.html").write_text(html, encoding="utf-8")
    return salida


if __name__ == "__main__":
    DESTINO.mkdir(parents=True, exist_ok=True)
    shutil.copy(ORIGEN / "style.css", DESTINO / "style.css")
    hechas = [construir(*p) for p in PAGINAS]
    reglas = "".join(f".{n}{{" + ";".join(d.strip() + " !important" for d in css.split(";") if d.strip()) + "}\n" for css, n in ESTILOS.items())
    (DESTINO / "site.css").write_text(EXTRA_CSS + reglas, encoding="utf-8")
    print(f"OK: {len(hechas)} páginas y {len(ESTILOS)} estilos extraídos en {DESTINO}")
