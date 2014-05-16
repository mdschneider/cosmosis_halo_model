from cosmosis import names, option_section
### HOD module from CHOMP http://code.google.com/p/chomp
import hod

# cosmo = names.cosmological_parameters
# likes = names.likelihoods
halo_model = names.halo_model_parameters

### Implemented HOD models in CHOMP
hod_models = ["Kravtsov", "Zheng", "Mandelbaum"]

def setup(options):
	### Which HOD model should we use?	
	hod_model = options[option_section, "hod_model"]
	if hod_model not in hod_models:
		raise KeyError("The requested HOD model not implented in CHOMP")

	### Create dictionary of HOD parameters
	### TODO: handle different names of arguments for different HOD models
	hod_dict = {"log_M_min": options[option_section, "log_M_min"],
				"sigma": options[option_section, "sigma"],
				"log_M_0": options[option_section, "log_M_0"],
				"log_M_1p": options[option_section, "log_M_1p"],
				"alpha": options[option_section, "alpha"]}

	### Instantiate the appropriate HOD class
	hod_class_name = "HOD" + hod_model
	print getattr(hod, hod_class_name)
	hod_instance = getattr(hod, hod_class_name)(hod_dict)

	return hod_instance

def execute(block, config):
	mass = block[halo_model, "M"]
	Nbar = config.first_moment(mass)
	block["halo_occupation", "first_moment"] = Nbar
	### TODO: compute int dmass first_moment * (camb output)
	# scipy.integrate.quad(my_mass_integral, ...)
	return 0

def cleanup(config):
	pass


