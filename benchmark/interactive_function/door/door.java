public class door {
    public static void main(String[] args) {
        final int n = 1000000;
        boolean[] doors = new boolean[n + 1];

        for (int pass = 1; pass <= n; pass++) {
            for (int d = pass; d <= n; d += pass) {
                doors[d] = !doors[d];
            }
        }

        int openCount = 0;
        for (int i = 1; i <= n; i++) {
            if (doors[i]) {
                openCount++;
            }
        }
        System.out.println("Open doors: " + openCount);
    }
}
