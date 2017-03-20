py.test -k $1 -q --tb short                                         \
    | sed s:^=====:\\n:                                             \
    | sed s:=====$:\\n:                                             \
    | sed s:^_____:\\n:                                             \
    | sed s:_____$:\\n:                                             \
    | sed s:^-----:\\n:                                             \
    | sed s:-----$:\\n:                                             \
    | sed 's:^_ _ _ _ _::'                                          \
    | sed s:../.venv.3.6/lib/python3.6/site-packages:\\n.venv:      \
    | sed s:^test_:\\ntest_: