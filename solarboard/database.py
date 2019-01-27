import pandas as pd
import numpy as np

def get_queue():
    first_row = ["Trth-Master", 0, 1]
    feeds = [i for i in range(21)]
    slaves = [f"Trth-Slave-{i}" for i in range(21)]
    states = "waiting running finished failed".split()
    slave_states = np.random.choice([0, 1, 2, 3], 21, [0.2, 0.3,0.3,0.2])
    df = pd.DataFrame({"id": slaves, "feed_id": feeds, "status_code": slave_states})
    df.loc[0] = first_row
    df["status"] = df.status_code.apply(lambda x: states[x])
    return df