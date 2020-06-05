# Adam Kimbrough - Link Margin Calculator
from math import log10, pow, pi, atan, sqrt, sin, cos
import matplotlib.pyplot as plt
import numpy as np

# Gains
tx_pwr = 0;
tx_ant = 0;
rx_ant = 0;

# Pass Loss Info
path_loss = 0;
tx_ant_height = 0;
rx_ant_height = 0;
distance = 0;
freq = 0;
hb = 0;
hm = 0;
a_hm = 0;
a_hm2 = 0;

# Losses
tx_feed = 0;
rx_feed = 0;
pwr_back_off = 0;
thermal_noise_density = -174.0; # dBm

noise_figure = 0;
sig_to_noise = 0;

# Prop Model Booleans
fspl_bool = False
fspl2_bool = False
hms_bool = False
hl_bool = False


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

def sign(a):
    return (a > 0) - (a < 0)

def thermal_noise_power(tnd, bw):
	tnp = tnd + 10*log10(1000000*bw);
	return tnp

def pl_calc():
	global fspl_bool, fspl2_bool, hms_bool, hl_bool, thermal_noise_pwr, noise_figure, sig_to_noise
	have_rx_sens = input("Enter 'Y' if you have RX sensitivity, otherwise, 'N'...  ")
	if (have_rx_sens.upper() == 'Y'):
		manual_margin = int(input('Enter RX sensitivity: '));

		prop_model = input("Choose propagation model: 'FSPL', 'HMS'(Hata med-small), 'HL'(Hata large), 'FSPL2'(ground refl only): ")

		if (prop_model.upper() == 'FSPL'):
			path_loss = 20*log10(distance) + 20*log10(freq) + 32.44
			fspl_bool = True
		elif (prop_model.upper() == 'HMS'):

			# Correction factor (medium-small city)
			a_hm = (1.1*log10(freq)-0.7)*hm - (1.56*log10(freq)-0.8)

			# General Hata Model Equation
			Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(distance);
			# Hata Model (Open Area) - based on urban losses
			path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
			hms_bool = True
		elif (prop_model.upper() == 'HL'):
			# Correction factor (large city)
			a_hm2 = 3.2*(pow(log10(11.75*hm),2)) - 4.97
			# General Hata Model Equation
			Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(distance);
			# Hata Model (Open Area) - based on urban losses
			path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
			hl_bool = True
		elif (prop_model.upper() == 'FSPL2'):
			# Free Space Path Loss Model w/ Ground Reflection
			G = tx_ant * rx_ant
			path_loss = 40*log10(distance*1000) - 10*log10(G*pow(hb,2)*pow(hm, 2))
			fspl2_bool = True
		else:
			print('Invalid option')

		power_at_rx = (tx_pwr+tx_ant+rx_ant) - path_loss - (pwr_back_off + tx_feed + rx_feed);
		link_margin = power_at_rx - manual_margin
		print('--------------------------------');
		print('Path loss: ', path_loss);
		print('Power left at input: ', power_at_rx);
		print('**Link Margin** ');
		print(link_margin)

	elif (have_rx_sens.upper() == 'N'):
		noise_figure = float(input('Enter receiver NF: '));
		sig_to_noise = float(input('Enter receiver\'s required S/N: '));

		prop_model = input("Choose propagation model: 'FSPL', 'FSPL2'(ground refl only), 'HMS'(Hata med-small), 'HL'(Hata large): ")
		if (prop_model.upper() == 'FSPL'):
			path_loss = 20*log10(distance) + 20*log10(freq) + 32.44
			fspl_bool = True
			power_at_rx = (tx_pwr+tx_ant+rx_ant) - path_loss - (pwr_back_off + tx_feed + rx_feed);
		elif (prop_model.upper() == 'HMS'):

			# Correction factor (medium-small city)
			a_hm = (1.1*log10(freq)-0.7)*hm - (1.56*log10(freq)-0.8)

			# General Hata Model Equation
			Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(distance);
			# Hata Model (Open Area) - based on urban losses
			path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
			hms_bool = True
			power_at_rx = (tx_pwr+tx_ant+rx_ant) - path_loss - (pwr_back_off + tx_feed + rx_feed);

		elif (prop_model.upper() == 'HL'):
			# Correction factor (large city)
			a_hm2 = 3.2*(pow(log10(11.75*hm),2)) - 4.97
			# General Hata Model Equation
			Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm2 + (44.9 - 6.55*log10(hb))*log10(distance);
			# Hata Model (Open Area) - based on urban losses
			path_loss = Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94;
			hl_bool = True
			power_at_rx = (tx_pwr+tx_ant+rx_ant) - path_loss - (pwr_back_off + tx_feed + rx_feed);

		elif (prop_model.upper() == 'FSPL2'):
			# Free Space Path Loss Model w/ Ground Reflection
			# G = tx_ant * rx_ant
			# path_loss = 40*log10(distance*1000) - 10*log10(G*pow(hb,2)*pow(hm, 2))
			fspl2_bool = True

			c = 299.972458 * pow(10,6); # Speed of light in vaccum [m/s]
			Gr = rx_ant; # Antenna Gain receiving antenna.
			Gt = tx_ant; # Antenna Gain transmitting antenna.
			Pt = pow(10, tx_pwr/10)/1000; # Energy to the transmitting antenna [Watt]
			er = 18;
			wave_len = c/(freq*1000000)
			phi = atan((hb+hm)/(distance*1000)); # phi incident angle to ground.
			direct_wave=sqrt(pow(abs(hb-hm),2)+pow(distance*1000, 2)); # Distance, traveled direct wave
			refl_wave=sqrt(pow(distance*1000,2)+pow((hb+hm),2)); # Distance, traveled reflected wave
			gamma=(er*sin(phi)-sqrt(er-pow(cos(phi),2)))/(er*sin(phi)+sqrt(er-pow(cos(phi),2))); # Vertical polarization
			length_diff=refl_wave-direct_wave;
			cos_phase_diff=cos(length_diff*2*pi/wave_len)*sign(gamma);
			Direct_energy=Pt*Gt*Gr*pow(wave_len,2)/(pow((4*pi*direct_wave),2));
			reflected_energy=Pt*Gt*Gr*pow(wave_len,2)/(pow((4*pi*refl_wave),2))*abs(gamma);
			Total_received_energy=Direct_energy+cos_phase_diff*reflected_energy;
			Total_received_energy_dBm=10*log10(Total_received_energy*1e3);
			path_loss = (tx_pwr+tx_ant+rx_ant) - Total_received_energy_dBm - (pwr_back_off + tx_feed + rx_feed);
			power_at_rx = Total_received_energy_dBm - (pwr_back_off + tx_feed + rx_feed);

		else:
			print('Invalid option');

		thermal_noise_pwr = thermal_noise_power(thermal_noise_density, detect_bw)
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

	return (fspl_bool, fspl2_bool, hms_bool, hl_bool, tx_pwr, tx_ant, rx_ant)


def plp(pl, total_dist, model1, model2, model3, model4, tx_freq, tnp, nf, sn, txp, txant, rxant):
	distance2 = float(input('Enter assumed max FSPL distance (mi) from table: '));
	path_loss2 = 20*log10(distance2*1.60934) + 20*log10(freq) + 32.44
	power_at_rx2 = (txp+txant+rxant) - path_loss2; # neglects (pwr_back_off + tx_feed + rx_feed)
	rx_sensitivity2 = tnp + nf + sn;
	link_margin2 = power_at_rx2 - rx_sensitivity2;
	print(link_margin2)
	path_loss_arr = []
	link_margin_arr = []
	dist_arr = []
	i = 0
	total_dist = total_dist
	for dist in np.arange(1, total_dist, 0.01):
		if model1:
			path_loss_arr.append(20*log10(dist) + 20*log10(tx_freq) + 32.44)
			dist_arr.append(dist)
			power_at_rx = float((tx_pwr+tx_ant+rx_ant) - path_loss_arr[i] - (pwr_back_off + tx_feed + rx_feed));
			rx_sensitivity = float(tnp + nf + sn);
			link_margin_arr.append(power_at_rx - rx_sensitivity)
			i += 1

		if model2:
			c = 299.972458 * pow(10,6); # Speed of light in vaccum [m/s]
			Gr = rx_ant; # Antenna Gain receiving antenna.
			Gt = tx_ant; # Antenna Gain transmitting antenna.
			Pt = pow(10, tx_pwr/10)/1000; # Energy to the transmitting antenna [Watt]
			er = 18;
			wave_len = c/(freq*1000000)
			phi = atan((hb+hm)/(dist*1000)); # phi incident angle to ground.
			direct_wave=sqrt(pow(abs(hb-hm),2)+pow(dist*1000, 2)); # Distance, traveled direct wave
			refl_wave=sqrt(pow(distance*1000,2)+pow((hb+hm),2)); # Distance, traveled reflected wave
			gamma=(er*sin(phi)-sqrt(er-pow(cos(phi),2)))/(er*sin(phi)+sqrt(er-pow(cos(phi),2))); # Vertical polarization
			length_diff=refl_wave-direct_wave;
			cos_phase_diff=cos(length_diff*2*pi/wave_len)*sign(gamma);
			Direct_energy=Pt*Gt*Gr*pow(wave_len,2)/(pow((4*pi*direct_wave),2));
			reflected_energy=Pt*Gt*Gr*pow(wave_len,2)/(pow((4*pi*refl_wave),2))*abs(gamma);
			Total_received_energy=Direct_energy+cos_phase_diff*reflected_energy;
			Total_received_energy_dBm=10*log10(Total_received_energy*1e3);
			path_loss_arr.append((tx_pwr+tx_ant+rx_ant) - Total_received_energy_dBm - (pwr_back_off + tx_feed + rx_feed));
			power_at_rx = Total_received_energy_dBm - (pwr_back_off + tx_feed + rx_feed);
			rx_sensitivity = float(tnp + nf + sn);
			dist_arr.append(dist)
			link_margin_arr.append(power_at_rx - rx_sensitivity)
			i += 1

		if model3:
			# Correction factor (medium-small city)
			a_hm = (1.1*log10(freq)-0.7)*hm - (1.56*log10(freq)-0.8)
			# General Hata Model Equation
			Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm + (44.9 - 6.55*log10(hb))*log10(dist);
			# Hata Model (Open Area) - based on urban losses
			path_loss_arr.append(Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94)
			dist_arr.append(dist)
			power_at_rx = float((tx_pwr+tx_ant+rx_ant) - path_loss_arr[i] - (pwr_back_off + tx_feed + rx_feed));
			rx_sensitivity = float(tnp + nf + sn);
			link_margin_arr.append(power_at_rx - rx_sensitivity)
			i += 1

		if model4:
			# Correction factor (large city)
			a_hm2 = 3.2*(pow(log10(11.75*hm),2)) - 4.97
			# General Hata Model Equation
			Lp = 69.55 + 26.16*log10(freq) - 13.82*log10(hb) - a_hm2 + (44.9 - 6.55*log10(hb))*log10(dist);
			# Hata Model (Open Area) - based on urban losses
			path_loss_arr.append(Lp - 4.78*(pow(log10(freq), 2)) + 18.33*log10(freq) - 40.94)
			dist_arr.append(dist)
			power_at_rx = float((tx_pwr+tx_ant+rx_ant) - path_loss_arr[i] - (pwr_back_off + tx_feed + rx_feed));
			rx_sensitivity = float(tnp + nf + sn);
			link_margin_arr.append(power_at_rx - rx_sensitivity)
			i += 1

	x1 = np.array(dist_arr)
	y1 = np.array(path_loss_arr)
	y2 = np.array(link_margin_arr)
	plt.plot(x1, y1, "-r", label = "path loss")
	plt.plot(x1, y2, "-g", label = "link margin")
	j = 0
	for xy in zip(x1,y1):
		if round(y2[j],2) == round(link_margin2, 2):
			plt.annotate('Breakpoint: (%.2f, %.2f)' % xy, xy = xy, textcoords = 'data')
			break
		j += 1
	if model1:
		plt.title('Path Loss/Link Margin vs. Range (FSPL)')
	if model2:
		plt.title('Path Loss/Link Margin vs. Range (2-Ray GR)')
	if model3:
		plt.title('Path Loss/Link Margin vs. Range (Hata: med-small city)')
	if model4:
		plt.title('Path Loss/Link Margin vs. Range (Hata: large city)')
	plt.xlabel('Range (km)')
	plt.ylabel('Path Loss/Link Margin (dBm)')
	plt.legend(loc="center right")
	plt.show()

fspl_bool, fspl2_bool, hms_bool, hl_bool, tx_pwr, tx_ant, rx_ant = pl_calc()
plp(path_loss, distance, fspl_bool, fspl2_bool, hms_bool, hl_bool, freq, thermal_noise_pwr, noise_figure, sig_to_noise, tx_pwr, tx_ant, rx_ant)
