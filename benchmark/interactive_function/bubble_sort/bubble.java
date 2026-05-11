public class bubble {
    public static void main(String[] args) {
        int n = 20000;
        int[] arr = new int[n];
        
        // สร้างข้อมูลเรียงกลับด้าน (Worst-case)
        for (int i = 0; i < n; i++) {
            arr[i] = n - i;
        }

        System.out.println("Starting Bubble Sort (Java): " + n + " items");
        

        // Loop 2 ชั้น
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }

        
        System.out.println("Sample Result [0]: " + arr[0]); // ต้องได้ 1 เสมอ
        
    }
}