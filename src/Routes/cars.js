import { Router } from "express";
import { getCars } from "../Config/database.js";

export const carsRouter = Router()

carsRouter.get("/cars", async (req, res) => {
    const cars = await getCars()
    res.render('home', {
        cars: cars
    })
})