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
    "HIYAHHH"
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