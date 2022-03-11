from tornado.web import RequestHandler, Application, StaticFileHandler
from tornado.ioloop import IOLoop
import os
import json


httpport = int(os.getenv('PORT', 8080))

class BasicRequestHandler(RequestHandler):
    def get(self):
        self.render('test.html')

class JSONRequestHandler(RequestHandler):
    def get(self):
        with open('requirements.txt','r') as f:
            packages = f.read().splitlines()
            self.write(json.dumps(packages))
       

class ResourceParamRequestHandler(RequestHandler):
    def get(self, studentname, courseid):
        self.write(f"Querying info for {studentname} taking course {courseid}")

class QueryStringRequestHandler(RequestHandler):
    def get(self):
        n = int(self.get_argument("n"))
        r = "odd" if n % 2 else "even"
        
        self.write("the number " + str(n) + " is " + r)

class StaticRequestHandler(RequestHandler):
    def get(self):
        self.render("index.html")

class MainPageHandler(RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)

class SlidesHandler(RequestHandler):
    def get(self):
        self.render('slides.html')


class UploadHandler(StaticFileHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        files = self.request.files['imgFile']
        for f in files:
            with open(f'img/{f.filename}','wb') as fh:
                fh.write(f.body)
        self.write(f'a< href="https://localhost:{httpport}/img/{f.filename}"')


if __name__ == '__main__':
    app = Application([
        (r'/',MainPageHandler),
        (r'/basic',BasicRequestHandler),
        (r'/slides',SlidesHandler),
        (r"/blog", StaticRequestHandler),
        (r"/iseven", QueryStringRequestHandler),
        (r"/students/([a-z]+)/([0-9]+)", ResourceParamRequestHandler),
        (r'/json', JSONRequestHandler),
        (r'/img/(.*)', JSONRequestHandler,{'path':'img'}),
    ])
    app.listen(port=httpport)
    IOLoop.current().start()