#!/usr/bin/env python
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
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")
    def post(self):
        vnos = self.request.get("vnos")
        rezultat = vnos
        rezultat_drugi = ""
        #if "button_cm" in self:
         #   rezultat = 2*int(vnos)
        #elif "button_inch" in self:
         #   rezultat = int(vnos)*3
#DRUGI DEL
        vnos_drugi = self.request.get("vnos_drugi")
        enota = self.request.get("enota")

        if enota == "cm":
            rezultat_drugi= str(vnos_drugi) + " inch = " + str(float(vnos_drugi)*2.54) + " cm"
        elif enota == "inch":
            rezultat_drugi = str(vnos_drugi) + " cm =" + str(float(vnos_drugi) * 0.393700787) + " inch"


        params={"rezultat":rezultat,"rezultat_drugi":rezultat_drugi}
        return self.render_template("pretvornik.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
