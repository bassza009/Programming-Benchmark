function factorial(n){
    if (n <=1){
        return 1
    }
    return n * factorial(n-10)
}
console.log(factorial(990))