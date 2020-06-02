# Adam Kimbrough - Link Margin Calculator
from math import log10, pow

import math

# Gains
tx_pwr = 0;
tx_ant = 0;
rx_ant = 0;

# Pass Loss Info
tx_ant_height = 0;
rx_ant_height = 0;
distance = 0;
freq = 0;
hb = 0;
hm = 0;
a_hm = 0;

# Losses
tx_feed = 0;
rx_feed = 0;
pwr_back_off = 0;
thermal_noise_density = -174.0; # dBm

noise_figure = 0;
sig_to_noise = 0;

tx_pwr = float(input('Enter transmitter power (dBm): '));
tx_ant = float(input('Enter transmitter ant gain: '));
rx_ant = float(input('Enter receiver ant gain: '));
tx_ant_height = float(input('Enter base ant height (m): '));
rx_ant_height = float(input('Enter mobile ant height (m): '));
distance = float(input('Enter distance between TX & RX (km): '));
freq = float(input('Enter tx freq (MHz): '));
detect_bw = float(input('Enter detection bandwidth (MHz): '));
pwr_back_off = float(input('Enter power back-off: '));
tx_feed = float(input('Enter TX feed loss: '));
rx_feed = float(input('Enter RX feed loss: '));

hb = tx_ant_height;
hm = rx_ant_height;

have_rx_sens = input("Enter 'Y' if you have RX sensitivity, otherwise, 'N'...  ")
if (have_rx_sens.upper() == 'Y'):
	manual_margin = int(input('Enter RX sensitivity: '));

	prop_modelap = input("Choose propagation model: 'FSPL', 'HMS'(Hata med-small), 'HL'(Hata large), 'FSPL2'(ground refl only): ")

	if (prop_model.upper() == 'FSPL'):
		path_loss = 20*log10(distance) + 20*log10(freq) + 32.44

	elif (prop_model.upper() == 'HMS'):

		# Correction factor (medium-small city)
		a_hm = (1.1*log10(freq)-0.7)*hm - (1.56*log10(freq)-0.8)

		# General Hata Model Equation
		Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(distance);
		# Hata Model (Open Area) - based on urban losses
		path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
	elif (prop_model == 'HL'):
		# Correction factor (large city)
		a_hm2 = 3.2*(pow(log10(11.75*hm),2)) - 4.97
		# General Hata Model Equation
		Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(distance);
		# Hata Model (Open Area) - based on urban losses
		path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
	elif (prop_model.upper() == 'FSPL2'):
		# Free Space Path Loss Model w/ Ground Reflection
		G = tx_ant * rx_ant
		path_loss = 40*log10(distance*1000) - 10*log10(G*pow(hb,2)*pow(hm, 2))
	else:
		print('Invalid option')

	power_at_rx = (tx_pwr+tx_ant+rx_ant) - path_loss - (pwr_back_off + tx_feed + rx_feed);

	print('--------------------------------');
	print('Path loss: ', path_loss);
	print('Power left at input: ', power_at_rx);
	print('**Link Margin** ');
	print(power_at_rx - manual_margin)

elif (have_rx_sens.upper() == 'N'):
	noise_figure = float(input('Enter receiver NF: '));
	sig_to_noise = float(input('Enter receiver\'s required S/N: '));

	prop_model = input("Choose propagation model: 'FSPL', 'HMS'(Hata med-small), 'HL'(Hata large), 'FSPL2'(ground refl only): ")
	if (prop_model.upper() == 'FSPL'):
		path_loss = 20*log10(distance) + 20*log10(freq) + 32.44

	elif (prop_model.upper() == 'HMS'):

		# Correction factor (medium-small city)
		a_hm = (1.1*log10(freq)-0.7)*hm - (1.56*log10(freq)-0.8)

		# General Hata Model Equation
		Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(distance);
		# Hata Model (Open Area) - based on urban losses
		path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
	elif (prop_model.upper() == 'HL'):
		# Correction factor (large city)
		a_hm2 = 3.2*(pow(log10(11.75*hm),2)) - 4.97
		# General Hata Model Equation
		Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(distance);
		# Hata Model (Open Area) - based on urban losses
		path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
	elif (prop_model.upper() == 'FSPL2'):
		# Free Space Path Loss Model w/ Ground Reflection
		G = tx_ant * rx_ant
		path_loss = 40*log10(distance*1000) - 10*log10(G*pow(hb,2)*pow(hm, 2))
	else:
		print('Invalid option');

	thermal_noise_pwr = thermal_noise_density + 10*log10(1000000*detect_bw);
	power_at_rx = (tx_pwr+tx_ant+rx_ant) - path_loss - (pwr_back_off + tx_feed + rx_feed);
	rx_sensitivity = thermal_noise_pwr + noise_figure + sig_to_noise;
	link_margin = power_at_rx - rx_sensitivity;
	print('--------------------------------');
	print('Path loss: ', path_loss);
	print('Power left at input: ', power_at_rx);
	print('Receiver sensitivity: ', rx_sensitivity);
	print('**Link Margin** ');
	print(link_margin)

else:
	print('Invalid input');
