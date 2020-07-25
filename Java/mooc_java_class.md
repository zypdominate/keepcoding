####  1. 对象初始化

**构造函数**

- 如果有一个成员函数的名字和类的名字完全相同，则在创建这个类的每一个对象的时候会自动调用这个函数；
- 这个函数不能有返回类型；

**重载**

- 一个类可以有多个构造函数，只要它们的参数表不同；
- 创建对象的时候给出不同的参数值，就会自动调用不同的构造函数；
- 通过 `this()` 还可以调用其他构造函数；
- 一个类的同名但参数表不同的函数构成了重载关系；

```java
package mooc_java.class_object;

public class VendingMachine {
    int price = 10;
    int balance;
    int total;

    // 构造函数
    VendingMachine() {
        total = 1;
    }

    // 重载
    VendingMachine(int price) {
        this.price = price;
    }

    void showPrompt() {
        System.out.println("welcome to VendingMachine");
    }

    void setPrice(int price) {
        this.price = price;
    }

    void insertMoney(int amount) {
        balance += amount;
    }

    void showBalance() {
        System.out.println(balance);
    }

    void getFood() {
        if (balance >= price) {
            System.out.println("Here you are");
            balance = balance - price;
            total = total + price;
            showBalance();
        }
    }

    public static void main(String[] args) {
        // 创建对象
        VendingMachine vm = new VendingMachine();
        // 对象变量是对象的管理者
        vm.showPrompt();
        vm.showBalance();
        vm.setPrice(20);
        vm.insertMoney(100);
        vm.getFood();

        VendingMachine vm2 = new VendingMachine(100);
    }
}
```

相关代码见：[class_object](https://gitee.com/zypdominate/keeplearning/tree/master/myLearning/learningJava/src/mooc_java/class_object)

---

#### 2. 对象交互

对象 = 属性 + 服务

- 数据： 属性或状态
- 操作：函数

把数据和对数据的操作放在一起 ——> 封装。

private：只有这个类内部可以访问

- 类内部指 类的成员函数 和 定义初始化；
- 这个限制是对类的，而不是对对象的；

public：任何人都可以访问

- 任何人指的是 在任何类的函数或定义初始化中可以使用；
- 使用指的是 调用、访问或定义变量；

相关代码见：[clock](https://gitee.com/zypdominate/keeplearning/tree/master/myLearning/learningJava/src/mooc_java/clock)

---

#### 3. 容器类

eg: `ArrayList<String> strings = new ArrayList<String>();`、 `HashSet<String> stringHashSet = new HashSet<String>();`

容器类有两个类型：

- 容器的类型
- 元素的类型

---

######  (1). 顺序容器：

即放进容器中的对象是按照指定的顺序（放的顺序）排列起来的，而且允许具有相同值的多个对象存在。

```java
package mooc_java.object_container;

import java.util.ArrayList;

public class NoteBook {
    // 用来存放String类型的ArrayList (容器类)
    private ArrayList<String> notes = new ArrayList<String>();

    public void add(String s) {
        notes.add(s);
    }

    public void add(String s, int location) {
        notes.add(location, s);
    }

    public int getSize() {
        return notes.size();
    }

    public String getNote(int index) {
        return notes.get(index);
    }

    public void removeNote(int index) {
        notes.remove(index);
    }

    public String[] list() {
        String[] a = new String[notes.size()];
//        for (int i = 0; i < notes.size(); i++) {
//            a[i] = notes.get(i);
//        }
        notes.toArray(a);
        return a;
    }

    public static void main(String[] args) {
        NoteBook nb = new NoteBook();
        nb.add("one");
        nb.add("two");
        nb.add("three", 1);
        System.out.println(nb.getSize());
        System.out.println(nb.getNote(1));
        nb.removeNote(0);

        String[] nb_list = nb.list();
        for (String item : nb_list) {
            System.out.println(item);
        }

    }
}
```

---

###### (2). 对象数组

当数组的元素的类型是类的时候，数组的每一个元素其实只是对象的管理者而不是对象本身。因此，仅仅创建数组并没有创建其中的每一个对象！

即当创建了一个元素是类的数组后，那些对象还没有产生，还需要再去创建里面的每个对象。

```java
    public static void main(String[] args) {
        String[] a = new String[10];
        System.out.println(a[0]);
        System.out.println(a[0]+"aaa");
        System.out.println(a[0].length());
    }
/* 输出结果：
null
nullaaa
Exception in thread "main" java.lang.NullPointerException
	at mooc_java.notebook.NoteBook.main(NoteBook.java:55)
*/

    public static void main(String[] args) {
        String[] a = new String[10];
        System.out.println(a[0]);
        for (int i = 0; i < a.length; i++) {
            a[i] = "" + i;
        }
        System.out.println(a[0].length());
    }
/* 输出结果：
null
1
*/
```

对象数组的for-each循环:

```java
package mooc_java.object_container;

class Value {
    private int i;

    public void set(int i) {
        this.i = i;
    }

    public int get() {
        return i;
    }

    // 任何java类，只要实现了String toString函数，
    // 可以通过System.out.println(类Value的对象)来输出
    public String toString() {
        return i + "";
    }
}

public class objectArray {
    // int类型的数组循环
    public static void int_array(int[] array) {
        for (int i = 0; i < array.length; i++) {
            array[i] = i;
        }
        for (int k : array) {
//            System.out.println(k);
            k = 0;
        }
        for (int k : array) {
            System.out.print(k);
        }
    }

    // 对象数组的for-each循环
    public static void object_array(Value[] values) {
        for (int i = 0; i < values.length; i++) {
            values[i] = new Value();
            values[i].set(i);
        }
        for (Value v : values) {
            v.set(0);
        }
        for (Value v : values) {
//            System.out.print(v.get() + " ");
            System.out.print(v);
        }
    }

    public static void main(String[] args) {
        // int类型的数组循环
        int[] array = new int[10];
        int_array(array);
        System.out.println("\t");

        // 对象数组的for-each循环
        Value[] values = new Value[10];
        object_array(values);
    }
}

/*
输出结果：
0123456789	
0000000000
*/
```

---

###### (3). 集合容器(Set)：

集合就是数学中的集合的概念：所有的元素都具有唯一的值，元素在其中没有顺序。

```java
package mooc_java.object_container;

import java.util.ArrayList;
import java.util.HashSet;

public class container {
    public static void main(String[] args) {
        ArrayList<String> strings = new ArrayList<String>();
        strings.add("one");
        strings.add("two");
        strings.add(1, "one");
        System.out.println(strings);

        HashSet<String> stringHashSet = new HashSet<String>();
        stringHashSet.add("one");
        stringHashSet.add("two");
        stringHashSet.add("one");
        System.out.println(stringHashSet);
    }
}

/*
[one, one, two]
[one, two]
*/
```

---

###### (4). 散列表(Hash)

传统意义上的Hash表，是能以int做值，将数据存放起来的数据结构。Java的Hash表可以以任何实现了hash()函数的类的对象做值来存放对象。

Hash表是非常有用的数据结构，熟悉它，充分使用它，往往能起到事半功倍的效果。

```java
package mooc_java.object_container;

import java.util.HashMap;
import java.util.Scanner;

public class Coin {
    // hash表
    private HashMap<Integer, String> coinnames = new HashMap<Integer, String>();

    public Coin() {
        coinnames.put(1, "penny");
        coinnames.put(5, "dime");
        coinnames.put(25, "quarter");
        coinnames.put(50, "half-dollar");
        System.out.println(coinnames);
    }

    public String getName(int amount) {
        return coinnames.getOrDefault(amount, "NOT FOUND");
    }

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int amount = in.nextInt();

        Coin coin = new Coin();
        String name = coin.getName(amount);
        System.out.println(name);

        // 遍历hash表
        for (Integer key : coin.coinnames.keySet()) {
            String s = coin.coinnames.get(key);
            System.out.println(s);
        }
    }
}
```

