public class factorial {
    public static int facto_rial(int n){
        if(n<=1){
            return 1;
        }
        return n * facto_rial(n-1);

    }
    public static void main(String[] args){
        System.out.println(facto_rial(990));

    }
}
