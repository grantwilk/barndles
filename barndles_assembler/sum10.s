// file:    sum10.s
// author:  Grant Wilk
// created: April 10, 2020
// updated: April 10, 2020
// brief:   Sums all numbers from 10 down to 0.

.section read-only

    // test variable
    test_four:
    .arr 10 0c01

    // the starting summation value
    start_val:
    .int 10

    // test_variable
    test_one:
    .int 100

    // test variable
    test_two:
    .int 0x20

    // test variable
    test_tree:
    .int 0b1010

    // test variable
    test_five:
    .arr 10 0xFF

    // test_variable
    test_six:
    .arr 3 0b1010


.section read-write

    // flag that gets set high once the summation completes
    finished_flag:
    .int 0x00


.section instruction

    // load the start value into R1
    // LDR R1, start_val
    MOV R1, #0x0A

    // main loop
    loop:

        // add R1 to R0
        ADD R0, R0, R1

        // decrement R1
        SUB R1, #1

        // if R1 is greater than zero, loop
        CPS R1, #0
        BGT loop

    // set the finished flag
    // MOV R1, #1
    // STR R1, finished_flag

    // loop forever
    stop:
        BCH stop