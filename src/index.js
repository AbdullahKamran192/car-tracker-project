import express from "express"
import dotenv  from "dotenv"
import path from "path"
import { getCars } from "./Config/database.js"
import { carsRouter } from "./Routes/cars.js"
dotenv.config()

//===================== S3 request presigner ===========================

const bucketName = process.env.BUCKET_NAME
const bucketRegion = process.env.BUCKET_REGION
const accessKey = process.env.ACCESS_KEY
const secretAccessKey = process.env.SECRET_ACCESS_KEY

const s3 = new S3Client({
    credentials: {
        accessKeyId: accessKey,
        secretAccessKey: secretAccessKey,
    },
    region: bucketRegion
});

import {S3Client, PutObjectCommand, GetObjectCommand} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner"

//======================================================================

const app = express()
const PORT = 8080

app.set('view engine', 'ejs');
app.set('views', path.resolve("./src/Views"))

app.use(express.static('./src/Public'))

app.use(carsRouter)

app.get("/", (req, res) => {
    res.send("Hello, there!")
})


app.listen(PORT, () => console.log(`Server listening on port ${PORT}`))