num_ps = {
    # membrane names (labels)
    H = {m1};

    structure = [m1 ]m1;

    # membrane 1
    m1 = {
        var = {x_1_1, x_2_1, x_3_1, x_4_1, x_5_1, x_6_1, x_7_1, x_8_1, x_9_1}; # variables used in the production function
        E = {e_1_1}; # set of enzyme variables
        pr = {x_5_1 + x_1_1 - x_1_1 [e_1_1 -> ] 1|x_5_1};
        pr = {2*x_9_1*x_5_1 [e_1_1 ->] 1|x_9_1 + 1|x_1_1};
        pr = {x_6_1[e_1_1 -> ] 1|x_6_1};
        pr = {2*x_2_1*x_6_1 [e_1_1 ->] 1|x_2_1 + 1|x_1_1};
        pr = {x_7_1[e_1_1 -> ] 1|x_7_1};
        pr = {2*x_3_1*x_7_1 [e_1_1 ->] 1|x_3_1 + 1|x_1_1};
        pr = {x_8_1[e_1_1 -> ] 1|x_8_1};
        pr = {2*x_4_1*x_8_1 [e_1_1 ->] 1|x_4_1 + 1|x_1_1};
        var0 = (0, 1, 1, 1, 12, 16, 2, 5, 1); # initial values for variables x_1_1, x_2_1, x_3_1
        E0  = (2000000); # initial values for enzymes e_1_1, e_2_1
    };
}

