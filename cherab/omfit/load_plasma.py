from cherab.solps import load_solps_from_mdsplus, load_solps_from_raw_output, load_solps_from_balance

def load_edge_simulation(config, world):

    # Only try to do something if edge plasma has been selected as True
    try:
        if not config["plasma"]["edge"]["present"]:
            raise ValueError("This config file does not specify an edge plasma.")
    except KeyError:
        raise ValueError("This config file does not specify an edge plasma.")

    if config["plasma"]["edge"]["type"] == "SOLPS":
        return _load_solps_simulation(config, world)

    else:
        raise ValueError("Unrecognised simulation type.")


def _load_solps_simulation(config, world):

    if config["plasma"]["edge"]["SOLPS_format"] == "MDSplus":

        mds_server = config["plasma"]["edge"]["solps_reference"]["mds_server"]
        mds_solps_reference = config["plasma"]["edge"]["solps_reference"]["reference"]

        sim = load_solps_from_mdsplus(mds_server, mds_solps_reference)
            
    elif config["plasma"]["edge"]["SOLPS_format"] == "RawFiles":

        solps_directory = config["plasma"]["edge"]["solps_reference"]
        sim = load_solps_from_raw_output(solps_directory, debug=True)

    elif config["plasma"]["edge"]["SOLPS_format"] == "balance.nc":

        solps_directory = config["plasma"]["edge"]["solps_reference"]
        sim = load_solps_from_balance(solps_directory)

    else:
        raise ValueError("Unrecognised SOLPS format '{}'.".format(config["plasma"]["edge"]["SOLPS_format"]))

    plasma = sim.create_plasma(parent=world)
    mesh = sim.mesh

    return plasma, mesh