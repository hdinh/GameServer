class TableHandler(tornado.web.RequestHandler):
    def get(self, table_name):
        #self.write('table')
        self.render('templates/table_viewer.html')

class CreateTableHandler(tornado.web.RequestHandler):
    def post(self):
        self.write('create tabling')

