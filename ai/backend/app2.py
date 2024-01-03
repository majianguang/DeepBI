import tornado.ioloop
import tornado.web
from ai.backend.chat_task import ChatClass
from ai.backend.aidb.autopilot.autopilot_mysql_api import AutopilotMysql
import json
from ai.backend.base_config import CONFIG
from ai.backend.aidb.dashboard.prettify_dashboard import PrettifyDashboard



class MainHandler(tornado.web.RequestHandler):
    async def post(self):
        data = json.loads(self.request.body.decode('utf-8'))

        # 异步处理接收到的数据
        await self.process_data(data)

        # 返回响应
        self.write("POST request handled asynchronously in main thread")

    async def process_data(self, data):
        # 在这里异步处理接收到的数据，例如打印或执行其他操作
        print("Received data:", data)
        # 模拟异步处理
        print("Data processed asynchronously")

        print('data: ', data)

        user_name = data['user_name']
        report_id = data['report_id']
        file_name = data['file_name']

        chat_class = ChatClass(None, user_name)
        autopilotMysql = AutopilotMysql(chat_class)
        json_str = {
            "file_name": file_name,
            "report_id": report_id
        }
        await autopilotMysql.deal_question(json_str)


class DashboardHandler(tornado.web.RequestHandler):
    def get(self, page_name):
        self.render(f"{page_name}.html")

    async def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print('/api/dashboard data : ', data)

        # 异步处理接收到的数据
        await self.process_data(data)

        # 返回响应
        self.write("POST request handled asynchronously in main thread")

    async def process_data(self, data):
        # 在这里异步处理接收到的数据，例如打印或执行其他操作
        print("Received data:", data)
        # 模拟异步处理
        print("Data processed asynchronously")

        print('data: ', data)

        user_name = data['user_name']
        task_id = data['task_id']
        file_name = data['file_name']

        chat_class = ChatClass(None, user_name)
        prettifyDashboard = PrettifyDashboard(chat_class)
        json_str = {
            "file_name": file_name,
            "task_id": task_id
        }
        await prettifyDashboard.deal_question(json_str)



def make_app():
    return tornado.web.Application([
        (r"/api/autopilot", MainHandler),
        (r"/api/dashboard", DashboardHandler),
    ])

class CustomApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/autopilot", MainHandler),
            (r"/api/dashboard", DashboardHandler),
            (r"/api/dashboard/([0-9a-zA-Z]+)", DashboardHandler),
        ]

        settings = {
            "template_path": CONFIG.up_file_path,  # 指定模板路径
        }

        super().__init__(handlers, **settings)


# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8340)
#     tornado.ioloop.IOLoop.current().start()
