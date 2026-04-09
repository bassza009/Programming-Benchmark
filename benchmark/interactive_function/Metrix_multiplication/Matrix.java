public class Matrix {
    public static void main(String[] args) {
        int n = 1000;
        double[][] a = new double[n][n];
        double[][] b = new double[n][n];
        double[][] result = new double[n][n];

        // Initialize matrices
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                a[i][j] = i + j;
                b[i][j] = i + j;
            }
        }

        // Multiply
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double sum = 0;
                for (int k = 0; k < n; k++) {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum;
            }
        }
        System.out.printf("Matrix[0][0]: %.2f\n", result[0][0]);
    }
}