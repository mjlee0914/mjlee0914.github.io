// 4-2-1

let leftCup = "주스";
let rightCup = "우유";
let emptyCup = leftCup;
leftCup = rightCup;
rightCup = emptyCup;

//console.log("leftCup:", leftCup);
//console.log("rightCup:", rightCup);
//console.log("emptyCup:", emptyCup);


// 4-2-2

let enteredAge = "19";
//console.log(typeof(enteredAge)); // string
let requiredAge = 19;
//console.log(requiredAge === enteredAge);
enteredAge = 19;
//console.log(requiredAge === enteredAge);
const isEligible = (requiredAge === enteredAge) && (enteredAge >= requiredAge);
//console.log(isEligible);


// 4-2-3

let currentYear = 2028;
console.log (currentYear % 4 === 0);
currentYear += 2;
console.log(currentYear);
console.log (currentYear % 4 === 0);