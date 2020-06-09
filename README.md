# Link-Budget
Link Margin Calculator

To run: python3 link-margin-calc.py

**************

** INPUTS **

Enter transmitter power (dBm):

Enter transmitter ant gain:

Enter receiver ant gain:

Enter base ant height (m):

Enter mobile ant height (m):

Enter distance between TX & RX (km): 

Enter tx freq (MHz): 

Enter detection bandwidth (MHz):

Enter power back-off: 

Enter TX feed loss: 

Enter RX feed loss: 

Enter 'Y' if you have RX sensitivity, otherwise, 'N'...  N

Enter receiver NF: 

Enter receiver's required S/N: 

Choose propagation model: 'FSPL', 'FSPL2'(ground refl only), 'HMS'(Hata med-small), 'HL'(Hata large): 

**************


** OUTPUTS ** 

Path loss:  [Path Loss in dBm]

Power left at input:  [Power in dBm]

Receiver sensitivity:  [RX Sensitivity in dBm]

\*\*Link Margin\*\* 

[Link Margin in dBm]

PLOT OPENS IN NEW WINDOW
**************


**\\\Propagation Model Explanations//**

FSPL (Free Space Path Loss)

FSPL2 (2-Ray Propogation Model w/ Ground Reflections) 

*Hata COST-231 Model (valid from 1.5 GHz to 2.0 GHz)*

*based on open area urban losses, not surburban

*only use for base antenna height 30m-200m?

HMS (medium-small city)

HL (large city)
