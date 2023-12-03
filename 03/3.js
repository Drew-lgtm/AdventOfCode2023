import * as R from 'ramda';

import { readString } from '../util/file';
import { indexedReduce, indexedMap, indexedChain } from '../util/ramda';


const isDigit = R.both(
  R.gte(R.__, '0'),
  R.lte(R.__, '9')
);

const isSymbol = R.allPass([
  R.complement(isDigit),
  R.complement(R.equals('.')),
  R.complement(R.is(Object))
]);

const isGear = R.equals('*');

const onlyNumberNeighbours = R.filter(R.is(Object));

const onlyUniqueNeighbours = R.uniqBy(R.prop('id'));

const newSearchAccumulator = () => ({ value: '', numbers: [] });


const getCell = (dx, dy) => (x, y) => engine => {
  const newX = R.add(dx, x);
  const newY = R.add(dy, y);
  return R.path([newY, newX], engine);
};

const left = getCell(-1, 0);
const right = getCell(1, 0);
const top = getCell(0, -1);
const bottom = getCell(0, 1);
const leftTop = getCell(-1, -1);
const rightTop = getCell(1, -1);
const leftBottom = getCell(-1, 1);
const rightBottom = getCell(1, 1);

const getNeighbours = R.juxt([
  leftTop, top, rightTop,
  right, rightBottom, bottom,
  leftBottom, left
]);

const processCell = (cellPredicate, processNeighbours) => (y, engine) => (cell, x) =>
  R.ifElse(
    () => cellPredicate(cell),
    () => {
      const neighbours = R.juxt(getNeighbours(x, y))(engine);
      return processNeighbours ? processNeighbours(neighbours) : neighbours;
    },
    R.always([])
  )();

const processGearNeighbours = R.pipe(
  onlyNumberNeighbours,
  onlyUniqueNeighbours,
  R.ifElse(
    R.pipe(R.length, R.equals(2)),
    R.identity,
    R.always([])
  )
);

const processGearCell = R.pipe(
  onlyNumberNeighbours,
  R.pluck('value'),
  R.ifElse(
    R.isEmpty,
    R.always(0),
    R.reduce(R.multiply, 1)
  )
);

const findSymbolNeighbours = (engine) =>
  indexedChain((row, y) =>
    indexedMap(processCell(isSymbol, R.identity)(y, engine), row),
    engine
  );

const findGears = (engine) =>
  indexedChain((row, y) =>
    indexedMap(processCell(isGear, processGearNeighbours)(y, engine), row),
    engine
  );


const searchNumbers = indexedReduce((acc, char, index, arr) => {
  return R.cond([
    [() => !isDigit(char) && acc.value, () => {
      acc.numbers.push({ index, value: acc.value });
      acc.value = '';
      return acc;
    }],

    [() => isDigit(char), () => {
      acc.value += char;

      if (index === arr.length - 1) {
        acc.numbers.push({ index: index + 1, value: acc.value });
        acc.value = '';
      }

      return acc;
    }],

    [R.T, () => acc]
  ])(char);
});

const numerizeEngineLine = (engineLine, lineIndex) => {
  const numbersStr = searchNumbers(newSearchAccumulator(), engineLine);
  let numerizedLine = [...engineLine];

  R.forEach(numberStr => {
    const number = parseInt(numberStr.value);
    const id = `${lineIndex}-${numberStr.index}`;
    const startIndex = numberStr.index - numberStr.value.length;

    R.forEach(i => {
      numerizedLine[i] = { id, value: number };
    }, R.range(startIndex, numberStr.index));
  }, numbersStr.numbers);

  return numerizedLine;
}

const parseEngine = R.pipe(
  R.split('\n'),
  indexedMap(numerizeEngineLine),
);

const getSymbolNeighboursSum = R.pipe(
  findSymbolNeighbours,
  R.flatten,
  onlyNumberNeighbours,
  onlyUniqueNeighbours,
  R.pluck('value'),
  R.sum
);

const getGearRationsSum = R.pipe(
  findGears,
  R.map(processGearCell),
  R.sum
);


const sumOfSymbolNeighbours = R.pipe(
  parseEngine,
  getSymbolNeighboursSum
);

const sumOfGearRatios = R.pipe(
  parseEngine,
  getGearRationsSum
);

export async function sumOfAdjacentNumbersInEngine() {
  const engine = await readString('3/input.txt');

  console.log(
    "Day 3. Part 1. Sum of adjacent to symbols numbers in engine:",
    sumOfSymbolNeighbours(engine)
  );

  console.log(
    "Day 3. Part 2. Sum of gear ratios:",
    sumOfGearRatios(engine)
  );
}