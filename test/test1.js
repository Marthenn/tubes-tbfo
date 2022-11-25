function foo(a,b,c){
    for(var i=0;i<10;i++){
        console.log(i);
        if(i==5){
            break;
        } else {
            console.log('else');
        }
    }
    console.log(i);
    return a+b+c;
}

const a = 1; console.log(a);
switch(a){
    case 1:
        console.log('a is 1');
        break;
    case 2:
        console.log('a is 2');
        break;
    default:
        console.log('a is not 1 or 2');
        break;
}

delete a;
console.log(a);

let j = 0;
while(j<15){
    j++;
    if(j==5){continue}
    console.log(j);
}

try{
    console.log(j);
    if(j==5){throw 'j is 5'}
}
catch(e){
    console.log(e);
}
finally{
    console.log('finally');
}

while(true){
    console.log('infinite loop');
    break;
}

while(false){
    console.log('no loop');
}

let as = null; console.log(as);