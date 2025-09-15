from server import Server, Request, Response, Router
import time

router  = Router()


def slow_handler(request):
    time.sleep(5)
    return Response(body="Done after 5 seconds")
    

router.get("/slow", slow_handler)


server = Server(host="127.0.0.1", port=8080, router=router, mode="multiprocessing")
server.start()