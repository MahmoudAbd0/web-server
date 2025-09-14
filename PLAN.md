# Python Web Server From Scratch – Educational Roadmap

## Tools to Use

- **Python Standard Library only** (to maximize learning):

  - `socket` → Networking (TCP/UDP).
  - `threading` / `multiprocessing` → Concurrency & parallelism.
  - `selectors` → Event-driven concurrency.
  - `queue` → Producer-consumer patterns.
  - `logging` → Robust server logs.
  - `os`, `sys`, `time`, `json`, `re`, `http` → OS ops, serialization, regex parsing, and HTTP helpers.

- **Client Tools**: Browser, `curl`, `httpie`, `telnet`, `netcat`.
- **Optional later**: Wireshark/tcpdump (to _see_ raw traffic and debug your server).

---

## Milestones & Learning Goals

### **Milestone 1: Core TCP Server**

**Objective**: Create the minimal TCP server that can accept one connection and respond with "Hello, World!" in HTTP.

- Outcomes:

  - Server runs on `localhost:8000`.
  - Handles one connection at a time.
  - Sends valid HTTP response: `HTTP/1.1 200 OK`.
  - Closes connection after response.

- Concepts:

  - TCP sockets (`bind`, `listen`, `accept`, `recv`, `send`, `close`).
  - HTTP message structure (status line, headers, body).
  - Difference between TCP stream and HTTP request-response.

---

### **Milestone 2: HTTP Request Parsing & Routing**

**Objective**: Understand and respond to real HTTP requests.

- Outcomes:

  - Parse **request line**: method, path, HTTP version.
  - Extract headers and (optionally) body.
  - Implement routing (e.g., `/hello` → handler function).
  - Return `404 Not Found` when route not matched.

- Concepts:

  - Parsing algorithms (string splitting, regex).
  - HTTP request-response lifecycle.
  - Error handling with proper status codes.

---

### **Milestone 3: Serving Static Files & Templating**

**Objective**: Extend server to serve HTML, CSS, JS, and images.

- Outcomes:

  - Read files from `static/` and return with correct MIME type.
  - Implement mini-templating: placeholders like `{{name}}` replaced with dynamic data.
  - Serve a simple website with HTML + CSS.

- Concepts:

  - MIME types (`text/html`, `image/png`, etc.).
  - File I/O and path sanitization (avoid directory traversal!).
  - Template engines (string replacement, later extend to loops/conditions).

---

### **Milestone 4: Concurrency & Parallelism**

**Objective**: Handle many clients simultaneously.

- Outcomes:

  - Add **multi-threading**: one thread per client.
  - Compare with **multiprocessing** (CPU-bound tasks).
  - Experiment with **async/event-driven** model using `selectors` or `asyncio`.

- Concepts:

  - Difference between concurrency (switching tasks) and parallelism (truly simultaneous).
  - Race conditions, locks, queues.
  - Tradeoffs: threads vs processes vs async.

---

### **Milestone 5: Algorithms & Scheduling**

**Objective**: Learn backend scheduling and queuing.

- Outcomes:

  - Implement a **thread pool** (fixed workers).
  - Use a **request queue** to handle overload.
  - Add simple rate limiting algorithm (token bucket or leaky bucket).

- Concepts:

  - Classic backend algorithms (producer-consumer).
  - Scheduling (FIFO, priority).
  - Load shedding when overloaded.

---

### **Milestone 6: State Management & Sessions**

**Objective**: Support persistent state (like cookies/sessions).

- Outcomes:

  - Parse cookies from requests.
  - Implement simple in-memory session store (`dict` keyed by session_id).
  - Store user-specific data (e.g., visit count).

- Concepts:

  - HTTP is stateless → need for cookies/session.
  - Serialization (JSON, pickling).
  - Memory vs disk-backed persistence.

---

### **Milestone 7: Logging, Error Handling, and Graceful Shutdown**

**Objective**: Add utilities real systems depend on.

- Outcomes:

  - Log each request (method, path, status, duration).
  - Handle server errors → return custom `500 Internal Server Error` page.
  - Support graceful shutdown (catch `KeyboardInterrupt`).

- Concepts:

  - Python `logging` levels (DEBUG, INFO, ERROR).
  - Exception handling inside threads/processes.
  - Signal handling (`signal` module).

---

### **Milestone 8: Bonus Advanced Features**

**Optional challenges** (pick and choose):

- HTTPS support with `ssl` wrapper.
- Chunked transfer encoding.
- Persistent connections (`Connection: keep-alive`).
- Implement rudimentary **reverse proxy**.
- Add config file (YAML/JSON) for server settings.
- Write your own **benchmark client** (measure requests/sec).

---

### **Milestone 9: Dockerization**

**Objective**: Package the web server into a reproducible container image.

- **Expected Outcomes**:

  - Write a `Dockerfile` that:

    - Uses a lightweight base image (`python:3.11-slim`).
    - Copies server code inside `/app`.
    - Exposes a configurable port (default `8000`).
    - Runs the server via `CMD ["python", "server.py"]`.

  - Build & run with:

    ```bash
    docker build -t my-python-webserver .
    docker run -p 8000:8000 my-python-webserver
    ```

  - Verify you can connect from browser or `curl` to `http://localhost:8000`.

- **Key Concepts to Master**:

  - Containerization basics (image vs container).
  - Layering in Docker (`COPY`, `RUN`, `CMD`).
  - Networking: mapping host → container ports.
  - Reproducibility & environment isolation.

- **Stretch Goals**:

  - Use Docker volumes for static file mounts.
  - Docker Compose to run server + test client.

---

### **Milestone 10: Installable CLI Program**

**Objective**: Turn your server into a proper Python package with a CLI entrypoint.

- **Expected Outcomes**:

  - Project has a `setup.py` or modern `pyproject.toml` (recommended with `setuptools`).
  - Define CLI entrypoint in `console_scripts`, e.g.:

    ```toml
    [project.scripts]
    pyserver = "myserver.cli:main"
    ```

  - Install locally with:

    ```bash
    pip install -e .
    ```

  - Run server as a command:

    ```bash
    pyserver --port 8080 --debug
    ```

  - CLI can:

    - Start the server on custom host/port.
    - Set log level.
    - Optionally load config from file (`--config server.json`).

- **Key Concepts to Master**:

  - Python packaging (`pyproject.toml`, `setuptools`, `hatch`, or `poetry`).
  - Entry points & CLI design (`argparse` or `click`).
  - Distribution via PyPI (optional stretch).

- **Stretch Goals**:

  - Add `pipx` install support → `pipx install .` then run anywhere.
  - Create a `requirements.txt` / `Pipfile` for dependencies (if you later add non-stdlib stuff).
  - Publish package to **TestPyPI** and try `pip install`.

---

Tip:

After Milestone 10, you’ll have a project that you can:

- Run locally with `python server.py`.
- Run as a **CLI tool** (`pyserver --port 8080`).
- Run in a **Docker container**.
- Share on GitHub as an educational repo.

---

## Expected Final Outcomes

By the end, you’ll have:

- A **Python web server** (educational, not production-ready).
- Ability to explain:

  - TCP/IP & HTTP/1.1 internals.
  - Routing, templating, concurrency models.
  - Backend algorithms (thread pools, rate limiting, sessions).
  - Core utilities: logging, error handling, state.

- A complete **teaching project repo** you can use for others.

---

## Extra Tips & Guidance

1. **Work incrementally**: Each milestone should have its own code version (tag in git).
2. **Visualize traffic**: Use Wireshark/tcpdump to see raw HTTP packets.
3. **Use curl/httpie**: Send custom requests (`curl -v http://localhost:8000/hello`).
4. **Draw diagrams**: Sequence diagrams for request-response, thread pools, etc.
5. **Compare with real servers**: After each milestone, look at how Flask, Django, or Gunicorn do it.
6. **Document as you go**: Treat this like a lab notebook; explain concepts alongside code.

---
