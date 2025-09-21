import express from "express"
import dotenv  from "dotenv"
dotenv.config()

const app = express()
const PORT = 8080

app.get("/", (req, res) => {
    res.send("Hello, there!")
})

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`))