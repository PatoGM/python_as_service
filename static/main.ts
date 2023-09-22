let main = document.getElementById("main")

class PC_STATS
{
    ws?: WebSocket
    common_url: string
    endpoint = "/home/ws"
    cpu: HTMLDivElement = document.createElement("div")
    ram: HTMLDivElement = document.createElement("div")

    constructor(url: string, main: HTMLElement)
    {
        this.common_url = url
        this.setup()
        main.appendChild(this.cpu)
        main.appendChild(this.ram)
    }

    setup()
    {
        this.ws = new WebSocket(this.common_url + this.endpoint)

        this.ws.addEventListener("message", evt =>
        {
            let obj = JSON.parse(evt.data)

            if (obj.cpu)
                this.cpu.innerHTML = `CPU: ${obj.cpu}`

            if (obj.ram)
                this.ram.innerHTML = `RAM: ${obj.ram}`
        })

        this.ws.addEventListener("error", console.log)
        this.ws.addEventListener("close", evt =>
        {
            setTimeout(() => {
                this.setup()
            }, 1000);
            evt.stopPropagation()
        })
        this.ws.addEventListener("open", console.log)
    }
}

if (main)
{
    let title_div = document.createElement("div")
    title_div.innerText = "Modded"
    main.appendChild(title_div)

    let url_base = "ws://"

    let host = "155.138.247.250"

    let port = "8090"

    let endpoint = "/uiredesign/ws"

    let url = url_base + host + ":" + port + endpoint

    let common_url = url_base + host + ":" + port

    let pc = new PC_STATS(common_url, main)
}