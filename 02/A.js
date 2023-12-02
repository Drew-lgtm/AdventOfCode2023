const fs = require('fs');

const data = fs.readFileSync('./data.txt', 'utf8');

const RED_CUBES_MAX = 12;
const GREEN_CUBES_MAX = 13;
const BLUE_CUBES_MAX = 14;
const file = './data2.txt';
const lines = fs.readFileSync(file, 'utf-8').trim().split('\n');

function subdivideGameInfo(lines) {
	let sum = 0;
	let powers = 0;
	let sumPowers = 0;
	for (const line of lines) {
		const splitLine = line.split(':');
		const id = Number(splitLine[0].trim().substring(5));
		const rounds = splitLine[1].split(';');
		let possible = true;
		const reds = [];
		const greens = [];
		const blues = [];

		for (let i = 0; i < rounds.length; i++) {
			const colorCountPairs = rounds[i].split(',');
			for (const pair of colorCountPairs) {
				const splitPair = pair.trim().split(' ');
				const count = Number(splitPair[0]);
				const color = splitPair[1];
				if (color === 'red') {
					if (count > RED_CUBES_MAX) {
						possible = false;
					}
					reds.push(count);
				} else if (color === 'green') {
					if (count > GREEN_CUBES_MAX) {
						possible = false;
					}
					greens.push(count);
				} else if (color === 'blue') {
					if (count > BLUE_CUBES_MAX) {
						possible = false;
					}
					blues.push(count);
				}
			}
		}

		if (possible) {
			sum += id;
		}

		const minReds = Math.max(...reds);
		const minGreens = Math.max(...greens);
		const minBlues = Math.max(...blues);

		powers = minReds * minGreens * minBlues;
		sumPowers += powers;
	}
	console.log(`Part1: ${sum}`);
	console.log(`Part2: ${sumPowers}`);
}

subdivideGameInfo(lines);