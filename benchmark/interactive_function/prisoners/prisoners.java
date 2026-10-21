public class prisoners {
    public static double playOptimal(int n) {
        int pardoned = 0;
        int[] inDrawer = new int[100];
        for (int i = 0; i < 100; i++) {
            inDrawer[i] = i;
        }

        long seed = 42L;

        for (int r = 0; r < n; r++) {
            for (int i = 99; i > 0; i--) {
                seed = (seed * 1664525L + 1013904223L) & 0x7fffffffL;
                int j = (int) (seed % (i + 1));
                int temp = inDrawer[i];
                inDrawer[i] = inDrawer[j];
                inDrawer[j] = temp;
            }

            boolean allFound = true;
            for (int prisoner = 0; prisoner < 100; prisoner++) {
                boolean found = false;
                int reveal = prisoner;
                for (int step = 0; step < 50; step++) {
                    int card = inDrawer[reveal];
                    if (card == prisoner) {
                        found = true;
                        break;
                    }
                    reveal = card;
                }
                if (!found) {
                    allFound = false;
                    break;
                }
            }
            if (allFound) {
                pardoned++;
            }
        }
        return ((double) pardoned / n) * 100.0;
    }

    public static void main(String[] args) {
        final int n = 1000000;
        System.out.printf("Optimal play wins: %.4f%%\n", playOptimal(n));
    }
}
