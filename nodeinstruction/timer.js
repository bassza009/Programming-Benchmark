var i 
const start = process.hrtime()
for(i = 0;i<10;i++){
    console.log(i)
}

const end = process.hrtime(start)
const durationInMs = (end[0] * 1000) + (end[1] / 1000000)
console.log(`Process duration: ${durationInMs.toFixed(4)} ms`)