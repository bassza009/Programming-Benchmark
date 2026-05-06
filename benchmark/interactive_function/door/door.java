public class door {
    
    public static void main(String[] args) {
        int n = 1000000;
        boolean[] doors = new boolean[n+1]; // false = closed, true = open

        for (int pass = 1; pass <= n; pass++) {
            for (int door = pass; door <= n; door += pass) {
                doors[door] = !doors[door];
            }
        }

        System.out.print("Open doors: ");
        for (int i = 1; i <= n; i++) {
            if (doors[i]) System.out.print("Door "+i + " : opened\n");
        }
        System.out.println("");
    }
}