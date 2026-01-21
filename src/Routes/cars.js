import { Router } from "express";
import { getCars, getCarByImageName, deleteCarByImageName } from "../Config/database.js";

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

export const carsRouter = Router()

carsRouter.get("/cars", async (req, res) => {
    const cars = await getCars()

    for (const car of cars) {
        const getObjectParams = {
            Bucket: bucketName,
            Key: `${car.image_name}.jpg`,
        };
        const command = new GetObjectCommand(getObjectParams);
        const url = await getSignedUrl(s3, command, { expiresIn: 3600 });


        car.httpURL = url;
    }

    res.render('cars', {
        cars: cars
    })
})

carsRouter.get("/cars/:imageName", async (req, res) => {
    const imageName = req.params.imageName;

    console.log("Image name is ")
    console.log(imageName)

    const car = await getCarByImageName(imageName);

    console.log("CAR FETCHED....")
    console.log(car);

    const getObjectParams = {
        Bucket: bucketName,
        Key: `${car.image_name}.jpg`,
    };
    const command = new GetObjectCommand(getObjectParams);
    const url = await getSignedUrl(s3, command, { expiresIn: 3600 });


    car.httpURL = url;
    
    res.render('car_picture', {
        car: car
    })
});

carsRouter.post("/cars/:imageName", async (req, res) => {
    const imageName = req.params.imageName;

    await deleteCarByImageName(imageName)

    res.redirect("/cars")
});