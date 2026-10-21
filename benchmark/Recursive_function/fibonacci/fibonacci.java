public class fibonacci {
    public static long computeFibonacci(long n) {
        if (n <= 1L) {
            return n;
        }
        return computeFibonacci(n - 1L) + computeFibonacci(n - 2L);
    }

    public static void main(String[] args) {
        final long n = 40L;
        System.out.println(computeFibonacci(n));
    }
}
