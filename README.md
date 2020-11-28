# fibonacci-heap
Playing around to procrastinate my job search.

In class we learned that Dijkstra's Algorithm can run in 
```math
\Theta(|E| + |V|\log |V|)
```
using a fibonacci heap and left it at that, using that bound as the runtime for all of our shortest path problems. 
But what is a fibonacci heap? Well it was [first described](https://www.cl.cam.ac.uk/teaching/1112/AlgorithII/1987-FredmanTar-fibonacci.pdf) by Fredman and Tarjan
in 1984 (shoutout to the first *Dune* movie). I got my description of them from chapter 19 of *Introduction to Algorithms, 3rd Edition* by Cormen, Liersen, Rivest, and Stein.
A fibonnaci heap is "a collection of rooted trees that are min-heap ordered." The rootlist is a double linked list, and each group of siblings is part of its own
double linked list as well. We store a pointer to the min for easy access, and each child node points to its parent. Each parent has a pointer to one of its children, doesn't
really matter which. The order of the trees doesn't matter either. The crucial part is that the upper bound of the degree of every node is
```math
\log_a (|V|)
```
where a is the golden ratio.  The size of a subtree rooted in a node of degree k is at least $F_{k+2}$, where F_{k} is the kth Fibonacci number. When we extract the minimum, we just pull out all of its children into the top level root list and then consolidate all the roots so that each one
has its own distinct degree. The amortized time complexity of extracting a minimum is then
```math
\O(\log n)
```
which is really solid, although [in practice](https://arxiv.org/pdf/1403.0252.pdf) it doesn't really do that well compared to *d*-ary heaps.

Here are some quotes about how complicated they are:

>From a practical point of view, however, the constant factors and programming complexity of Fibonacci heaps make them less desirable than ordinary binary (or k-ary) heaps for most applications, except for certain applications that manage large amounts of data. Thus, Fibonacci heaps are predominantly of theoretical interest. If a much simpler data structure with the same amortized time bounds as Fibonacci heaps were developed, it would be of practical use as well.

> -- <cite>Cormen, Thomas H., Et Al. Introduction to Algorithms, third edition. MIT Press. Kindle Edition. </cite>


> Although theoretically efficient, fibonacci heaps are complicated to implement and not as fast in practice as other kinds of heaps

> -- [The Pairing Heap: A new form of self-adjusting heap](https://www.cs.cmu.edu/~sleator/papers/pairing-heaps.pdf)


>[Awful Linked Lists] are the main reason fibonacci heaps are so complex

> -- [Standford CS116 slides on Fibonacci Heaps](http://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/09/Small09.pdf)


> There is a better solution using Fibonacci Heaps, which is a data structure we are not going to talk about here... O( m log n) is the best run time you can do.
> -- Debmalya Panigrahi, Duke CS330 lecture, Fall 2020

##For when I have more time:
- write out proof of run time
- Implement Dijkstra's
- Strict Fibonacci Heap's and other types of heaps
- comparison pf algorithms on road data
