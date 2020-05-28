# Adam Kimbrough - Link Margin Calculator
# Assumes use of Wideband Nnetwork Waveform


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
thermal_noise_density = -174; # dBm

noise_figure = 0;
sig_to_noise = 0;

tx_pwr = int(input('Enter transmitter power (dBm): '));
tx_ant = float(input('Enter transmitter ant gain: '));
rx_ant = float(input('Enter receiver ant gain: '));
tx_ant_height = int(input('Enter base ant height (30 - 200m): '));
rx_ant_height = int(input('Enter mobile ant height (1 - 10m): '));
distance = int(input('Enter distance between TX & RX (m): '));
freq = int(input('Enter tx freq (MHz): '));
detect_bw = int(input('Enter detection bandwidth (MHz): '));
pwr_back_off = int(input('Enter power back-off: '));
tx_feed = int(input('Enter TX feed loss: '));
rx_feed = int(input('Enter RX feed loss: '));
noise_figure = int(input('Enter receiver NF: '));
sig_to_noise = int(input('Enter receiver\'s required S/N: '));

hb = tx_ant_height;
hm = rx_ant_height;
freq = float(freq);
# Correction factor (medium-small city)
a_hm = (1.1*math.log10(freq) - 0.7)*hm - (1.56*math.log10(freq) - 0.8);

# General Hata Model Equation
Lp = 69.55 + 26.16*math.log10(freq) - 13.82*math.log10(hb) - a_hm + (44.9 - 6.55*math.log10(hb)*math.log10(distance));

# Hata Model (Open Area) - based on urban losses
Lpo = Lp - 4.78*(math.log10(freq))**2 + 18.33*math.log10(freq) - 40.94;


thermal_noise_pwr = thermal_noise_density + 10*math.log10(1000000*detect_bw);

power_at_rx = (tx_pwr+tx_ant+rx_ant) - Lp - (pwr_back_off + tx_feed + rx_feed);
rx_sensitivity = thermal_noise_pwr + noise_figure + sig_to_noise;
link_margin = power_at_rx - rx_sensitivity;

print('--------------------------------');
print('Power left at input: ', power_at_rx);
print('Receiver sensitivity: ', rx_sensitivity);
print('**Link Margin** ', link_margin);

manual_margin = int(input('Enter receiver sensitivity manually to compute link margin: '));
print('**Link Margin** ', power_at_rx - manual_margin);
