py.test -q --tb short -k $*                                             \
    | awk '!a[$0]++'                                                    \
    | sed s:^=========:\\n:                                             \
    | sed s:=========$:\\n:                                             \
    | sed s:^_________:\\n:                                             \
    | sed s:_________$:\\n:                                             \
    | sed s:^---------:\\n:                                             \
    | sed s:---------$:\\n:                                             \
    | sed 's:^_ _ _ _ _::'                                              \
    | sed s:../.venv.3.6/lib/python3.6/site-packages.*:_:               \
    | sed 's:    .*:_:'                                                 \
    | sed s:^test_run.py:\\ntest_run.py:                                \
    | sed s:^E:\\nE:                                                    \
    | sed '/^_$/d'                                                      \
    | sed '/^E_$/d'