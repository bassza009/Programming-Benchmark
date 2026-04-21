public class fibonacci {
    public static int fibo_nacci(int n){
        if(n <= 1){
            return n;
        }
        return fibo_nacci(n-1) + fibo_nacci(n-2);
    }
    public static void main (String[] args){
        System.out.println(fibo_nacci(50));
    }
}
