(define (problem hanoi)
(:domain hanoi)
(:objects
table1
table2
table3
disk1
disk2
disk3
disk4
disk5
disk6
disk7
disk8
)
(:init
(clear disk1)
(clear table2)
(clear table3)
(on disk8 table1)
(on disk1 disk2)
(on disk2 disk3)
(on disk3 disk4)
(on disk4 disk5)
(on disk5 disk6)
(on disk6 disk7)
(on disk7 disk8)
(smaller disk1 table1)
(smaller disk1 table2)
(smaller disk1 table3)
(smaller disk2 table1)
(smaller disk2 table2)
(smaller disk2 table3)
(smaller disk3 table1)
(smaller disk3 table2)
(smaller disk3 table3)
(smaller disk4 table1)
(smaller disk4 table2)
(smaller disk4 table3)
(smaller disk5 table1)
(smaller disk5 table2)
(smaller disk5 table3)
(smaller disk6 table1)
(smaller disk6 table2)
(smaller disk6 table3)
(smaller disk7 table1)
(smaller disk7 table2)
(smaller disk7 table3)
(smaller disk8 table1)
(smaller disk8 table2)
(smaller disk8 table3)
(smaller disk1 disk8)
(smaller disk2 disk8)
(smaller disk3 disk8)
(smaller disk4 disk8)
(smaller disk5 disk8)
(smaller disk6 disk8)
(smaller disk7 disk8)
(smaller disk8 disk8)
(smaller disk1 disk7)
(smaller disk2 disk7)
(smaller disk3 disk7)
(smaller disk4 disk7)
(smaller disk5 disk7)
(smaller disk6 disk7)
(smaller disk7 disk7)
(smaller disk1 disk6)
(smaller disk2 disk6)
(smaller disk3 disk6)
(smaller disk4 disk6)
(smaller disk5 disk6)
(smaller disk6 disk6)
(smaller disk1 disk5)
(smaller disk2 disk5)
(smaller disk3 disk5)
(smaller disk4 disk5)
(smaller disk5 disk5)
(smaller disk1 disk4)
(smaller disk2 disk4)
(smaller disk3 disk4)
(smaller disk4 disk4)
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
(on disk3 disk4)
(on disk4 disk5)
(on disk5 disk6)
(on disk6 disk7)
(on disk7 disk8)
(on disk8 table3)
)))
