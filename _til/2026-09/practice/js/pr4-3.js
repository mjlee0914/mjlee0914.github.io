// 4-3-1 나만의 도서 카드 만들기
const book = {};

book.title = '자바스크립트 기초';
book.price = 20000;
book.quantity = 5;

book.totalPrice = function getSum() {
    return this.price * this.quantity;
};

book.quantity = 25000;
//console.log(book.totalPrice());
delete book.quantity;

//console.log(book);


// 4-3-2 맛집 대기열 제어 프로그램

let waitingList = ["철수", "영희", "민수"];

waitingList.push("지수");
waitingList.unshift("정우"); //배열 맨 앞에 추가

let subList = waitingList.slice(1,3);

//console.log(waitingList.join('/'));
//console.log(subList);
//console.log(waitingList);
//console.log(waitingList.length);

// 4-3-3 행운의 번호 추첨기

// Math.floor(): 소수점 이하 무조건 버림. Math.random(): 0~1 사이의 랜덤 소수 반환
let luckyNumber = Math.floor(Math.random() * 10) + 1;

console.log(luckyNumber);

let luckyMember = {
    number: luckyNumber,
};

// JSON.stringfy(value, replacer, space)
// value: JSON으로 바꿀 대상
// replacer: 어떤 값을 넣을지 선택/수정, 함수도 가능
// space: 들여쓰기, 보기 좋게 수정
const serializedMember = JSON.stringify(luckyMember, null, 2);
console.log(typeof(serializedMember));
console.log(serializedMember);
