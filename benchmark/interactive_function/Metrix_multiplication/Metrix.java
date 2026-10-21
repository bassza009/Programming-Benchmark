public class Metrix {
    public static void main(String[] args) {
        final int n = 1000;
        double[] a = new double[n * n];
        double[] b = new double[n * n];
        double[] result = new double[n * n];

        for (int i = 0; i < n * n; i++) {
            a[i] = (double) (i % n);
            b[i] = (double) (i / n);
        }

        for (int i = 0; i < n; i++) {
            int rowOffset = i * n;
            for (int j = 0; j < n; j++) {
                double sum = 0.0;
                for (int k = 0; k < n; k++) {
                    sum += a[rowOffset + k] * b[k * n + j];
                }
                result[rowOffset + j] = sum;
            }
        }

        System.out.printf("Sample Result [0]: %.2f\n", result[0]);
    }
}
