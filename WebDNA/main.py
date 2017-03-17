#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

class ResultHandler(BaseHandler):
    def post(self):
        dna = self.request.get("dna")
        lasje = {"CCAGCAATCGC": "Črni", "GCCAGTGCCG": "Rjavi", "TTAGCTATCGC": "Plavolasi"}
        obraz = {"GCCACGG": "Kvadratast", "ACCACAA": "Okrogel", "AGGCCTCA": "Ovalen"}
        oci = {"TTGTGGTGGC": "Modre", "GGGAGGTGGC": "Zelene", "AAGTAGTGAC": "Rjave"}
        spol = {"TGAAGGACCTTC": "Ženska", "TGCAGGAACTTC": "Moški"}
        rasa = {"AAAACCTCA": "Bela", "CGACTACAG": "Črna", "CGCGGGCCG": "Rumena"}

        lasje_ujemanje = ""
        for kljuc, vrednost in lasje.items():
            if kljuc in dna:
                lasje_ujemanje = vrednost
                break

        obraz_ujemanje = ""
        for kljuc, vrednost in obraz.items():
            if kljuc in dna:
                obraz_ujemanje = vrednost
                break

        oci_ujemanje = ""
        for kljuc, vrednost in oci.items():
            if kljuc in dna:
                oci_ujemanje = vrednost
                break

        spol_ujemanje = ""
        for kljuc, vrednost in spol.items():
            if kljuc in dna:
                spol_ujemanje = vrednost
                break

        rasa_ujemanje = ""
        for kljuc, vrednost in rasa.items():
            if kljuc in dna:
                rasa_ujemanje = vrednost
                break

        storilec = {
            "lasje": lasje_ujemanje,
            "obraz": obraz_ujemanje,
            "oci": oci_ujemanje,
            "spol": spol_ujemanje,
            "rasa": rasa_ujemanje,
            }

        return self.render_template("result.html", storilec)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
], debug=True)
