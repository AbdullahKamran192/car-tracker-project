import express from "express"
import dotenv  from "dotenv"
import path from "path"
import { getCars } from "./Config/database.js"
import { carsRouter } from "./Routes/cars.js"
dotenv.config()

const app = express()
const PORT = 8080

app.set('view engine', 'ejs');
app.set('views', path.resolve("./src/Views"))

app.use(carsRouter)

app.get("/", (req, res) => {
    res.send("Hello, there!")
})


app.listen(PORT, () => console.log(`Server listening on port ${PORT}`))