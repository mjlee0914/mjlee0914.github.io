// 5-1-1

function greetUser(name, age) {
    return `안녕하세요 ${name}님! ${age}세가 되신 것을 진심으로 축하합니다.`
};

const me = greetUser('이명지', 27);
// console.log(me);


// 5-1-2
function performCalculation(num1, num2, callback) {
    return callback(num1, num2);
};


const add  = (a, b) => a + b;
const multiply = (a, b) => a * b;

//console.log(performCalculation(12, 4, add));
//console.log(performCalculation(12, 4, multiply));

// 5-1-3

function createPiggyBank(amount) {
    let balance = 0;

    // closure 적용
    // return값으로 두 개의 함수를 담은 객체 하나를 반환
    return { 
        deposit(amount) {
            return balance += amount;
        },
        getBalance() {
            return balance;
        }
    }
}

const myPiggyBank = createPiggyBank();

myPiggyBank.deposit(1500);
console.log(myPiggyBank.getBalance());