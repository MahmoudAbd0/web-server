from server import  Request, Response, Router, ServerFactory
import time

router  = Router()


def slow_handler(request):
    time.sleep(5)
    return Response(body="Done after 5 seconds")
    

router.get("/slow", slow_handler)


server = ServerFactory.create_server(server_type="threading", router=router)
server.start()