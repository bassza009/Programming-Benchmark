public class prime {
    public static int countPrimes(int limit) {
        int count = 0;
        for (int i = 2; i <= limit; i++) {
            boolean isPrime = true;
            for (int j = 2; j * j <= i; j++) {
                if (i % j == 0) {
                    isPrime = false;
                    break;
                }
            }
            if (isPrime) {
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        final int n = 1000000;
        int result = countPrimes(n);
        System.out.println("Primes count: " + result);
    }
}
