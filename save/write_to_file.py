import numpy as np

def write_to_file(gv):
    print(f'Save data to file...')
    with open(gv.save_path, 'w') as f:
        # Make sure all the queue in gv.all_data are the same length
        all_len = [len(d) for d in gv.all_data] + [len(gv.all_t)] \
                  + [len(gv.all_experiment_val)]
        min_len = min(all_len)
        # Remove extra data           # TODO: ALEXM: There is certainly a better way to do that (There is usually only one value in excess
        for i in range(len(gv.all_data)):
            if len(gv.all_data[i]) > min_len:
                print('plus grand')
                gv.all_data[i].pop()

        print(len(gv.all_t))
        if len(gv.all_t) > min_len:
            gv.all_t.pop()

        print(len(gv.all_experiment_val) )
        if len(gv.all_experiment_val) > min_len:
            gv.all_experiment_val.pop()

        # Create the proper dimension for the concatenation
        t_queue = np.array(gv.all_t)[None, :]
        experiment_queue = np.array(gv.all_experiment_val)[None, :]

        # Concatenate
        save_val = np.concatenate((gv.all_data, t_queue,
                                   experiment_queue))
        # Save
        np.savetxt(f, np.transpose(save_val), delimiter=',')