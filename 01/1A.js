const fs = require('fs');

const data = fs.readFileSync('data.txt', 'utf8');

let firstDigits = [];
let lastDigits = [];
let sum = 0;

for (const item of data) {
  let firstDigit = null;
  let lastDigit = null;

  for (const char of item) {
    if (/\d/.test(char)) {
      firstDigit = char;
      break;
    }
  }

  for (let i = item.length - 1; i >= 0; i--) {
    const char = item[i];
    if (/\d/.test(char)) {
      lastDigit = char;
      break;
    }
  }

  firstDigits.push(firstDigit);
  lastDigits.push(lastDigit);

  if (firstDigit !== null && lastDigit !== null) {
    sum += parseInt(firstDigit) + parseInt(lastDigit);
  }
}

console.log(sum);