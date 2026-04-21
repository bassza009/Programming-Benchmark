import java.util.*;

public class prisoners {
    public static void main(String[] args) {
        int trials = 1000000;
        runTrial(trials, "random");
        runTrial(trials, "optimal");
    }

    public static void runTrial(int trials, String strategy) {
        int pardonedCount = 0;
        Random rand = new Random();
        int[] drawers = new int[100];

        for (int t = 0; t < trials; t++) {
            for (int i = 0; i < 100; i++) drawers[i] = i;
            shuffle(drawers, rand);

            boolean allFound = true;
            for (int p = 0; p < 100; p++) {
                if (!findCard(p, drawers, strategy, rand)) {
                    allFound = false;
                    break;
                }
            }
            if (allFound) pardonedCount++;
        }
        double rate = (double) pardonedCount / trials * 100;
        System.out.printf("Strategy: %-7s | Success Rate: %.2f%%\n", strategy, rate);
    }

    private static boolean findCard(int prisoner, int[] drawers, String strategy, Random rand) {
        if (strategy.equals("optimal")) {
            int next = prisoner;
            for (int i = 0; i < 50; i++) {
                if (drawers[next] == prisoner) return true;
                next = drawers[next];
            }
        } else {
            List<Integer> choices = new ArrayList<>();
            for (int i = 0; i < 100; i++) choices.add(i);
            Collections.shuffle(choices);
            for (int i = 0; i < 50; i++) {
                if (drawers[choices.get(i)] == prisoner) return true;
            }
        }
        return false;
    }

    private static void shuffle(int[] array, Random rand) {
        for (int i = array.length - 1; i > 0; i--) {
            int index = rand.nextInt(i + 1);
            int temp = array[index];
            array[index] = array[i];
            array[i] = temp;
        }
    }
}
