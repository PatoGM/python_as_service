let main = document.getElementById("main")!

class UI_Request_Init
{
    Type: string = "OPC_PLC_INIT"
    Tag: string[]

    constructor(tags: string[])
    {
        this.Tag = tags
    }
}

class UI_Request_RW
{
    Type: string = "PLC_RW"
    Destination: string = "PLC/IPC"
    Request: { Read: { Interval_ms: number, Tags: string[] }[], Write: { [tag: string]: string } }

    constructor(read: { Interval_ms: number, Tags: string[] }[], write: { [tag: string]: string })
    {
        this.Request = { Read: read, Write: write }
    }
}

class PC_STATS
{
    ws?: WebSocket
    common_url: string
    endpoint = "/home/ws"
    cpu: HTMLDivElement = document.createElement("div")
    ram: HTMLDivElement = document.createElement("div")

    constructor(url: string)
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
                this.cpu.innerHTML = obj.cpu

            if (obj.ram)
                this.ram.innerHTML = obj.ram
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

let ALL_TAGS = ["test", "test2"]

if (main)
{
    let title_div = document.createElement("div")
    title_div.innerText = "Modded"
    main.appendChild(title_div)

    let url_base = "ws://"

    let host = "localhost"

    let port = "8090"

    let endpoint = "/uiredesign/ws"

    let url = url_base + host + ":" + port + endpoint

    let ws: WebSocket
    function setup_ws()
    {
        ws = new WebSocket(url)
        ws.addEventListener("open", evt =>
        {
            let init_obj = new UI_Request_Init(ALL_TAGS)
            ws.send(JSON.stringify(init_obj))
        })
        ws.addEventListener("message", evt => { console.log(evt) })
        ws.addEventListener("error", evt => { console.log(evt) })
        ws.addEventListener("close", evt =>
        {
            if (evt.code != 4200)
            {
                console.log(evt)
                setTimeout(() =>
                {
                    console.log("rewind")
                    setup_ws()
                }, 1000);
                evt.stopPropagation()
            }
        })
    }
    // setup_ws()

    let send_button = document.createElement("button")
    send_button.innerText = "SEND 1"
    send_button.addEventListener
        (
            "click",
            evt =>
            {
                ws.send
                    (
                        JSON.stringify
                            (
                                new UI_Request_RW([{ Interval_ms: 1000, Tags: ["test"] }], {})
                            )
                    )
            }
        )
    main.appendChild(send_button)

    let send_button2 = document.createElement("button")
    send_button2.innerText = "SEND 2"
    send_button2.addEventListener
        (
            "click",
            evt =>
            {
                ws.send
                    (
                        JSON.stringify
                            (
                                new UI_Request_RW([{ Interval_ms: 250, Tags: ["test"] }, { Interval_ms: 500, Tags: ["test2"] }], {})
                            )
                    )
            }
        )
    main.appendChild(send_button2)

    let reconnect_button = document.createElement("button")
    reconnect_button.innerText = "RECONNECT"
    reconnect_button.addEventListener
        (
            "click",
            evt =>
            {
                ws.close(4200, "rewind time")
                setup_ws()
            }
        )
    main.appendChild(reconnect_button)

    let common_url = url_base + host + ":" + port
    let pc = new PC_STATS(common_url)
}