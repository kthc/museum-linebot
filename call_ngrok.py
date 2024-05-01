from pyngrok import ngrok

# Open a HTTP tunnel on the default port 80
# <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:80">


def call_ngrok():
    tunnels = ngrok.get_tunnels()
    for tunnel in tunnels:
        if 'https' in tunnel.public_url:
            print(tunnel.public_url)
            return tunnel.public_url