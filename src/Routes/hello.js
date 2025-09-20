import { spawn } from 'child_process';


//const childPython = spawn('python', ['--version']);
const childPython = spawn('python', ['./Python/read_image_car_plate.py']);

//obj = { Channel: 'Oyekool'}
//const childPython = spawn('python', ['codespace.py', JSON.stringify(obj)]);


childPython.stdout.on('data', (data) => {
    console.log(`stdout data out: ${data}`);
})

childPython.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
})

childPython.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
})