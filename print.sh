for m in {beeler_reuter,luo_rudy,ten_tusscher,ohara,davies}
    do echo projects/PyAP/python/general_mcmc.py --data-file projects/PyAP/python/input/synthetic_"$m"/traces/synthetic_"$m"_trace_0.csv --unscaled -i 500000 --cheat
done

