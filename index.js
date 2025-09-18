import express from "express"

const app = express()
const PORT = 8080

app.get("/", (req, res) => {
    res.send("Hello there!")
})

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`))