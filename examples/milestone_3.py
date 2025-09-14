from server import Server, Router, Response
from server.templating import render_template

def profile_handler(request):
    return render_template("profile.html", {"name":"Mahmoud"})

router = Router()
router.get("/profile", profile_handler)

server = Server(host="127.0.0.1", port=8080, router=router)
server.start()