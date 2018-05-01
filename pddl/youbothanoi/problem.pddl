(define (problem hanoi)
(:domain hanoi)
(:objects
table1
table2
table3
disk1
disk2
disk3
)
(:init
(clear disk1)
(clear table2)
(clear table3)
(on disk3 table1)
(on disk1 disk2)
(on disk2 disk3)
(smaller disk1 table1)
(smaller disk1 table2)
(smaller disk1 table3)
(smaller disk2 table1)
(smaller disk2 table2)
(smaller disk2 table3)
(smaller disk3 table1)
(smaller disk3 table2)
(smaller disk3 table3)
(smaller disk1 disk3)
(smaller disk2 disk3)
(smaller disk3 disk3)
(smaller disk1 disk2)
(smaller disk2 disk2)
(smaller disk1 disk1)
)
(:goal (and
(on disk1 disk2)
(on disk2 disk3)
(on disk3 table3)
)))
