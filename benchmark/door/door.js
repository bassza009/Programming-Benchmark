
const start = process.hrtime()
for (var door = 1; door <= 100; door++) {
  var sqrt = Math.sqrt(door);
  if (sqrt === (sqrt | 0)) {
    console.log("Door %d is open", door);
  }
}
const end = process.hrtime(start)
const durationInMs = (end[0] * 1000) + (end[1] / 1000000)
console.log(`Process duration : ${durationInMs}`)