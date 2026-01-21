import mysql from "mysql2";

import dotenv from 'dotenv'
dotenv.config()

const pool = mysql.createPool({
    host: process.env.HOST,
    user: process.env.USER,
    password: process.env.PASSWORD,
    database: process.env.DATABASE
}).promise()

export async function getCars() {
    const [rows] = await pool.query("SELECT * FROM Cars")
    return rows
}

export async function getCarByImageName(imageName) {
    const[row] = await pool.query("SELECT * FROM Cars Where image_name = ?", [imageName])
    return row[0] || null;
}

export async function deleteCarByImageName(imageName) {
    const[row] = await pool.query("DELETE FROM Cars Where image_name = ?", [imageName])
}