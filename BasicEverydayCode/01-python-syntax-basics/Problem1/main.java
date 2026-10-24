/*

Task: Write a program that:
1. Creates a variable age and assigns it 22.
2. Checks whether age is greater than or equal to 18.
3. If true, prints Adult.
4. Otherwise, prints Minor.
5. Prints Program completed after the condition, regardless of the result.


*/

class Main {
    public static void main(String[] args) {
        int age = 22;

        if (age >= 18)
            System.out.println("Adult");
        else
            System.out.println("Minor");

        System.out.println("Program completed");
    }
}