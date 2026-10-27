#!/usr/bin/env python3
"""Agrega preguntas nuevas al banco de los simulacros (banco.json).

Uso: python3 scripts/agregar.py nuevas.json [--fecha AAAA-MM-DD]

nuevas.json es una lista de bloques:
  [{"materia": "Programación III",            # nombre del campus o clave (p3, is, dpt, bd2)
    "fuente": "UVA 8 — Ramificación y poda",  # apunte del que salen
    "mc": [{"q": "...", "o": ["correcta", "inc1", "inc2", "inc3"], "a": 0, "e": "explicación"}],
    "ab": [{"q": "...", "r": ["punto 1", "punto 2"]}]}]

Valida cada pregunta (4 opciones distintas, índice válido, explicación, sin repetir enunciados)
y avisa si la opción correcta es mucho más larga que las demás (se adivina por el largo).
Si la materia no existe, la crea. Imprime un resumen y sale con código 1 si algo no pasa la validación.
"""
import json, re, sys, unicodedata, datetime, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BANCO = RAIZ / "banco.json"

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).strip()

def clave_de(nombre):
    return "".join(w[0] for w in norm(nombre).split() if w not in ("de", "y", "la", "el"))[:6] or "mat"

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    fecha = sys.argv[sys.argv.index("--fecha") + 1] if "--fecha" in sys.argv else datetime.date.today().isoformat()
    banco = json.loads(BANCO.read_text(encoding="utf-8"))
    nuevas = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    errores, avisos, agregadas = [], [], 0
    vistos = {norm(p["q"]) for m in banco["materias"].values() for p in m["mc"] + m["ab"]}
    for bloque in nuevas:
        mat = bloque["materia"]
        clave = mat if mat in banco["materias"] else next(
            (k for k, m in banco["materias"].items() if norm(m.get("campus", "")) == norm(mat) or norm(m["nombre"]) == norm(mat)), None)
        if clave is None:
            clave = clave_de(mat)
            while clave in banco["materias"]: clave += "x"
            banco["materias"][clave] = {"nombre": mat, "sub": "", "campus": mat, "mc": [], "ab": []}
            avisos.append(f"Materia nueva en el banco: {mat} ({clave})")
        m = banco["materias"][clave]
        for tipo in ("mc", "ab"):
            for p in bloque.get(tipo, []):
                q = (p.get("q") or "").strip()
                if not q: errores.append(f"{clave}: pregunta vacía"); continue
                if norm(q) in vistos: avisos.append(f"{clave}: repetida, no se agrega: {q[:60]}"); continue
                if tipo == "mc":
                    o, a = p.get("o", []), p.get("a", 0)
                    if len(o) != 4 or len(set(o)) != 4 or not (0 <= a < 4) or not p.get("e"):
                        errores.append(f"{clave}: opción múltiple mal formada: {q[:60]}"); continue
                    otros = max(len(x) for i, x in enumerate(o) if i != a)
                    if len(o[a]) > 1.5 * otros:
                        errores.append(f"{clave}: la correcta es mucho más larga que las demás: {q[:60]}"); continue
                    item = {"q": q, "o": o, "a": a, "e": p["e"]}
                else:
                    r = p.get("r", [])
                    if not r: errores.append(f"{clave}: abierta sin respuesta modelo: {q[:60]}"); continue
                    item = {"q": q, "r": r}
                n = len(m[tipo]) + 1
                item = {"id": f"{clave}-{tipo}-{n:03d}", **item, "fuente": bloque.get("fuente", ""), "agregada": fecha}
                m[tipo].append(item); vistos.add(norm(q)); agregadas += 1
    if errores:
        print("NO SE GUARDÓ NADA. Errores:\n- " + "\n- ".join(errores)); sys.exit(1)
    banco["actualizado"] = fecha
    BANCO.write_text(json.dumps(banco, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"OK: {agregadas} preguntas agregadas.")
    for a in avisos: print("Aviso:", a)

if __name__ == "__main__":
    main()
