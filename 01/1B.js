const fs = require('fs');

const data = fs.readFileSync('data.txt', 'utf8');

function getSumOfCalibrationValues(data) {
    const lines = extractNumbers(data);
    let total = 0;
    lines.map(line => {
      const digits = line.replace(/\D/g, '');
      const firstDigit = digits[0];
      const lastDigit = digits[digits.length - 1];
      const sum = Number(firstDigit + lastDigit);
      total += sum;
    });
  
    return total;
  }
  
  function extractNumbers(data) {
  
  
    const copy = {
      'one': 'o1e',
      'two': 't2o',
      'three': 't3e',
      'four': 'f4r',
      'five': 'f5e',
      'six': 's6x',
      'seven': 's7n',
      'eight': 'e8t',
      'nine': 'n9e'
    };
  
    Object.keys(copy).forEach(key => {
      data = data.replaceAll(key, copy[key]);
    });
  
    return data.split('\n');
  }
  
  console.log(`the total is: ${getSumOfCalibrationValues(data)}`);