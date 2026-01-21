import { spawn } from 'child_process';

export let processActive = false

export function startImageDetectionProcess() {
    //const childPython = spawn('python', ['--version']);
    const childPython = spawn('python', ['./Python/main.py']);

    //obj = { Channel: 'Oyekool'}
    //const childPython = spawn('python', ['codespace.py', JSON.stringify(obj)]);


    childPython.stdout.on('data', (data) => {
        processActive = true
        console.log(`stdout data out: ${data}`);
    })

    childPython.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    })

    childPython.on('close', (code) => {
        processActive = false
        console.log(`child process exited with code ${code}`);
    })
}