import { Router } from "express";
import multer from "multer"

import fs from "fs/promises"
import path from "path"

import { startImageDetectionProcess, processActive } from "./child_process.js";


const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'Python/videos')
  },
  filename: function (req, file, cb) {
    //const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9)
    const ext = path.extname(file.originalname);
    //const base = path.basename(file.originalname, ext)
    cb(null, 'cars2' + ext)
  }
})

const upload = multer({ storage: storage })

const clearVideosMiddleware = async (req, res, next) => {
    const directory = "Python/videos"
    try{
        for (const file of await fs.readdir(directory)) {
            await fs.unlink(path.join(directory, file));
        }
    } catch {
        res.send("<h1>Resource is busy</h1><a href='/'>Go back</a>");
    }
    
    console.log("Videos folder empty")

    next();
}


export const videoStreamRouter = Router()


videoStreamRouter.post('/',clearVideosMiddleware, upload.single('file'), (req, res) => {
    //req.avatar
    if (processActive == false) {
        startImageDetectionProcess();
        res.send("Uploaded successfully! Process started.");
    } else {
        res.send("A process is already running")
    }
})