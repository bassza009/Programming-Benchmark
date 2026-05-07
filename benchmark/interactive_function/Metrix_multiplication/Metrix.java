public class Metrix {
    public static void main(String[] args) {
        int n = 1000;
        double[] a = new double[n * n];
        double[] b = new double[n * n];
        double[] result = new double[n * n];

        // Initialize matrices
        for (int i = 0; i < n * n; i++) {
            a[i] = i % n;
            b[i] = i / n;
        }

        System.out.println("Starting Matrix Multiplication (Java - Flat): " + n + "x" + n);
        // long start = System.currentTimeMillis();

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double sum = 0;
                for (int k = 0; k < n; k++) {
                    // สูตร: (row * N) + col
                    sum += a[i * n + k] * b[k * n + j];
                }
                result[i * n + j] = sum;
            }
        }

        // long end = System.currentTimeMillis();
        System.out.printf("Sample Result [0]: %.2f\n", result[0]);
        // System.out.println("Time: " + (end - start) / 1000.0 + " sec");
    }
}