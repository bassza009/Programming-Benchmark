import java.util.concurrent.ThreadLocalRandom;

public class prisoners{
    public static double playOptimal(int n) {
        int pardoned = 0;
        int[] inDrawer = new int[100];
        for (int i = 0; i < 100; i++) inDrawer[i] = i;

        for (int r = 0; r < n; r++) {
            // Shuffle
            for (int i = 99; i > 0; i--) {
                int index = ThreadLocalRandom.current().nextInt(i + 1);
                int a = inDrawer[index];
                inDrawer[index] = inDrawer[i];
                inDrawer[i] = a;
            }

            boolean allFound = true;
            for (int prisoner = 0; prisoner < 100; prisoner++) {
                boolean found = false;
                int reveal = prisoner;
                for (int go = 0; go < 50; go++) {
                    if (inDrawer[reveal] == prisoner) {
                        found = true;
                        break;
                    }
                    reveal = inDrawer[reveal];
                }
                if (!found) {
                    allFound = false;
                    break;
                }
            }
            if (allFound) pardoned++;
        }
        return (double) pardoned / n * 100;
    }

    public static void main(String[] args) {
        int n = 1000000;
      System.out.printf("Optimal play wins (Java): %.1f%%\n", playOptimal(n));
    }
}