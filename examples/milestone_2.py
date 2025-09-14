from server import Server, Router, Response

def hello_handler(request):
    return Response(body="Hello from home page ")


def about_handler(request):
    return Response(body="Hello from about page ")


router = Router()
router.get("/", hello_handler)
router.get("/about", about_handler)

server = Server(host="127.0.0.1", port=8080, router=router)
server.start()