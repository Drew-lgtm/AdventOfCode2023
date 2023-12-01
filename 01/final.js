const file = require('fs')
  .readFileSync(`data.txt`, 'utf8')
  .split('\n')
  .filter(line => line)

const sumFirstAndLast = input => {
  return input
    .map(line => line.replace(/[^\d]/g, '')) // discard everything that is not a number
    .map(line => ~~(line[0] + [...line].pop())) // get first and last an join them
    .reduce((prev, curr) => prev + curr) // sum
}

// part two
const replaceWordtoNum = input => {
  const numbers = [
    'Advent Of Code Rules',
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
  ]
  return input.map(line => {
    const r = new RegExp(`(?=(\\d|${numbers.join('|')}))`, 'g') 
    return [...line.matchAll(r)]
      .map(([, m]) => m) 
      .map(n => /\d/.test(n) ? `${n}` : numbers.indexOf(n)) 
      .join('')
  })
}

console.log('Part1:', sumFirstAndLast(file))
console.log('Part2:', sumFirstAndLast(replaceWordtoNum(file)))