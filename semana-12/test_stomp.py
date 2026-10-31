import pytest

from consumidor import interpretar
from productor import construir_mensaje

PEDIDO = {"id": "123", "cliente": "Ana", "monto": "123.45"}


def ida_y_vuelta(formato):
    cuerpo, mime = construir_mensaje(formato, PEDIDO, "hola")
    return cuerpo, interpretar(cuerpo, {"x-formato": formato, "content-type": mime})


def test_texto():
    cuerpo, (fmt, contenido) = ida_y_vuelta("texto")
    assert (fmt, contenido) == ("texto", "hola")


def test_fijo_largo_36_y_campos():
    cuerpo, (fmt, c) = ida_y_vuelta("fijo")
    assert len(cuerpo) == 36
    assert cuerpo == "000123Ana                 0000123.45"
    assert c == {"id": "000123", "cliente": "Ana", "monto": "0000123.45"}


def test_json():
    _, (fmt, c) = ida_y_vuelta("json")
    assert fmt == "json" and c == PEDIDO


def test_xml():
    cuerpo, (fmt, c) = ida_y_vuelta("xml")
    assert cuerpo.startswith("<pedido>")
    assert fmt == "xml" and c == PEDIDO


def test_formato_se_deduce_del_mime():
    assert interpretar('{"a": 1}', {"content-type": "application/json"})[0] == "json"
    assert interpretar("<pedido/>", {"content-type": "application/xml"})[0] == "xml"
    assert interpretar("x", {})[0] == "texto"


@pytest.mark.parametrize("cliente", ["x" * 21, "Ñandú"])
def test_productor_rechaza_cliente_invalido(cliente):
    with pytest.raises(ValueError):
        construir_mensaje("fijo", {**PEDIDO, "cliente": cliente}, "")


def test_productor_rechaza_id_y_monto_invalidos():
    with pytest.raises(ValueError):
        construir_mensaje("fijo", {**PEDIDO, "id": "1234567"}, "")
    with pytest.raises(ValueError):
        construir_mensaje("fijo", {**PEDIDO, "monto": "-1"}, "")
    with pytest.raises(ValueError):
        construir_mensaje("fijo", {**PEDIDO, "monto": "99999999.99"}, "")


def test_productor_formato_desconocido():
    with pytest.raises(ValueError):
        construir_mensaje("csv", PEDIDO, "")


@pytest.mark.parametrize("cuerpo,formato", [
    ("corto", "fijo"),
    ("00A123Ana                 0000123.45", "fijo"),
    ("000123Ana                 0000123,45", "fijo"),
    ("{no es json", "json"),
    ("<otro><x/></otro>", "xml"),
    ("<pedido>", "xml"),
    ("x", "csv"),
])
def test_consumidor_rechaza_mensajes_invalidos(cuerpo, formato):
    with pytest.raises(ValueError):
        interpretar(cuerpo, {"x-formato": formato})
