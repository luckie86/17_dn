#!/usr/bin/env python
import os
import jinja2
import webapp2
import random

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

class GlavnoMesto():
    def __init__(self,glavnomesto, drzava, slika):
        self.glavnomesto = glavnomesto
        self.drzava = drzava
        self.slika = slika

def podatki():
    lj = GlavnoMesto("Ljubljana", "Slovenia","/assets/img/city1.jpg")
    zg = GlavnoMesto("Zagreb", "Croatia", "/assets/img/city2.jpg")
    w = GlavnoMesto("Vienna", "Austria", "/assets/img/city3.jpg")
    rm = GlavnoMesto("Rome", "Italy", "/assets/img/city4.jpg")
    be = GlavnoMesto("Berlin", "Germany", "/assets/img/city5.jpg")

    return [lj, zg, w, rm, be]

class MainHandler(BaseHandler):
    def get(self):
        glavno_mesto = podatki()[random.randint(0,4)]
        glavno_mesto_dict = {"glavno_mesto": glavno_mesto}
        return self.render_template("index.html", glavno_mesto_dict)

class ResultHandler(BaseHandler):
    def post(self):
        odgovor = self.request.get("odgovor")
        drzava = self.request.get("drzava")

        glavna_mesta = podatki()
        for item in glavna_mesta:
            if item.drzava == drzava:
                if item.glavnomesto.lower() == odgovor.lower():
                    rezultat = True
                else:
                    rezultat = False

                rez_dict = {"rezultat": rezultat, "item": item}
                return self.render_template("result.html", rez_dict)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
], debug=True)
