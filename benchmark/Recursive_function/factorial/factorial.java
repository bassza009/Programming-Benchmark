public class factorial {
    public static double computeFactorial(int n) {
        if (n <= 1) {
            return 1.0;
        }
        return (double) n * computeFactorial(n - 1);
    }

    public static void main(String[] args) {
        final int n = 100;
        System.out.printf("%.6e\n", computeFactorial(n));
    }
}
