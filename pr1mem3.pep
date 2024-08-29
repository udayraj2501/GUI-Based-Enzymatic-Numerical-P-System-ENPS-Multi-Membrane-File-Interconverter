num_ps = {
    # membrane names (labels)
    H = {m1};

    structure = [m1 ]m1;

    # membrane 1
    m1 = {
        var = {x_1_1, x_2_1}; # variables used in the production function
        E = {e_1_1}; # set of enzyme variables
        pr = {x_1_1*x_2_1 [e_1_1 ->] 1|x_1_1};
        pr = {x_2_1 [e_1_1->] 1|x_2_1};
        var0 = (0, 6); # initial values for variables x_1_1, x_2_1, x_3_1
        E0  = (2000000); # initial values for enzymes e_1_1, e_2_1
    };
}