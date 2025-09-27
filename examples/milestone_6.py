from server import  Request, Response, Router, ServerFactory


router  = Router()


def visits_handler(request):
    visits = request.session.get("visits")
    return Response(body=f"You have visited {visits} times")
    

router.get("/visits", visits_handler)


server = ServerFactory.create_server(server_type="async", router=router)
server.start()