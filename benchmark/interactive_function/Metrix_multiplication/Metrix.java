public class MatrixBench {
    public static void main(String[] args) {
        int n = 1000;
        double[] a = new double[n * n];
        double[] b = new double[n * n];
        double[] res = new double[n * n];

        for (int i = 0; i < n * n; i++) {
            a[i] = (double) (i % n);
            b[i] = (double) (i / n);
        }

        System.out.printf("Starting Matrix Multiplication (Java): %dx%d\n", n, n);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double sum = 0;
                for (int k = 0; k < n; k++) {
                    sum += a[i * n + k] * b[k * n + j];
                }
                res[i * n + j] = sum;
            }
        }
        System.out.printf("Sample Result [0]: %.6f\n", res[0]);
    }
}